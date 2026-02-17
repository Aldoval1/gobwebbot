import discord
from discord.ext import commands
import os
import aiohttp
from aiohttp import web
from dotenv import load_dotenv

# Cargar variables
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

# --- CONFIGURACIÓN ---
GUILD_ID = 1407095652718215480 
ROLE_ID = 1407095970650521681  

TOKEN = os.getenv("DISCORD_TOKEN")
WEB_APP_URL = os.getenv("WEB_APP_URL", "http://127.0.0.1:5000")
BOT_PORT = int(os.getenv("BOT_PORT", 8080))

intents = discord.Intents.default()
intents.members = True 
intents.message_content = True

class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        # Sincronización básica (por si añades comandos administrativos en el futuro)
        guild = discord.Object(id=GUILD_ID)
        self.tree.copy_global_to(guild=guild)
        await self.tree.sync(guild=guild)
        print("✅ Bot listo y escuchando a la web.")

bot = MyBot()

@bot.event
async def on_ready():
    print(f'🤖 Bot conectado como {bot.user}')
    # Iniciar servidor web interno para recibir órdenes de la web
    bot.loop.create_task(start_web_server())

# --- EVENTO: MIEMBRO ENTRA ---
@bot.event
async def on_member_join(member):
    if member.guild.id != GUILD_ID:
        return

    print(f"👋 Nuevo miembro: {member.display_name} ({member.id})")

    # Fetch Config from Web App
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{WEB_APP_URL}/api/bot_config") as resp:
                if resp.status != 200:
                    print(f"❌ Error fetching bot config: {resp.status}")
                    return
                config = await resp.json()
    except Exception as e:
        print(f"❌ Exception fetching config: {e}")
        return

    # 1. AutoRoles
    if config.get('autoroles_enabled') and config.get('autoroles_ids'):
        role_ids = config['autoroles_ids'].split(',')
        roles_to_add = []
        for r_id in role_ids:
            try:
                role = member.guild.get_role(int(r_id))
                if role:
                    roles_to_add.append(role)
            except ValueError:
                continue

        if roles_to_add:
            try:
                await member.add_roles(*roles_to_add)
                print(f"✅ AutoRoles asignados a {member.display_name}: {[r.name for r in roles_to_add]}")
            except discord.Forbidden:
                print("❌ No tengo permisos para asignar roles.")
            except Exception as e:
                print(f"❌ Error asignando roles: {e}")

    # 2. Welcome Message (DM)
    if config.get('welcome_enabled') and config.get('welcome_message'):
        try:
            embed = discord.Embed(
                description=config['welcome_message'],
                color=0x00ff00
            )
            banner_url = config.get('welcome_banner_url')
            if banner_url and banner_url.strip():
                embed.set_image(url=banner_url)

            embed.set_footer(text=f"Bienvenido a {member.guild.name}")

            await member.send(embed=embed)
            print(f"✅ Mensaje de bienvenida enviado a {member.display_name}")
        except discord.Forbidden:
            print(f"⚠️ No pude enviar DM a {member.display_name} (MDs cerrados)")
        except Exception as e:
            print(f"❌ Error enviando bienvenida: {e}")

# --- ENDPOINT: PROCESAR VINCULACIÓN ---
# La web llamará a esto cuando el usuario complete el Login con Discord
async def handle_link_request(request):
    try:
        data = await request.json()
        discord_id = int(data.get('discord_id'))
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        
        print(f"🔗 Solicitud de vinculación recibida para ID: {discord_id}")

        guild = bot.get_guild(GUILD_ID)
        if not guild:
            print("❌ Error: Bot no está en el servidor configurado.")
            return web.Response(status=500, text="Bot not in guild")

        member = guild.get_member(discord_id)
        if not member:
            print(f"❌ Miembro {discord_id} no encontrado en el servidor.")
            # Intentamos fetch por si no está en caché
            try:
                member = await guild.fetch_member(discord_id)
            except discord.NotFound:
                 return web.Response(status=404, text="Member not found in Discord Server")

        role = guild.get_role(ROLE_ID)
        changes = []
        
        # 1. Asignar Rol
        if role and role not in member.roles:
            try:
                await member.add_roles(role)
                changes.append("Rol Verificado Asignado")
            except discord.Forbidden:
                print("❌ Permisos insuficientes para dar rol.")
                changes.append("Error al dar rol (Permisos Bot)")

        # 2. Cambiar Apodo
        new_nick = f"{first_name} {last_name}"
        if member.nick != new_nick:
            try:
                await member.edit(nick=new_nick)
                changes.append(f"Nombre cambiado a: {new_nick}")
            except discord.Forbidden:
                print("❌ Permisos insuficientes para cambiar apodo.")
                changes.append("Error al cambiar nombre (Permisos Bot)")

        # 3. Enviar Mensaje Privado
        embed = discord.Embed(
            title="✅ Cuenta Vinculada Exitosamente",
            description=f"Hola **{first_name}**, tu cuenta de Gobierno ha sido vinculada correctamente con Discord.",
            color=0x00ff00
        )
        if changes:
            embed.add_field(name="Cambios Aplicados", value="\n".join(changes))
        
        try:
            await member.send(embed=embed)
        except discord.Forbidden:
            print("⚠️ El usuario tiene los MDs cerrados.")

        return web.Response(text="Linked successfully")

    except Exception as e:
        print(f"❌ Error crítico en handle_link: {e}")
        return web.Response(status=500, text=str(e))

# --- ENDPOINT: NOTIFICACIONES GENÉRICAS ---
async def handle_notification(request):
    try:
        data = await request.json()
        user = await bot.fetch_user(int(data.get('discord_id')))
        if user:
            embed = discord.Embed(description=data.get('message'), color=0x5865F2)
            embed.set_footer(text="Gobierno de San Andreas")
            await user.send(embed=embed)
            return web.Response(text="OK")
    except:
        pass
    return web.Response(status=200)

# --- ENDPOINT: OBTENER ROLES ---
async def handle_get_roles(request):
    try:
        guild = bot.get_guild(GUILD_ID)
        if not guild:
            return web.json_response([], status=503)

        roles = []
        for role in guild.roles:
            if role.name != "@everyone" and not role.managed:
                roles.append({'id': str(role.id), 'name': role.name})

        # Ordenar alfabéticamente
        roles.sort(key=lambda x: x['name'])

        return web.json_response(roles)
    except Exception as e:
        print(f"Error fetching roles: {e}")
        return web.json_response({'error': str(e)}, status=500)

async def start_web_server():
    app = web.Application()
    app.router.add_post('/link_discord', handle_link_request) # Nueva ruta para vinculación
    app.router.add_post('/notify', handle_notification)
    app.router.add_get('/roles', handle_get_roles)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', BOT_PORT)
    await site.start()
    print(f"📡 Escuchando órdenes en puerto {BOT_PORT}")

if __name__ == "__main__":
    if TOKEN:
        bot.run(TOKEN)
    else:
        print("Falta DISCORD_TOKEN")