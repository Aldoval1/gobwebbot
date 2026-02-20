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

# Nuevas configuraciones multi-guild
GOBIERNO_GUILD_ID = int(os.getenv("GOBIERNO_GUILD_ID") or GUILD_ID)
JUDICIAL_GUILD_ID = int(os.getenv("JUDICIAL_GUILD_ID") or 0)
CONGRESO_GUILD_ID = int(os.getenv("CONGRESO_GUILD_ID") or 0)

JUDICIAL_ROLE_ID = int(os.getenv("JUDICIAL_ROLE_ID") or 1473865577993994260)
CONGRESO_ROLE_ID = int(os.getenv("CONGRESO_ROLE_ID") or 1473835075375337740)

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

# --- ENDPOINT: PROCESAR VINCULACIÓN ---
# La web llamará a esto cuando el usuario complete el Login con Discord
async def handle_setup_account(request):
    try:
        data = await request.json()
        discord_id = int(data.get('discord_id'))
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        guild_keys = data.get('guilds', [])

        print(f"⚙️ Solicitud de configuración para ID: {discord_id} en {guild_keys}")
        
        results = []

        async def configure_guild(g_id, r_id):
            if not g_id: return "No configurado"
            guild = bot.get_guild(g_id)
            if not guild: return "Bot no está en el servidor"

            member = guild.get_member(discord_id)
            if not member:
                try:
                    member = await guild.fetch_member(discord_id)
                except discord.NotFound:
                    return "Usuario no encontrado en servidor"
                except Exception as e:
                    return f"Error fetch: {e}"

            # Nickname
            new_nick = f"{first_name} {last_name}"
            if member.nick != new_nick:
                try:
                    await member.edit(nick=new_nick)
                except discord.Forbidden:
                    print(f"⚠️ Sin permisos nick en {guild.name}")

            # Role
            if r_id:
                role = guild.get_role(r_id)
                if role and role not in member.roles:
                    try:
                        await member.add_roles(role)
                    except discord.Forbidden:
                        print(f"⚠️ Sin permisos rol en {guild.name}")

            return "OK"

        # Gobierno (Always)
        res = await configure_guild(GOBIERNO_GUILD_ID, ROLE_ID)
        results.append(f"Gobierno: {res}")

        if 'judicial' in guild_keys:
            res = await configure_guild(JUDICIAL_GUILD_ID, JUDICIAL_ROLE_ID)
            results.append(f"Judicial: {res}")

        if 'congreso' in guild_keys:
            res = await configure_guild(CONGRESO_GUILD_ID, CONGRESO_ROLE_ID)
            results.append(f"Congreso: {res}")

        # Notify User
        try:
             user = await bot.fetch_user(discord_id)
             if user:
                embed = discord.Embed(
                    title="✅ Configuración Completada",
                    description=f"Hola **{first_name}**, hemos configurado tu perfil en los servidores solicitados.\n\nResultados:\n" + "\n".join(results),
                    color=0x00ff00
                )
                await user.send(embed=embed)
        except:
            pass

        return web.Response(text="Setup complete")

    except Exception as e:
        print(f"❌ Error en setup_account: {e}")
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

async def start_web_server():
    app = web.Application()
    app.router.add_post('/setup_account', handle_setup_account) # Nueva ruta para vinculación multi-server
    app.router.add_post('/notify', handle_notification)
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