import discord
import random
import requests
from discord.ext import commands
from bs4 import BeautifulSoup
from discord.utils import get


class Mushball(commands.Cog):

    def __init__(self, client):
        self.client = client

    #Fuck Command
    @commands.cooldown(1, 5, commands.BucketType.member)
    @commands.command()
    async def fuck(self, ctx):
        from cogs.Lists.lists import menace
        ranmenace = random.choice(menace)
        await ctx.send(ranmenace)

    #8ball Command
    @commands.command(aliases=["8ball"])
    async def mushball(self, ctx, *, message = None):
        if message == None:
            embed = discord.Embed(description="• **.mushball `<ASK A QUESTION>`\n• Aliases = `.8ball`", color=discord.Colour.random())
            embed.set_author(name = "MushBall Usage:",icon_url=ctx.author.avatar_url)
            await ctx.reply(embed=embed)
            return
        if "mush" in message:
            await ctx.send("I cant answer questions about Mush")
        elif "569792736367083560" in message:
            await ctx.send("I cant answer questions about Mush")
        else:
            from cogs.Lists.lists import reactions
            ranemote = random.choice(reactions)
            await ctx.message.add_reaction(emoji=ranemote)

    #Hello Command
    @commands.cooldown(1, 5, commands.BucketType.member)
    @commands.command(aliases = ["hi","himush"])
    async def himushball(self,ctx):
        from cogs.Lists.lists import greetings
        rangreet = random.choice(greetings)
        await ctx.send(f"{rangreet} {ctx.author.mention}")

    #Goodbye Command
    @commands.cooldown(1, 5, commands.BucketType.member)
    @commands.command(aliases = ["bye","byemush"])
    async def byemushball(self,ctx):
        from cogs.Lists.lists import goodbyes
        ranbye = random.choice(goodbyes)
        await ctx.send(f"{ranbye} {ctx.author.mention}")

    #Sleep Command
    @commands.cooldown(1, 5, commands.BucketType.member)
    @commands.command(aliases = ["sleep"])
    async def mushsleep(self,ctx, arg1 = None):
        if arg1 == None:
            embed = discord.Embed(description="• **.mushsleep `@USER`\n• Aliases = `.sleep`", color=discord.Colour.random())
            embed.set_author(name = "MushSleep Usage:",icon_url=ctx.author.avatar_url)
            await ctx.reply(embed=embed)
            self.mushsleep.reset_cooldown(ctx)
            return
        if "569792736367083560" in arg1:
            await ctx.send("Dont tell Mush what to do")
        else:
            from cogs.Lists.lists import sleep
            ransleep = random.choice(sleep)
            await ctx.send(f"{ransleep}{arg1}")

    #Crypto Command
    @commands.cooldown(1, 5, commands.BucketType.member)
    @commands.command(aliases = ["crypto"])
    async def mushcrypto(self, ctx):
        #Gets info from website
        URL = 'https://coinmarketcap.com/'
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, 'html.parser')
        results = soup.find("h1", class_="sc-1q9q90x-0 dlDcED")
        results2 = soup.find("p", class_="sc-1eb5slv-0 bSDVZJ")
        results3 = soup.find("p", class_="sc-1eb5slv-0 kOjPMg")
        #Sends Embed
        embed = discord.Embed(title="MushBall Crypto", color=discord.Colour.random())
        embed.set_thumbnail(url="https://cdn.betterttv.net/emote/5e08940c8245800d97564e14/3x")
        embed.add_field(name=f"{results.text}",value="‎‎‎‎‎‎‎‎‎‎‎‎‎‎",inline=False)
        embed.add_field(name="‎‎‎‎‎‎‎‎‎‎",value=f"{results2.text}‎‎‎‎‎‎‎‎‎‎‎‎‎‎",inline=False)
        embed.add_field(name="‎‎‎‎‎‎‎‎‎‎",value=f"{results3.text}‎‎‎‎‎‎‎‎‎‎‎‎‎‎",inline=False)
        await ctx.send(embed=embed)

    #Compatibility Command
    @commands.cooldown(1, 5, commands.BucketType.member)
    @commands.command(aliases = ["match"])
    async def mushmatch(self, ctx, *, message = None):
        if message == None:
            embed = discord.Embed(description="• **.mushmatch `@USER`\n• Aliases = `.match`", color=discord.Colour.random())
            embed.set_author(name = "MushMatch Usage:",icon_url=ctx.author.avatar_url)
            await ctx.reply(embed=embed)
            self.mushmatch.reset_cooldown(ctx)
            return
        if ctx.author.id == 277560453977079818:
            if "727251965507010702" in message:
                await ctx.reply("https://tenor.com/view/vegeta-its-over9000-gif-14419267")
        elif ctx.author.id == 126421766020136960:
            await ctx.reply("https://tenor.com/view/yeah-that-brothers-starving-starving-gif-19331207")
        elif ctx.author.id == 557976700286140426:
            if "569792736367083560" in message:
                await ctx.reply("https://tenor.com/view/do-you-understand-that-this-man-loves-you-steve-harvey-steve-on-watch-feelings-in-love-gif-16817328")
        elif "766973249103724564" in message:
            await ctx.reply("https://tenor.com/view/handshake-shake-you-got-it-deal-nice-gif-5778373")
        elif "569792736367083560" in message:
            await ctx.reply("Why are you so obsessed with Mush")
        elif "mush" in message:
            await ctx.reply("Why are you so obsessed with Mush")
        elif ctx.author.id == 569792736367083560:
            if "‎" in ctx.message.content:
                from cogs.Lists.lists import disgust
                randisgust = random.choice(disgust)
                embed = discord.Embed(title=f"<a:bongoheart:831724871594541066> MushBall Compatibility <a:bongoheart:831724871594541066>", color=discord.Colour.random())
                embed.add_field(name="‎‎‎‎‎‎‎‎‎‎‎‎‎‎",value=f"**{ctx.author.mention} AND {message}‎‎‎‎‎‎‎‎‎‎‎‎‎‎?**",inline=False)
                embed.set_image(url=f"{randisgust}")
                await ctx.reply(embed=embed)
            else:
                mushcomp = [
                    "You should DM Mush",
                    "You're Mush, you're compatible with everyone",
                    "You know don't even need me to tell you it's a high percantage",
                    "You're probably already in their DM's, why you checking this"
                ]
                ranmushcomp = random.choice(mushcomp)
                mushnum = random.randint(97, 110)
                embed = discord.Embed(title=f"MushBall Compatibility", color=discord.Colour.random())
                embed.set_thumbnail(url="https://cdn.betterttv.net/emote/5b3e4576477e3e4508285548/3x")
                embed.add_field(name="‎‎‎‎‎‎‎‎‎‎‎‎‎‎",value=f"<a:bongoheart:831724871594541066>Lets see how compatible {ctx.author.mention} is with {message}‎‎‎‎‎‎‎‎‎‎‎‎‎‎<a:bongoheart:831724871594541066>",inline=False)
                embed.add_field(name=f"You two are {mushnum}% compatible",value="‎‎‎‎‎‎‎‎‎‎‎‎‎‎",inline=False)
                embed.add_field(name="‎‎‎‎‎‎‎‎‎‎‎‎‎‎",value=f"{ranmushcomp}",inline=False)
                await ctx.send(embed=embed)
        else:
            rannum = random.randint(-1, 101)
            embed = discord.Embed(title=f"MushBall Compatibility", color=discord.Colour.random())
            embed.set_thumbnail(url="https://cdn.betterttv.net/emote/5b3e4576477e3e4508285548/3x")
            embed.add_field(name="‎‎‎‎‎‎‎‎‎‎‎‎‎‎",value=f"<a:bongoheart:831724871594541066>Lets see how compatible {ctx.author.mention} is with {message}‎‎‎‎‎‎‎‎‎‎‎‎‎‎<a:bongoheart:831724871594541066>",inline=False)
            embed.add_field(name=f"You two are {rannum}% compatible", value="‎‎‎‎‎‎‎‎‎‎‎‎‎‎",inline=False)
            from cogs.Lists.lists import lowcomp
            ranlowcomp = random.choice(lowcomp)
            from cogs.Lists.lists import medlowcomp
            ranmedlowcomp = random.choice(medlowcomp)
            from cogs.Lists.lists import highlowcomp
            ranhighlowcomp = random.choice(highlowcomp)
            from cogs.Lists.lists import medcomp
            ranmedcomp = random.choice(medcomp)
            from cogs.Lists.lists import medmedcomp
            ranmedmedcomp = random.choice(medmedcomp)
            from cogs.Lists.lists import highmedcomp
            ranhighmedcomp = random.choice(highmedcomp)
            from cogs.Lists.lists import highcomp
            ranhighcomp = random.choice(highcomp)
            from cogs.Lists.lists import worstcomp
            ranworstcomp = random.choice(worstcomp)
            from cogs.Lists.lists import bestcomp

            ranbestcomp = random.choice(bestcomp)
            if rannum == -1:
                embed.add_field(name="‎‎‎‎‎‎‎‎‎‎‎‎‎‎",value=f"{ranworstcomp}",inline=False)
            if -1 < rannum < 11:
                embed.add_field(name="‎‎‎‎‎‎‎‎‎‎‎‎‎‎",value=f"{ranlowcomp}",inline=False)
            if 10 < rannum < 31:
                embed.add_field(name="‎‎‎‎‎‎‎‎‎‎‎‎‎‎",value=f"{ranmedlowcomp}",inline=False)
            if 30 < rannum < 51:
                embed.add_field(name="‎‎‎‎‎‎‎‎‎‎‎‎‎‎", value=f"{ranhighlowcomp}",inline=False)
            if 50 < rannum < 71:
                embed.add_field(name="‎‎‎‎‎‎‎‎‎‎‎‎‎‎",value=f"{ranmedcomp}",inline=False)
            if 70 < rannum < 86:
                embed.add_field(name="‎‎‎‎‎‎‎‎‎‎‎‎‎‎",value=f"{ranmedmedcomp}",inline=False)
            if 85 < rannum < 96:
                embed.add_field(name="‎‎‎‎‎‎‎‎‎‎‎‎‎‎", value=f"{ranhighmedcomp}",inline=False)
            if 95 < rannum < 101:
                embed.add_field(name="‎‎‎‎‎‎‎‎‎‎‎‎‎‎",value=f"{ranhighcomp}",inline=False)
            if rannum == 101:
                embed.add_field(name="‎‎‎‎‎‎‎‎‎‎‎‎‎‎",value=f"{ranbestcomp}",inline=False)

            await ctx.reply(embed=embed)

    #Yeet Command
    @commands.cooldown(1, 5, commands.BucketType.member)
    @commands.command()
    async def yeet(self, ctx, *, message = None):
        if message == None:
            embed = discord.Embed(description="• **.yeet `@USER`\n• Aliases = `.mushyeet`", color=discord.Colour.random())
            embed.set_author(name = "Yeet Usage:",icon_url=ctx.author.avatar_url)
            await ctx.reply(embed=embed)
            self.yeet.reset_cooldown(ctx)
            return
        if "569792736367083560" in message:
            await ctx.send("You cant yeet Mush")
        elif "mush" in message:
            await ctx.send("You cant yeet Mush")
        else:
            embed=discord.Embed(description=f"**{ctx.author.mention} YEETED {message}**", color=discord.Colour.random())
            embed.set_image(url="https://media1.tenor.com/images/3d00d1fe55785a94b80b7139ee539d43/tenor.gif?itemid=16987702")
            await ctx.send(embed=embed)

    #Food Command
    @commands.cooldown(1, 5, commands.BucketType.member)
    @commands.command()
    async def food(self,ctx):
        from cogs.Lists.lists import food
        ranfood = random.choice(food)
        await ctx.reply(f"You should have {ranfood}")

    #Homies Command
    @commands.command()
    async def homies(self, ctx, *, arg1 = None):
        if arg1 == None:
            embed = discord.Embed(title="**Usage:**", description=".homies `@USER`", color=discord.Colour.random())
            await ctx.reply(embed=embed)
            self.homies.reset_cooldown(ctx)
            return
        converted_num = str(ctx.author.id)
        if converted_num in arg1:
            from cogs.Lists.lists import bro
            ranbro = random.choice(bro)
            await ctx.send(ranbro)
        else:
            homie = ["||<a:homiekiss:828386571514151003>||","||<a:homiedance:828386682801750036>||","||<:homieskiss:832501395742523433>||",]
            ranhomie = random.choice(homie)
            await ctx.send(f"**From:** {ctx.author.mention}\n**To:** {arg1}\n{ranhomie}")
            await ctx.message.delete()

    #Salty Command
    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.member)
    async def salty(self,ctx, arg1 = None):
        if arg1 == None:
            embed = discord.Embed(description="• **.salty `@USER`", color=discord.Colour.random())
            embed.set_author(name = "Salty Usage:",icon_url=ctx.author.avatar_url)
            await ctx.reply(embed=embed)
            self.salty.reset_cooldown(ctx)
            return
        salty = ["https://i.pinimg.com/originals/1b/43/2a/1b432a6e88b6db2a387d59ffc1205b20.jpg","https://media1.tenor.com/images/3206c4fa9caf7d068431ddd42d6c6480/tenor.gif?itemid=17584364"]
        ransalt = random.choice(salty)
        embed=discord.Embed(description=f"**This is for you {arg1}**", color=discord.Colour.random())
        embed.set_image(url=f"{ransalt}")
        await ctx.send(embed=embed)

    #Rio/Kith Command
    @commands.command(aliases = ["rio","kiss"])
    @commands.cooldown(1, 15, commands.BucketType.member)
    async def kith(self, ctx, arg1 = None):
        if arg1 == None:
            embed = discord.Embed(description="• **.kith `@USER`\n• Aliases = `.rio`, `.kiss`", color=discord.Colour.random())
            embed.set_author(name = "Kith Usage:",icon_url=ctx.author.avatar_url)
            await ctx.reply(embed=embed)
            self.kith.reset_cooldown(ctx)
            return
        from cogs.Lists.lists import rio
        ranrio = random.choice(rio)
        embed=discord.Embed(description=f"**{ctx.author.mention} GAVE {arg1} A KITH**", color=discord.Colour.random())
        embed.set_image(url=f"{ranrio}")
        await ctx.send(embed=embed)

    #Pat Command
    @commands.command()
    @commands.cooldown(1, 15, commands.BucketType.member)
    async def pat(self, ctx, arg1 = None):
        if arg1 == None:
            embed = discord.Embed(description="• **.pat `@USER`", color=discord.Colour.random())
            embed.set_author(name = "Pat Usage:",icon_url=ctx.author.avatar_url)
            await ctx.reply(embed=embed)
            self.pat.reset_cooldown(ctx)
            return
        from cogs.Lists.lists import pat
        ranpat = random.choice(pat)
        embed=discord.Embed(description=f"**{ctx.author.mention} PAT {arg1}**", color=discord.Colour.random())
        embed.set_image(url=f"{ranpat}")
        await ctx.send(embed=embed)

    #Yumo/Slap Command
    @commands.command(aliases = ["yumo"])
    @commands.cooldown(1, 15, commands.BucketType.member)
    async def slap(self, ctx, arg1 = None):
        if arg1 == None:
            embed = discord.Embed(description="• **.slap `@USER`\n• Aliases = `.yumo`", color=discord.Colour.random())
            embed.set_author(name = "Slap Usage:",icon_url=ctx.author.avatar_url)
            await ctx.reply(embed=embed)
            self.slap.reset_cooldown(ctx)
            return
        from cogs.Lists.lists import slap
        ranslap = random.choice(slap)
        if "569792736367083560" in ctx.message.content:
            await ctx.send("You cant slap Mush")
        elif "mush" in ctx.message.content:
            await ctx.send("You cant slap Mush")
        elif ctx.author.id == 809509445893488650:
            embed=discord.Embed(description=f"**{arg1} got slapped by Yumo just cause \n {ranslap}**", color=discord.Colour.random())
            embed.set_image(url=f"{ranslap}")
            await ctx.send(embed=embed)
        else:
            embed=discord.Embed(description=f"**{ctx.author.mention} SLAPPED {arg1}**", color=discord.Colour.random())
            embed.set_image(url=f"{ranslap}")
            await ctx.send(embed=embed)

    #Charie/Vodka Command
    @commands.command(aliases = ["charie"])
    @commands.cooldown(1, 15, commands.BucketType.member)
    async def vodka(self,ctx):
        elmoburn = "<a:elmoburn1:837809446746193970>"
        embed=discord.Embed(title=f"{elmoburn}{elmoburn}   **PRAISE VODKA**   {elmoburn}{elmoburn}", color=discord.Colour.random())
        embed.set_image(url="https://cdn.discordapp.com/attachments/833141982704304148/857793589873999882/image0.gif")
        await ctx.send(embed=embed)

    #Scribbles/Glock Command
    @commands.command(aliases = ["scribbles"])
    @commands.cooldown(1, 10, commands.BucketType.member)
    async def glock(self, ctx, arg1 = None):
        if arg1 == None:
            embed = discord.Embed(description="• **.glock `@USER`\n• Aliases = `.scribbles`", color=discord.Colour.random())
            embed.set_author(name = "Glock Usage:",icon_url=ctx.author.avatar_url)
            await ctx.reply(embed=embed)
            self.glock.reset_cooldown(ctx)
            return
        if "569792736367083560" in ctx.message.content:
            await ctx.send("You cant glock Mush")
        elif "mush" in ctx.message.content:
            await ctx.send("You cant glock Mush")
        else:
            from cogs.Lists.lists import scribbles
            ranscribbles = random.choice(scribbles)
            embed=discord.Embed(description=f"**{ctx.author.mention} GLOCKED {arg1}**", color=discord.Colour.random())
            embed.set_image(url=f"{ranscribbles}")
            await ctx.send(embed=embed)

    #Shots
    @commands.command()
    @commands.cooldown(1, 15, commands.BucketType.member)
    async def shots(self, ctx):
        from cogs.Lists.lists import shotgifs
        ranshot = random.choice(shotgifs)
        elmoburn = "<a:elmoburn1:837809446746193970>"
        embed=discord.Embed(title=f"{elmoburn}{elmoburn}   **SHOTS**   {elmoburn}{elmoburn}", color=discord.Colour.random())
        embed.set_image(url=ranshot)
        await ctx.send(embed=embed)

    #Calculator
    @commands.command(aliases=["calc"])
    async def calculator(self, ctx):
        embed = discord.Embed(title="**Usage:**", description=".add/sub/mult/div `NUM` `NUM`", color=discord.Colour.random())
        await ctx.reply(embed=embed)
    @commands.command(pass_context=True)
    async def add(self, ctx, a:int, b:int = None):
        if b == None:
            embed = discord.Embed(title="**Usage:**", description=".add/sub/mult/div `NUM` `NUM`", color=discord.Colour.random())
            await ctx.reply(embed=embed)
            return
        await ctx.send(f"The answer is:\n**{a+b}**")
    @commands.command(aliases=["sub"])
    async def subtract(self, ctx, a:int, b:int = None):
        if b == None:
            embed = discord.Embed(title="**Usage:**", description=".add/sub/mult/div `NUM` `NUM`", color=discord.Colour.random())
            await ctx.reply(embed=embed)
            return
        await ctx.send(f"The answer is:\n**{a-b}**")
    @commands.command(aliases=["mult"])
    async def multiply(self, ctx, a:int, b:int = None):
        if b == None:
            embed = discord.Embed(title="**Usage:**", description=".add/sub/mult/div `NUM` `NUM`", color=discord.Colour.random())
            await ctx.reply(embed=embed)
            return
        await ctx.send(f"The answer is:\n**{a*b}**")
    @commands.command(aliases=["div"])
    async def divide(self, ctx, a:int, b:int = None):
        if b == None:
            embed = discord.Embed(title="**Usage:**", description=".add/sub/mult/div `NUM` `NUM`", color=discord.Colour.random())
            await ctx.reply(embed=embed)
            return
        await ctx.send(f"The answer is:\n**{a/b}**")

    #Bite Command
    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.member)
    async def bite(self, ctx, arg1 = None):
        if arg1 == None:
            embed = discord.Embed(description="• **.bite `@USER`", color=discord.Colour.random())
            embed.set_author(name = "Bite Usage:",icon_url=ctx.author.avatar_url)
            await ctx.reply(embed=embed)
            self.bite.reset_cooldown(ctx)
            return
        if "569792736367083560" in ctx.message.content:
            if ctx.author.id == 557976700286140426:
                from cogs.Lists.lists import bite
                ranbite = random.choice(bite)
                embed=discord.Embed(description=f"**{ctx.author.mention} bit {arg1}**", color=discord.Colour.random())
                embed.set_image(url=f"{ranbite}")
                await ctx.send(embed=embed)
                return
            await ctx.send("You cant bite Mush")
        elif "mush" in ctx.message.content:
            await ctx.send("You cant bite Mush")
        else:
            from cogs.Lists.lists import bite
            ranbite = random.choice(bite)
            embed=discord.Embed(description=f"**{ctx.author.mention} bit {arg1}**", color=discord.Colour.random())
            embed.set_image(url=f"{ranbite}")
            await ctx.send(embed=embed)

    #Mush
    @commands.command()
    async def mush(self,ctx):
        if ctx.author.id == 557976700286140426:
            await ctx.reply("Hi Sarah")
            return
        from cogs.Lists.lists import mush
        ranmush = random.choice(mush)
        embed = discord.Embed(color=discord.Colour.random())
        embed.set_image(url=f"{ranmush}")
        await ctx.send(embed=embed)

def setup(client):
    client.add_cog(Mushball(client))
