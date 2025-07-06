import discord
from discord.ext import commands
import aiohttp

class FairtagCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="info")
    async def info(self, ctx, *, city: str):
        url = f"http://localhost/index.php?c=pais&a=apiCiudad&city={city}"

        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url) as resp:
                    if resp.status != 200:
                        await ctx.send(f"⚠️ No se pudo obtener información para **{city}**. Código: {resp.status}")
                        return

                    data = await resp.json()

                    embed = discord.Embed(
                        title=f"🏙️ Coste de vida en {data['city']}",
                        color=discord.Color.blue()
                    )

                    embed.add_field(name="🍽️ Comida barata", value=f"{data['meal_inexpensive_restaurant']} €", inline=True)
                    embed.add_field(name="👫 Cena para 2", value=f"{data['meal_for_2_midrange']} €", inline=True)
                    embed.add_field(name="🍔 McMeal", value=f"{data['mcmeal_at_mcdonalds']} €", inline=True)
                    embed.add_field(name="🍺 Cerveza nacional (restaurante)", value=f"{data['beer_domestic_restaurant']} €", inline=True)
                    embed.add_field(name="☕ Cappuccino", value=f"{data['cappuccino_restaurant']} €", inline=True)
                    embed.add_field(name="🚌 Transporte mensual", value=f"{data['transport_monthly']} €", inline=True)
                    embed.add_field(name="⛽ Gasolina (1L)", value=f"{data['gasoline_1l']} €", inline=True)
                    embed.add_field(name="🏠 Piso 1 hab. centro", value=f"{data['apartment_1br_center']} €", inline=True)
                    embed.add_field(name="💰 Sueldo medio neto mensual", value=f"{data['avg_salary_monthly']} €", inline=True)

                    embed.set_footer(text="Fuente: FairTag")

                    await ctx.send(embed=embed)

            except Exception as e:
                await ctx.send(f"❌ Error al obtener los datos: {str(e)}")
async def setup(bot):
    await bot.add_cog(FairtagCog(bot))
