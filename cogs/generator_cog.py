import discord
from discord.ext import commands
import aiohttp
import os
from dotenv import load_dotenv
load_dotenv()

class GeneradorCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.n8n_url = os.getenv("N8N_WEBHOOK_URL")

    @commands.command(name="def")
    async def generar(self, ctx, *, mensaje: str):
        await ctx.send("Generando contenido... ⏳")
        payload = {
            "usuario": str(ctx.author),
            "mensaje": mensaje
        }

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(self.n8n_url, json=payload) as resp:
                    if resp.status == 200:
                        data = await resp.json()

                        if isinstance(data, list):
                            data = data[0]

                        audio_url = data.get("audio_url")
                        if not audio_url:
                            await ctx.send("❌ No se recibió ningún audio.")
                            return

                        async with session.get(audio_url) as audio_resp:
                            if audio_resp.status == 200:
                                audio_data = await audio_resp.read()
                                filename = "voz.wav"
                                with open(filename, "wb") as f:
                                    f.write(audio_data)

                                await ctx.send(file=discord.File(filename))
                                os.remove(filename)
                            else:
                                await ctx.send("❌ No se pudo descargar el audio.")
                    else:
                        await ctx.send(f"❌ Error al llamar a n8n: {resp.status}")
        except Exception as e:
            await ctx.send(f"❌ Error de conexión: {str(e)}")

async def setup(bot):
    await bot.add_cog(GeneradorCog(bot))
