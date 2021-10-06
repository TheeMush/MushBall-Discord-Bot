import discord
import datetime
from pymongo import MongoClient
from discord.ext import commands
from cogs.Lists.functions import update_bank
import traceback

cluster = MongoClient("mongodb+srv://testbot:testbot123@testbot.78blp.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
roles = cluster["discord"]["daily"]


class daily(commands.Cog):

    def __init__(self, client):
        self.client = client

    async def cog_check(self, ctx):
        if ctx.channel.id == 766731745542275113:
            await ctx.send("Use your daily in the MushBall channel dumbass")
            return
        else:
            return True

    @commands.command()
    async def daily(self,ctx):
        try:
            idlist = []
            lol = roles.find({'_id': ctx.guild.id},{'userAccounts'})
            for x in lol:
                for y in x['userAccounts']:
                    if y["time"] == '** **':
                        continue
                    idlist.append(y['id'])
                    if y["id"] == ctx.author.id:
                        lastused = y['time']
                        break
            
            if ctx.author.id in idlist:
                past = datetime.datetime.strptime(lastused, '%Y-%m-%d %H:%M:%S')
                current = datetime.datetime.now().replace(microsecond=0)
                difference = (current-past).total_seconds()
                
                if difference < 86400:
                    cooldowntime = 86400 - difference
                    cooldowntime = datetime.timedelta(seconds=cooldowntime)
                    await ctx.reply(f"<a:hourglass:857868080435560520> **| Cooldown:** **{cooldowntime}**")
                    
                else:
                    await self.update_daily(ctx,ctx.author.id)
                    embed = discord.Embed(description = f":money_with_wings: | You got your daily `$10,000`",color=discord.Colour.random())
                    embed.set_author(name = "Daily",icon_url=ctx.author.avatar_url)
                    await ctx.send(embed=embed)
                    await update_bank(ctx,ctx.author.id,10000,0)
                    await self.update_daily(ctx,ctx.author.id)
            else:
                embed = discord.Embed(description = f":money_with_wings: | You got your daily `$10,000`",color=discord.Colour.random())
                embed.set_author(name = "Daily",icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embed)
                await update_bank(ctx,ctx.author.id,10000,0)
                await self.update_daily(ctx,ctx.author.id)
                return

        except:
            print(f"```{traceback.format_exc()}```")
            
    #~~~~~~~~~~FUNCTIONS~~~~~~~~~~$
    async def open_account(self,ctx,user):
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
            newrolelist = {'time':'** **'}
            roles.update({'_id': ctx.guild.id}, {'$push': {'userAccounts': newrolelist}})

        lol = roles.find({'_id': ctx.guild.id},{'userAccounts'})
        namelist = []
        for x in lol:
            for y in x['userAccounts']:
                name = list(y.items())[0][1]
                namelist.append(name)
        if user in namelist:
            return
        else:
            time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            newaccountlist = {'id':user,'time': time}
            roles.update({'_id': ctx.guild.id}, {'$push': {'userAccounts': newaccountlist}})

    async def update_daily(self,ctx,user):
        await self.open_account(ctx,user)

        lol = roles.find({'_id': ctx.guild.id},{'userAccounts'})
        for x in lol:
            for y in x['userAccounts']:
                if y["time"] == '** **':
                    continue
                if y["id"] == user:  
                    time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")              
                    roles.update_one({ "_id": ctx.guild.id, "userAccounts.id": user }, { "$set": { "userAccounts.$.time": time}})
                    
    #~~~~~~~~~~FUNCTIONS END~~~~~~~~~~#

def setup(client):
    client.add_cog(daily(client))