import os
from openai import OpenAI
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

session_histories = {}

@bot.event
async def on_ready():
    print(f" Bot conectado como {bot.user}")

@bot.command(name="chat")
async def chat(ctx, *, prompt: str):
    channel_id = str(ctx.channel.id)
    history = session_histories.get(channel_id, [])
    history.append({"role": "user", "content": prompt})

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=history
        )
        reply = response.choices[0].message.content
        await ctx.send(reply)

        history.append({"role": "assistant", "content": reply})
        session_histories[channel_id] = history[-10:]
    except Exception as e:
        await ctx.send("❌ Error al procesar la respuesta.")
        print("Error:", e)

@bot.command(name="reset")
async def reset(ctx):
    session_histories[str(ctx.channel.id)] = []
    await ctx.send("🔄 Contexto reiniciado.")

bot.run(DISCORD_TOKEN)
