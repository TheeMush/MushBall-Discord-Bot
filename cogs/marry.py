from pymongo import MongoClient
import discord
from discord.ext import commands
import traceback
import datetime
import random
import asyncio
from cogs.Lists.functions import update_bank

cluster = MongoClient("mongodb+srv://testbot:testbot123@testbot.78blp.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
roles = cluster["discord"]["marriage"]




class marry(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def marry(self,ctx,member: discord.Member = None):
        try:
            if member == None:
                embed = discord.Embed(description="• **.marry** `@USER`", color=0xFF0000)
                embed.set_author(name = "Marry Usage:",icon_url=ctx.author.avatar_url)
                await ctx.reply(embed=embed)
                return

            await self.open_marriage(ctx)

            lol = roles.find({'_id': ctx.guild.id},{'userAccounts'})
            namelist = []
            for x in lol:
                for y in x['userAccounts']:
                    name = list(y.items())[0][1]
                    spouse = list(y.items())[1][1]
                    namelist.append(name)
                    namelist.append(spouse)

            if ctx.author.id in namelist:
                cheating = [
                    f"Hey {ctx.author.mention}, wait until <@{spouse}> hears that you're trying to marry someone else",
                    f"Yooooooo {ctx.author.mention} is trying to cheat on <@{spouse}>",
                    f"Damn {ctx.author.mention}, very bold of you to try to marry someone else when youre married to <@{spouse}>"
                ]
                rancheat = random.choice(cheating)
                spouse = await self.spouse(ctx,ctx.author.id)

                if member.id == spouse:
                    embed = discord.Embed(description=f"Look {ctx.author.mention}, I know you and <@{spouse}> love each other (gross), but you're already married", color=0xFF0000)
                    embed.set_author(name = f"{ctx.author.name}'s Marriage",icon_url=ctx.author.avatar_url)
                    await ctx.reply(embed=embed)
                    return

                embed = discord.Embed(description=f"{rancheat}", color=0xFF0000)
                embed.set_author(name = f"{ctx.author.name} Cheating",icon_url=ctx.author.avatar_url)
                await ctx.reply(embed=embed)
                return

            elif member.id in namelist:
                spouse = await self.spouse(ctx,member.id)

                cheating = [
                    f"Oi {ctx.author.mention} is trying to be a homewrecker and breakup {member.mention} & <@{spouse}>'s marriage",
                    f"{ctx.author.mention} calm down bud, {member.mention} is already happily(?) married to <@{spouse}>",
                    f"Damn {ctx.author.mention}, are you trying to breakup {member.mention} and <@{spouse}>?",
                    f"Yo {ctx.author.mention}, do you want {member.mention} to cheat on <@{spouse}> or something?"
                ]
                rancheat = random.choice(cheating)

                embed = discord.Embed(description=f"{rancheat}", color=0xFF0000)
                embed.set_author(name = f"{ctx.author.name} Homewrecking",icon_url=ctx.author.avatar_url)
                await ctx.reply(embed=embed)
                return
            else:
                proposal = [
                    f"Hey {member.mention}, {ctx.author.mention} is down on one knee trying to marry you,\n\nWhat do you say?",
                    f"Yo {member.mention}, you got {ctx.author.mention} over here down bad tryna marry you,\n\nWhat's your answer?",
                    f"Damn {ctx.author.mention} you simping this hard? Hey {member.mention},\n\nCome marry this idiot?",
                    f"Aw this cute or whatever I guess. Hey {member.mention}, {ctx.author.mention} tryna hold you down for life,\n\nWhat you think?"
                ]
                ranpropose = random.choice(proposal)

                embed = discord.Embed(description = ranpropose,  color=discord.Colour.random())
                embed.set_author(name = f"{ctx.author.name} Proposing To {member.name}",icon_url=ctx.author.avatar_url)
                embed.set_image(url="https://cdn.discordapp.com/emojis/755954990572372018.png?v=1")
                embed.set_footer(text="React with your answer")
                buttons = [u"\U0001f44d",u"\U0001F44E"] 

                msg = await ctx.send(embed=embed)
                
                for button in buttons:
                    await msg.add_reaction(button)

                try:
                    reaction, user = await self.client.wait_for("reaction_add", check=lambda reaction, user: user == member and reaction.emoji in buttons, timeout=60.0)

                except asyncio.TimeoutError:
                    await ctx.reply(f"Damn {ctx.author.mention}, you ain't get a reply in time. Try again later maybe?")
                    return

                if reaction.emoji == u"\U0001f44d":
                    currenttime = datetime.datetime.now().replace(microsecond=0)
                    newaccountlist = {'id':ctx.author.id,'spouse': member.id,'time':currenttime}
                    roles.update({'_id': ctx.guild.id}, {'$push': {'userAccounts': newaccountlist}})

                    embed = discord.Embed(description=f"By the power vested in me by some sketchy guy Mush found on craigslist,\nI now pronounce {ctx.author.mention} and {member.mention} married! ", color=0xFF0000)
                    embed.set_author(name = f"{ctx.author.name} and {member.name}'s Wedding",icon_url=self.client.user.avatar_url)
                    await ctx.send(embed=embed)
                elif reaction.emoji == u"\U0001F44E":
                    await ctx.send(f"Oooooooooooof sorry {ctx.author.mention} they said no, thats gotta be rough lol. Sucks to suck fr, couldn't be me")
        except:
            print(f"```{traceback.format_exc()}```")

    #Marry ERROR HANDLING
    @marry.error
    async def marry_error(self,ctx, error):
        if isinstance(error, commands.MemberNotFound):
            embed = discord.Embed(description = "Be sure to @ mention someone",  color=0xFF0000)
            embed.set_author(name='ERROR:',icon_url=self.client.user.avatar_url)
            await ctx.reply(embed=embed)
        else:
            print(error)

    @commands.command()
    async def divorce(self,ctx):
        spouse = await self.spouse(ctx,ctx.author.id)

        if spouse == None:
            embed = discord.Embed(description=f"Yo {ctx.author.mention}, did you forget you're lonely or something? You're not married to anyone")
            await ctx.send(embed=embed)
            return

        buttons = [u"\U0001f44d",u"\U0001F44E"] 

        embed = discord.Embed(description = "You sure you wanna do this? It's pretty expensive",  color=discord.Colour.random())
        msg = await ctx.send(embed=embed)
        
        for button in buttons:
            await msg.add_reaction(button)

        try:
            reaction, user = await self.client.wait_for("reaction_add", check=lambda reaction, user: user == ctx.author and reaction.emoji in buttons, timeout=60.0)

        except asyncio.TimeoutError:
            await ctx.reply(f"You didnt make a choice fast enough!")
            return

        if reaction.emoji == u"\U0001f44d":
            bal = await update_bank(ctx,ctx.author.id,0,0)
            if bal[0] < 50000:
                embed = discord.Embed(description="You need atleast $50,000 to get divorced", color=0xFF0000)
                embed.set_author(name ="Divorce",icon_url=ctx.author.avatar_url)
                await ctx.reply(embed=embed)
                return

            await update_bank(ctx,ctx.author.id,-50000,0)
            roles.update({'_id': ctx.guild.id}, {'$pull': { 'userAccounts': {'id': ctx.author.id} }})
            roles.update({'_id': ctx.guild.id}, {'$pull': { 'userAccounts': {'id': spouse} }})


            embed = discord.Embed(description=f"You hate to see it but {ctx.author.mention} & <@{spouse}> got divorced")
            embed.set_author(name ="Divorce",icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)

    @commands.command(aliases = ['status','stat'])
    async def stats(self,ctx,member:discord.Member = None):
        try:
            if member == None:
                spouse = await self.spouse(ctx,ctx.author.id)

                if spouse == None:
                    embed = discord.Embed(description=f"Yo {ctx.author.mention}, did you forget you're lonely or something? You're not married to anyone")
                    embed.set_author(name='MushBall Marriages',icon_url=self.client.user.avatar_url)
                    await ctx.send(embed=embed)
                    return
                
                time = await self.time(ctx,ctx.author.id)
                current = datetime.datetime.now().replace(microsecond=0)
                timepassed = (current-time)
                embed = discord.Embed(description=f"{ctx.author.mention} is married to <@{spouse}>\n\n They've been married for `{timepassed}`\n\nThey got married on:\n`{time}`", color=discord.Colour.random())
                embed.set_author(name='MushBall Marriages',icon_url=self.client.user.avatar_url)
                await ctx.send(embed=embed)
            else:
                spouse = await self.spouse(ctx,member.id)

                if spouse == None:
                    embed = discord.Embed(description=f"{member.mention} is lonely and not married to anyone lol")
                    embed.set_author(name='MushBall Marriages',icon_url=self.client.user.avatar_url)
                    await ctx.send(embed=embed)
                    return

                time = await self.time(ctx,ctx.member.id)
                current = datetime.datetime.now().replace(microsecond=0)
                timepassed = (current-time)
                embed = discord.Embed(description=f"{member.mention} is married to <@{spouse}>\n\n They've been married for `{timepassed}`\n\nThey got married on:\n`{time}`", color=discord.Colour.random())
                embed.set_author(name='MushBall Marriages',icon_url=self.client.user.avatar_url)
                await ctx.send(embed=embed)
        except:
            print(f"```{traceback.format_exc()}```")
            
    #Marry ERROR HANDLING
    @stats.error
    async def stats_error(self,ctx, error):
        if isinstance(error, commands.MemberNotFound):
            embed = discord.Embed(description = "Be sure to @ mention someone if you wanna see their stats",  color=0xFF0000)
            embed.set_author(name='ERROR:',icon_url=self.client.user.avatar_url)
            await ctx.reply(embed=embed)
        else:
            print(error)    


        

    #~~~~~~~~~~FUNCTIONS~~~~~~~~~~#
    async def open_marriage(self,ctx):
        check = roles.find({})
        serverlist = []
        for x in check:
            serverlist.append(x.get('_id'))

        if ctx.guild.id in serverlist:
            yon = True

        else:
            yon = False

        if yon == False:
            newshop = {"_id" : ctx.guild.id}
            roles.insert_one(newshop)
            newrolelist = {'id':'** **','spouse': '** **','time':'** **'}
            roles.update({'_id': ctx.guild.id}, {'$push': {'userAccounts': newrolelist}})

    async def spouse(self,ctx,userid):
        await self.open_marriage(ctx)
        lol = roles.find({'_id': ctx.guild.id},{'userAccounts'})
        for x in lol:
            for y in x['userAccounts']:
                name = list(y.items())[0][1]
                spouseid = list(y.items())[1][1]
                spouse = None
                if name == userid:
                    spouse = spouseid
                    return spouse
                elif spouseid == userid:
                    spouse = name
                    return spouse
        return spouse
                
    async def time(self,ctx,userid):
        await self.open_marriage(ctx)
        lol = roles.find({'_id': ctx.guild.id},{'userAccounts'})
        for x in lol:
            for y in x['userAccounts']:
                name = list(y.items())[0][1]
                spouseid = list(y.items())[1][1]
                time = list(y.items())[2][1]
                if name == userid:
                    return time
                elif spouseid == userid:
                    return time
    #~~~~~~~~~~FUNCTIONS~~~~~~~~~~#

def setup(client):
    client.add_cog(marry(client))