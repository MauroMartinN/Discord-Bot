import os
from openai import OpenAI
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class ChatCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.session_histories = {}

    @commands.command(name="chat")
    async def chat(self, ctx, *, prompt: str):
        channel_id = str(ctx.channel.id)
        history = self.session_histories.get(channel_id, [])
        history.append({"role": "user", "content": prompt})

        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=history
            )
            reply = response.choices[0].message.content
            await ctx.send(reply)

            history.append({"role": "assistant", "content": reply})
            self.session_histories[channel_id] = history[-10:]
        except Exception as e:
            await ctx.send("Error al procesar la respuesta.")
            print("Error:", e)

    @commands.command(name="reset")
    async def reset(self, ctx):
        self.session_histories[str(ctx.channel.id)] = []
        await ctx.send("🔄 Contexto reiniciado.")

async def setup(bot):
    await bot.add_cog(ChatCog(bot))
