import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import asyncio

load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

initial_extensions = [
    "cogs.chat_cog",
    "cogs.moderation_cog",
    "cogs.music_cog",
    "cogs.fairtag_cog"
]

async def main():
    async with bot:
        for ext in initial_extensions:
            await bot.load_extension(ext)
        await bot.start(DISCORD_TOKEN)

@bot.event
async def on_ready():
    print(f"Bot conectado como {bot.user}")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nBot detenido.")
    except RuntimeError as e:
        if "Session is closed" in str(e):
            print("\nSesión HTTP cerrada correctamente durante el cierre del bot.")
        else:
            raise
