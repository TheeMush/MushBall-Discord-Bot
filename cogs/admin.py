import discord
from discord.ext import commands

class admin(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['slow'])
    @commands.has_permissions(administrator=True)
    async def slowmode(self,ctx,seconds = None):
        if seconds == None:
            embed = discord.Embed(description="• **.slowmode** `TIME`", color=0xFF0000)
            embed.set_author(name = "Slowmode Usage:",icon_url=ctx.author.avatar_url)
            await ctx.reply(embed=embed)
            return
        if seconds == 'off':
            seconds = 0
            await ctx.channel.edit(slowmode_delay=seconds)
            embed = discord.Embed(description=f"**Turned off Slowmode in {ctx.channel.mention}**",color=discord.Colour.random())
            embed.set_author(name=f"{ctx.message.guild.name} | Slowmode", icon_url=ctx.guild.icon_url)
            await ctx.send(embed=embed)
            return
        else:
            seconds = int(seconds)

        await ctx.channel.edit(slowmode_delay=seconds)
        embed = discord.Embed(description=f"**Set Slowmode to `{seconds}` Seconds in {ctx.channel.mention}**",color=discord.Colour.random())
        embed.set_author(name=f"{ctx.message.guild.name} | Slowmode", icon_url=ctx.guild.icon_url)
        await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def mute(self,ctx, member: discord.Member = None):
        if member == None:
            embed = discord.Embed(description="• **.mute** `@USER`", color=0xFF0000)
            embed.set_author(name = "Mute Usage:",icon_url=ctx.author.avatar_url)
            await ctx.reply(embed=embed)
            return

        role = discord.utils.get(ctx.guild.roles, name="Muted")
        guild = ctx.guild

        if role not in guild.roles:
            perms = discord.Permissions(send_messages=False, speak=False)
            await guild.create_role(name="Muted", permissions=perms)
            await member.add_roles(role)
            embed = discord.Embed(description=f"**{member.mention} was muted.**",color=discord.Colour.random())
            embed.set_author(name=f"{ctx.message.guild.name} | Mute", icon_url=ctx.guild.icon_url)
            await ctx.send(embed=embed)
        else:
            await member.add_roles(role) 
            embed = discord.Embed(description=f"**{member.mention} was muted.**",color=discord.Colour.random())
            embed.set_author(name=f"{ctx.message.guild.name} | Mute", icon_url=ctx.guild.icon_url)
            await ctx.send(embed=embed)


    @commands.command()
    @commands.has_permissions(administrator=True)
    async def unmute(self,ctx,member:discord.Member = None):
        if member == None:
            embed = discord.Embed(description="• **.unmute** `@USER`", color=0xFF0000)
            embed.set_author(name = "Unmute Usage:",icon_url=ctx.author.avatar_url)
            await ctx.reply(embed=embed)
            return
        role = discord.utils.get(ctx.guild.roles, name="Muted")
        await member.remove_roles(role)
        embed = discord.Embed(description=f"**{member.mention} was unmuted.**",color=discord.Colour.random())
        embed.set_author(name=f"{ctx.message.guild.name} | Unmute", icon_url=ctx.guild.icon_url)
        await ctx.send(embed=embed)

def setup(client):
    client.add_cog(admin(client))