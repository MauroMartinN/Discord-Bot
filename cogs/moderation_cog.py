import discord
from discord.ext import commands

class ModerationCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="ban")
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason="No se especificó motivo"):
        await member.ban(reason=reason)
        await ctx.send(f"🔨 {member} ha sido baneado.\n📝 Motivo: {reason}")
        print(f"[LOG] {member} fue baneado por {ctx.author} - Motivo: {reason}")

    @commands.command(name="kick")
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason="No se especificó motivo"):
        await member.kick(reason=reason)
        await ctx.send(f"🥾 {member} fue expulsado.\n📝 Motivo: {reason}")
        print(f"[LOG] {member} fue expulsado por {ctx.author} - Motivo: {reason}")

    @commands.command(name="mute")
    @commands.has_permissions(manage_roles=True)
    async def mute(self, ctx, member: discord.Member, *, reason="No se especificó motivo"):
        guild = ctx.guild
        muted_role = discord.utils.get(guild.roles, name="Muted")

        await member.add_roles(muted_role, reason=reason)
        await ctx.send(f"🔇 {member.mention} muted.")
        print(f"[LOG] {member} fue silenciado por {ctx.author} - Motivo: {reason}")
        
    @commands.command(name="unmute")
    @commands.has_permissions(manage_roles=True)
    async def unmute(self, ctx, member: discord.Member, *, reason="No se especificó motivo"):
        guild = ctx.guild
        muted_role = discord.utils.get(guild.roles, name="Muted")

        await member.remove_roles(muted_role, reason=reason)
        await ctx.send(f"🔇 {member.mention} unmuted.")
        print(f"[LOG] {member} fue dessilenciado por {ctx.author} - Motivo: {reason}")

    @commands.command(name="clear")
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount: int):
        await ctx.channel.purge(limit=amount + 1)
        await ctx.send(f"🧹 Se borraron {amount} mensajes.", delete_after=5)
        print(f"[LOG] {ctx.author} borró {amount} mensajes en #{ctx.channel}")

async def setup(bot):
    await bot.add_cog(ModerationCog(bot))
