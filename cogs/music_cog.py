from discord import FFmpegPCMAudio
from discord.ext import commands
import yt_dlp
import asyncio

class MusicCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.temp_channels = set()

    @commands.command(name="join")
    async def join(self, ctx):
        try:
            if ctx.author.voice:
                channel = ctx.author.voice.channel
                await channel.connect()
                await ctx.send("✅ Me uní al canal de voz.")
            else:
                await ctx.send("❌ Debes estar en un canal de voz.")
        except Exception as e:
            await ctx.send(f"❌ Ocurrió un error: {e}")
            print(f"[ERROR] join command: {e}")

    @commands.command(name="leave")
    async def leave(self, ctx):
        if ctx.voice_client:
            await ctx.voice_client.disconnect()
            await ctx.send("👋 Me salí del canal de voz.")
        else:
            await ctx.send("❌ No estoy en un canal de voz.")

    @commands.command(name="play")
    async def play(self, ctx, *, url):
        print(f"[DEBUG] Comando play recibido con: {url}")

        if not ctx.voice_client:
            if ctx.author.voice:
                print(f"[DEBUG] Intentando unirse al canal de {ctx.author.voice.channel}")
                await ctx.author.voice.channel.connect()
                print("[DEBUG] Bot se unió al canal")
            else:
                await ctx.send("❌ Debes estar en un canal de voz.")
                return

        ydl_opts = {
            'format': 'bestaudio',
            'quiet': True,
            'noplaylist': True,
            'default_search': 'ytsearch',
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                print(f"[DEBUG] info extraída: {info}")

                if 'entries' in info:
                    info = info['entries'][0]

                audio_url = info['url']
                print(f"[DEBUG] URL audio: {audio_url}")


            source = FFmpegPCMAudio(audio_url, options='-vn')

            if ctx.voice_client.is_playing():
                ctx.voice_client.stop()

            def after_playing(error):
                if error:
                    print(f"[ERROR] Reproducción terminó con error: {error}")
                else:
                    print("Reproducción finalizada sin errores.")

            ctx.voice_client.play(source, after=after_playing)

            await ctx.send(f"▶️ Reproduciendo: **{info['title']}**")
        except Exception as e:
            await ctx.send(f"❌ Error al reproducir: {e}")
            print(f"[ERROR] {e}")
            
            
    @commands.command(name="bs")
    async def bs(self, ctx, member: commands.MemberConverter):
        if not ctx.author.voice:
            await ctx.send("❌ Debes estar en un canal de voz para usar este comando.")
            return

        channel = ctx.author.voice.channel

        try:
            guild = ctx.guild
            new_channel = await guild.create_voice_channel(name=f"BS - {member.display_name}", category=channel.category)
            self.temp_channels.add(new_channel.id)

            await member.move_to(new_channel)

            if ctx.voice_client:
                await ctx.voice_client.move_to(new_channel)
            else:
                await new_channel.connect()

            audio_source = FFmpegPCMAudio(
                "audio/bs.mp3",
                before_options='-ss 28',
                options='-vn'
            )

            if ctx.voice_client.is_playing():
                ctx.voice_client.stop()

            def after_playing(error):
                if error:
                    print(f"[ERROR] Reproducción terminó con error: {error}")
                else:
                    print("Reproducción finalizada sin errores.")

            ctx.voice_client.play(audio_source, after=after_playing)

            await ctx.send(f"🎤 {member.mention} ha sido movido al canal {new_channel.name} y empezó a sonar Baby Shark!")

        except Exception as e:
            await ctx.send(f"❌ Error al mover o reproducir: {e}")
            print(f"[ERROR] {e}")

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if before.channel and before.channel.id in self.temp_channels:
            channel = before.channel

            if len(channel.members) == 1:
                try:
                    await channel.delete()
                    self.temp_channels.remove(channel.id)
                    print(f"[INFO] Canal temporal {channel.name} borrado porque quedó vacío.")
                except Exception as e:
                    print(f"[ERROR] al borrar canal temporal: {e}")





    @commands.command(name="stop")
    async def stop(self, ctx):
        if ctx.voice_client and ctx.voice_client.is_playing():
            ctx.voice_client.stop()
            await ctx.send("⏹️ Reproducción detenida.")
        else:
            await ctx.send("❌ No hay música en reproducción.")
            

async def setup(bot):
    await bot.add_cog(MusicCog(bot))
