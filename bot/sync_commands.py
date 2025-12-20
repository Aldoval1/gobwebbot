import discord
from discord.ext import commands
import os
import asyncio
from dotenv import load_dotenv

# Cargar variables
load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
GUILD_ID = 1407095652718215480  # Tu ID de servidor

# Configuración mínima del bot para sincronizar
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Conectado como {bot.user}. Iniciando sincronización...")
    try:
        # 1. Limpiar comandos globales (por si acaso)
        bot.tree.clear_commands(guild=None)
        
        # 2. Definir el comando (necesitamos re-definirlo aquí para que sepa QUÉ sincronizar)
        # Nota: Normalmente esto se importa, pero para este test lo redefinimos simple
        # Solo para ver si APARECE en Discord.
        
        @bot.tree.command(name="verificar", description="Comando de prueba de sincronización")
        async def verificar(interaction: discord.Interaction):
            await interaction.response.send_message("¡Funcionando!", ephemeral=True)

        # 3. Sincronizar al servidor específico
        guild = discord.Object(id=GUILD_ID)
        bot.tree.copy_global_to(guild=guild)
        synced = await bot.tree.sync(guild=guild)
        
        print(f"¡ÉXITO! Se han sincronizado {len(synced)} comandos al servidor {GUILD_ID}.")
        print("Cierra este script y vuelve a iniciar bot/main.py")
        
    except Exception as e:
        print(f"ERROR: {e}")
    
    await bot.close()

if __name__ == "__main__":
    if not TOKEN:
        print("Error: No hay token en .env")
    else:
        asyncio.run(bot.start(TOKEN))