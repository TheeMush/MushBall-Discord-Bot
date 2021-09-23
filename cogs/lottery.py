import discord
from discord.ext import commands
from pymongo import MongoClient
import traceback
import random
import asyncio
import math
from cogs.Lists.functions import update_bank

cluster = MongoClient("mongodb+srv://testbot:testbot123@testbot.78blp.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
roles = cluster["discord"]["lotto"]
money = cluster["discord"]["account"]


class lottery(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['lotto'])
    @commands.cooldown(1, 86400, commands.BucketType.member)
    async def lottery(self,ctx):
        try:
            pool = await self.open_list(ctx)
            bal = await update_bank(ctx,ctx.author.id,0,0)

            slots = "<a:slots:847746097711677461> <a:slots:847746097711677461> <a:slots:847746097711677461>"
            embed = discord.Embed(title=f"{slots} MushBall's Lottery {slots}", color=discord.Colour.random())
            embed.add_field(name="**Current Pool:**",value=f"`${format (pool, ',d')}`",inline=True)
            embed.add_field(name="Total Balance:",value=f"`${format ((bal[0]+bal[1]), ',d')}`",inline=True)
            embed.set_footer(text="Playing the lottery takes $25,000!")
            buttons = ['\u2705',"\u274C"] 

            msg = await ctx.send(embed=embed)     
            for button in buttons:
                await msg.add_reaction(button)

            try:
                reaction, user = await self.client.wait_for("reaction_add", check=lambda reaction, user: user == ctx.author and reaction.emoji in buttons, timeout=60.0)

            except asyncio.TimeoutError:
                embed.add_field(name="\nYou didn't reply fast enough!",value="** **",inline=False)
                await msg.clear_reactions()
                await msg.edit(embed=embed)
                self.lottery.reset_cooldown(ctx)
                return

            if reaction.emoji == "\u2705":
                if bal[0] < 25000:
                    embed.add_field(name="\nYou need to have a $25,000 to play the lottery idiot",value="** **",inline=False)
                    embed.set_footer(text="Go gamble more broke ass")  
                    await msg.clear_reactions()
                    await msg.edit(embed=embed)
                    self.lottery.reset_cooldown(ctx)
                    return

                embed = discord.Embed(title=f"{slots} MushBall's Lottery {slots}",description=f"**Let's see if {ctx.author.mention} Won...**", color=discord.Colour.random())
                embed.set_author(name="Lottery Results", icon_url=ctx.author.avatar_url)
                await msg.clear_reactions()
                await msg.edit(embed=embed)
                await asyncio.sleep(2.5)

                rannum = random.randint(1, 200)

                if rannum == 66:
                    embed = discord.Embed(title=f"{slots} MushBall's Lottery {slots}",description=f"**{ctx.author.mention} You WON!!!!**", color=discord.Colour.random())
                    embed.set_thumbnail(url=ctx.author.avatar_url)
                    embed.set_footer(text="Lemme get some money")

                    roles.update_one({ "_id": ctx.guild.id, "lottopool.pool": int(pool) }, { "$set": {"lottopool.$.pool": 10000000}})
                    await update_bank(ctx,ctx.author.id,0,pool)
                    await msg.edit(embed=embed)
                else:
                    embed = discord.Embed(title=f"{slots} MushBall's Lottery {slots}",description=f"**Sorry {ctx.author.mention} You Lost**", color=discord.Colour.random())
                    embed.set_author(name="Lottery Results", icon_url=ctx.author.avatar_url)
                    embed.set_footer(text="Sucks to suck huh")
                    change = int(pool) + 25000
                    roles.update_one({ "_id": ctx.guild.id, "lottopool.pool": int(pool) }, { "$set": {"lottopool.$.pool": change}})
                    await update_bank(ctx,ctx.author.id,-25000,0)
                    await msg.edit(embed=embed)

            else:
                embed.add_field(name="\nCancelled",value="** **",inline=False)
                await msg.clear_reactions()
                await msg.edit(embed=embed)
                self.lottery.reset_cooldown(ctx)


        except:
            print(f"```{traceback.format_exc()}```")

    
    async def open_list(self,ctx):
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
            newaccountlist = {'pool':10000000}
            roles.update({'_id': ctx.guild.id}, {'$push': {'lottopool': newaccountlist}})

        lol = roles.find({'_id': ctx.guild.id},{'lottopool'})
        for x in lol:
            for y in x['lottopool']:
                pool = y["pool"]
        
        return pool

   
    
def setup(bot):
    bot.add_cog(lottery(bot))