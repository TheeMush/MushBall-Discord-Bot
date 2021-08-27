import discord
import random
import json
from discord.ext import commands

class Misc(commands.Cog):

    def __init__(self, client):
        self.client = client

    
    #Sarah Upload Command
    @commands.command()
    async def sarahupload1(self,ctx,arg):
        if ctx.author.id == 569792736367083560:
            jsonFile = open("sara2.json", "w")
            jsonFile.write(arg)
            jsonFile.close()
            await ctx.message.delete()
            await ctx.send("Success", delete_after=2)
        else:
            await ctx.message.delete()
            await ctx.send("No")
    @commands.command()
    async def sarahupload(self,ctx,arg):
        if ctx.author.id == 569792736367083560:
            jsonFile = open("sara.json", "w")
            jsonFile.write(arg)
            jsonFile.close()
            await ctx.message.delete()
            await ctx.send("Success", delete_after=2)
        else:
            await ctx.message.delete()
            await ctx.send("No")

    #Announce Command
    @commands.command()
    async def announce(self,ctx,arg1):
        channel = self.client.get_channel(766731745542275113)
        message = ' '.join(ctx.message.content.split(' ')[2:])
        embed=discord.Embed(title=f"{arg1}", description=f"{message}", color=0xff0000)
        await channel.send(embed=embed)
    @commands.command()
    async def announce1(self,ctx):
        if ctx.author.id == 569792736367083560:
            channel = self.client.get_channel(766731745542275113)
            await ctx.message.delete()
            message = ' '.join(ctx.message.content.split(' ')[1:])
            await channel.send(message)
        else:
            await ctx.send("No")

    @commands.command()
    async def servers(self,ctx):
        try:
            activeservers = self.client.guilds
            for guild in activeservers:
                await ctx.send(guild.name)
                print(guild.name)
        except Exception as e:
            await ctx.send(f'```{e}```')

    @commands.Cog.listener()
    async def on_message(self, message):
        try:
            if message.author.id == 557976700286140426: 
                #await message.delete()
                emote = "<:stinky:866708570216071209>"
            
                
        except Exception:
            pass
        with open('sara2.json') as f:
            s = json.load(f)
            s = str(s)
        with open('sara.json') as f:
            d = json.load(f)
            d = str(d)
        if s in message.content.lower() or d in message.content.lower():
                await message.reply("You mean Sarah")
        if '859950743674028052' in message.content.lower():
            await message.reply("You mean Sarah")
        if "sarah" in message.content.lower():
            pass
        elif 'sara' in message.content.lower():
            if message.channel.id == 814101565266067507:
                pass
            else:
                await message.reply("You mean Sarah")
    
    @commands.command()
    async def realname(self,ctx,member:discord.Member):
        await ctx.send(f"{member.mention}'s real name is {member.name}")
        
        

def setup(client):
    client.add_cog(Misc(client))