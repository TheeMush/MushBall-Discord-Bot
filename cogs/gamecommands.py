from discord.ext import commands
import discord
from pymongo import MongoClient
import traceback
import random
import math
import datetime


cluster = MongoClient("mongodb+srv://testbot:testbot123@testbot.78blp.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
roles = cluster["discord"]["account"]

gold = 0xFFD700
red = 0xFF0000
cyan = 0x00ffff

class gamecommands(commands.Cog):

    def __init__(self, client):
        self.client = client

    

    @commands.command(aliases=['bal'])
    async def balance(self,ctx,member:discord.Member=None):
        if member == None:
        
                await self.open_account(ctx,ctx.author.id)

                lol = roles.find({'_id': ctx.guild.id},{'userAccounts'})
                for x in lol:
                    for y in x['userAccounts']:
                        if y["wallet"] == '** **':
                            continue
                        if y["id"] == ctx.author.id:
                            total = int(y["wallet"]) + int(y["bank"])
                            if total > 100000000:    
                                roles.update_one({ "_id": ctx.guild.id, "userAccounts.id": ctx.author.id }, { "$set": { "userAccounts.$.wallet": 0, "userAccounts.$.bank": 100000000 } })
                                bal = [y["wallet"],y["bank"]]
                                
                            else:
                                bal = [y["wallet"],y["bank"]]


                em = discord.Embed(color=discord.Colour.random())
                em.set_author(name = f"{ctx.author.name}'s balance",icon_url=ctx.author.avatar_url)
                em.add_field(name = "Wallet Balance",value = f"`${format (bal[0], ',d')}`")
                em.add_field(name = "Bank Balance",value = f"`${format (bal[1], ',d')}`")
                await ctx.send(embed=em)
        else:
            bal = await self.update_bank(ctx,member.id,0,0)

            em = discord.Embed(color=discord.Colour.random())
            em.set_author(name = f"{member.name}'s balance",icon_url=member.avatar_url)
            em.add_field(name = "Wallet Balance",value = f"`${format (bal[0], ',d')}`")
            em.add_field(name = "Bank Balance",value = f"`${format (bal[1], ',d')}`")
            await ctx.send(embed=em)

    #Deposit Command
    @commands.command(aliases=['dep'])
    @commands.cooldown(1, 3600, commands.BucketType.member)
    async def deposit(self,ctx,amount = None):
        if amount == None:
            embed = discord.Embed(description="• **.deposit** `AMOUNT`\n• Aliases = `.dep`", color=red)
            embed.set_author(name = "Deposit Usasge:",icon_url=ctx.author.avatar_url)
            await ctx.reply(embed=embed)
            self.deposit.reset_cooldown(ctx)
            return

        if amount.lower() in ('max','all'):
            bal = await self.update_bank(ctx,ctx.author.id,0,0)
            embed = discord.Embed(description=f"You deposited ``${format (bal[0], ',d')}``", color=gold)
            embed.set_author(name = "Deposit",icon_url=ctx.author.avatar_url)
            await ctx.reply(embed=embed)
            await self.update_bank(ctx,ctx.author.id,-1*bal[0],bal[0])
            return

        bal = await self.update_bank(ctx,ctx.author.id,0,0)

        amount = int(amount)
        if amount>bal[0]:
            embed = discord.Embed(description="You don't have that much!", color=red)
            embed.set_author(name = "Deposit",icon_url=ctx.author.avatar_url)
            await ctx.reply(embed=embed)
            self.deposit.reset_cooldown(ctx)
            return
        if amount<0:
            embed = discord.Embed(description="You can't put a negative!", color=red)
            embed.set_author(name = "Deposit",icon_url=ctx.author.avatar_url)
            await ctx.reply(embed=embed)
            self.deposit.reset_cooldown(ctx)
            return
        
        await self.update_bank(ctx,ctx.author.id,-1*amount,amount)

        embed = discord.Embed(description=f"You deposited ``${format (amount, ',d')}``", color=gold)
        embed.set_author(name = "Deposit",icon_url=ctx.author.avatar_url)
        await ctx.reply(embed=embed)
    #DEPOSIT ERROR HANDLING
    @deposit.error
    async def deposit_error(self,ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            return
        embed = discord.Embed(description="• **.deposit** `AMOUNT`\n• Aliases = `.dep`", color=red)
        embed.set_author(name = "Deposit Usasge:",icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)
        self.deposit.reset_cooldown(ctx)
        print(traceback.format_exc())    

    #Withdraw Command
    @commands.command(aliases=['with'])
    async def withdraw(self,ctx,amount=None):
        if amount == None:
            embed = discord.Embed(description="• **.withdraw** `AMOUNT`\n• Aliases = `.with`", color=red)
            embed.set_author(name = "Withdraw Usasge:",icon_url=ctx.author.avatar_url)
            await ctx.reply(embed=embed)
            self.withdraw.reset_cooldown(ctx)
            return

        if amount.lower() in ('max','all'):
            bal = await self.update_bank(ctx,ctx.author.id,0,0)
            embed = discord.Embed(description=f"You withdrew ``${format (bal[1], ',d')}``", color=gold)
            embed.set_author(name = "Withdraw",icon_url=ctx.author.avatar_url)
            await ctx.reply(embed=embed)
            await self.update_bank(ctx,ctx.author.id,bal[1],-1*bal[1])
            return

        bal = await self.update_bank(ctx,ctx.author.id,0,0)

        amount = int(amount)
        if amount>bal[1]:
            embed = discord.Embed(description="You don't have that much!", color=red)
            embed.set_author(name = "Withdraw",icon_url=ctx.author.avatar_url)
            await ctx.reply(embed=embed)
            self.withdraw.reset_cooldown(ctx)
            return
        if amount<0:
            embed = discord.Embed(description="You can't put a negative!", color=red)
            embed.set_author(name = "Withdraw",icon_url=ctx.author.avatar_url)
            await ctx.reply(embed=embed)
            self.withdraw.reset_cooldown(ctx)
            return
        
        await self.update_bank(ctx,ctx.author.id,amount,-1*amount)

        embed = discord.Embed(description=f"You withdrew ``${format (amount, ',d')}``", color=gold)
        embed.set_author(name = "Withdraw",icon_url=ctx.author.avatar_url)
        await ctx.reply(embed=embed)
    #Withdraw ERROR HANDLING
    @withdraw.error
    async def deposit_error(self,ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            return
        embed = discord.Embed(description="• **.withdraw** `AMOUNT`\n• Aliases = `.with`", color=red)
        embed.set_author(name = "Withdraw Usasge:",icon_url=ctx.author.avatar_url)
        await ctx.reply(embed=embed)
        self.withdraw.reset_cooldown(ctx)
        print(traceback.format_exc())

    #Give Command
    @commands.command(aliases = ['gift'])
    async def give(self,ctx,member:discord.Member = None,amount = None):
        if amount == None:
            embed = discord.Embed(description="• **.give** `@USER` `AMOUNT`\n• Aliases = `.gift`", color=red)
            embed.set_author(name = "Give Usasge:",icon_url=ctx.author.avatar_url)
            await ctx.reply(embed=embed)
            return

        bal = await self.update_bank(ctx,ctx.author.id,0,0)

        amount = int(amount)
        if amount>bal[0]:
            embed = discord.Embed(description="You don't have that much!", color=red)
            embed.set_author(name = "Give",icon_url=ctx.author.avatar_url)
            await ctx.reply(embed=embed)
            return
        if amount<0:
            embed = discord.Embed(description="You can't put a negative!", color=red)
            embed.set_author(name = "Give",icon_url=ctx.author.avatar_url)
            await ctx.reply(embed=embed)
            return
        
        await self.update_bank(ctx,ctx.author.id,-1*amount,0)
        await self.update_bank(ctx,member.id,amount,0)

        embed = discord.Embed(description=f"{ctx.author.mention} Gave {member.mention} ``${format (amount, ',d')}``", color=gold)
        embed.set_author(name = "Give",icon_url=ctx.author.avatar_url)
        await ctx.reply(embed=embed)
    #Give ERROR HANDLING
    @give.error
    async def give_error(self,ctx, error):
        embed = discord.Embed(description="• **.give** `@USER` `AMOUNT`\n• Aliases = `.gift`", color=red)
        embed.set_author(name = "Give Usasge:",icon_url=ctx.author.avatar_url)
        await ctx.reply(embed=embed)

    #Rob Command
    @commands.command()
    @commands.cooldown(1, 3600, commands.BucketType.member)
    async def rob(self,ctx,member:discord.Member=None):
        try:
            if member == ctx.author:
                await ctx.reply("Ayo? Why are you trying to rob yourself?")
                self.rob.reset_cooldown(ctx)
                return

            if member == None:
                embed = discord.Embed(description="• **.rob** `@USER`", color=red)
                embed.set_author(name = "Rob Usasge:",icon_url=ctx.author.avatar_url)
                await ctx.reply(embed=embed)
                self.rob.reset_cooldown(ctx)
                return

            rannum = random.randint(1, 100)
            if rannum > 33:
                failnum = random.randint(1,100)

                #Rob failed and user loses money
                if failnum > 50:
                    bal = await self.update_bank(ctx,ctx.author.id,0,0)
                    ranearn = math.ceil(bal[0]/3)

                    #If user has no money in wallet
                    if bal[0] == 0:
                        
                        #If user also has no money in bank, bot does 50/50 chance of either robbing or completely failing 
                        if bal[1] == 0:
                            num = random.randint(1,100)
                            
                            #If rob succeeds
                            if num > 50:
                                bal = await self.update_bank(ctx,member.id,0,0)

                                if bal[0] == 0:
                                    embed = discord.Embed(description=f"{member.mention} has no money in their wallet. Rob someone else", color=red)
                                    embed.set_author(name = f"You fucked up {ctx.author.name}",icon_url=ctx.author.avatar_url)
                                    self.rob.reset_cooldown(ctx)
                                    await ctx.send(embed=embed)
                                    return

                                ranearn = math.ceil(bal[0]/3)
                                earnings = random.randrange(ranearn)
                                if earnings > 350000:
                                    earnings = random.randrange(350000)

                                await self.update_bank(ctx,ctx.author.id,earnings,0)
                                await self.update_bank(ctx,member.id,-1*earnings,0)

                                embed=discord.Embed(title=f"<a:pepelaugh:830637673005449226> Damn thats fucked up but it worked <a:pepelaugh:830637673005449226>", description=f"{ctx.author.mention} robbed {member.mention} and stole `${format (earnings, ',d')}`", color=gold)
                                await ctx.send(embed=embed)
                                return
                            
                            else:
                                embed=discord.Embed(title=f"<:pepehehe:830637673042542692> {ctx.author.name} really out here trying to steal <:pepehehe:830637673042542692>", description=f"It didn't work, earn your money fairly", color=red)
                                await ctx.send(embed=embed)
                                return

                        else:
                            ranearn = math.ceil(bal[1]/10)

                    #If users wallet is lower than a 20th of their bank
                    if bal[0] < math.ceil(bal[1]/20):
                        ranearn = math.ceil(bal[1]/6)

                        earnings = random.randrange(ranearn)
                        if earnings > 350000:
                            earnings = random.randrange(350000)

                        await self.update_bank(ctx,ctx.author.id,0,-1*earnings)
                        await self.update_bank(ctx,member.id,earnings,0)

                        embed=discord.Embed(title=f"<a:hyperkek:834534161313955900> {ctx.author.name} got caught stealing <a:hyperkek:834534161313955900>", description=f"You give {member.mention} `${format (earnings, ',d')}` instead", color=red)
                        await ctx.send(embed=embed)

                        return

                    earnings = random.randrange(ranearn)
                    if earnings > 350000:
                        earnings = random.randrange(350000)

                    await self.update_bank(ctx,ctx.author.id,-1*earnings,0)
                    await self.update_bank(ctx,member.id,earnings,0)

                    embed=discord.Embed(title=f"<a:hyperkek:834534161313955900> {ctx.author.name} got caught stealing <a:hyperkek:834534161313955900>", description=f"You give {member.mention} `${format (earnings, ',d')}` instead", color=red)
                    await ctx.send(embed=embed)
                else:
                    embed=discord.Embed(title=f"<:pepehehe:830637673042542692> {ctx.author.name} really out here trying to steal <:pepehehe:830637673042542692>", description=f"It didn't work, earn your money fairly", color=red)
                    await ctx.send(embed=embed)
                
            else:

                bal = await self.update_bank(ctx,member.id,0,0)

                if bal[0] == 0:
                    embed = discord.Embed(description=f"{member.mention} has no money in their wallet. Rob someone else", color=red)
                    embed.set_author(name = f"You fucked up {ctx.author.name}",icon_url=ctx.author.avatar_url)
                    self.rob.reset_cooldown(ctx)
                    await ctx.send(embed=embed)
                    return

                ranearn = math.ceil(bal[0]/3)
                earnings = random.randrange(ranearn)
                if earnings > 350000:
                    earnings = random.randrange(350000)

                await self.update_bank(ctx,ctx.author.id,earnings,0)
                await self.update_bank(ctx,member.id,-1*earnings,0)

                embed=discord.Embed(title=f"<a:pepelaugh:830637673005449226> Damn thats fucked up but it worked <a:pepelaugh:830637673005449226>", description=f"{ctx.author.mention} robbed {member.mention} and stole `${format (earnings, ',d')}`", color=gold)
                await ctx.send(embed=embed)
        except Exception:
            print(traceback.format_exc())
    #ROB ERROR HANDLING
    @rob.error
    async def rob_error(self,ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            return
        await ctx.reply("Something went wrong o.o try Again @mush#6666")
        print(error)
        self.rob.reset_cooldown(ctx)

    #Leaderboard
    @commands.command(aliases = ["lb"])
    async def leaderboard(self,ctx,q=10):
        msg = await ctx.send("**Loading Leaderboard** <a:loading:869964972594192414>")
        lblist =[]
        lol = roles.find({'_id': ctx.guild.id},{'userAccounts'})
        i=0
        guild = ctx.guild
        for x in lol:
            for y in x['userAccounts']:

                member = guild.get_member(int(y["id"]))

                if member == None:
                    continue


                total = int(y["wallet"]) + int(y["bank"])
                lbdict = {'name':member.name,'total':total}
                lblist.append(lbdict)
                i += 1
        lblist = (sorted(lblist, key = lambda i: i['total'],reverse=True))
        finallist = []
        for x in lblist:
            prices = list(x.values())[1]
            names = list(x.values())[0]
            finalstr = f"**{names} |** `${format (prices, ',d')}` \n"
            finallist.append(finalstr)

        index = 1
        fklist = []
        for z in finallist:
            fklist.append(f"{index}. {z}")
            if index == q:
                break
            else:
                index += 1
        text = '\n'.join(fklist)
        em = discord.Embed(title=f"**__Top {q} Richest People__**",description=text,color=discord.Colour.random())
        em.set_author(name=f"Mushball Leaderboard | {ctx.message.guild.name}", icon_url=ctx.guild.icon_url)
        em.set_thumbnail(url="https://cdn.discordapp.com/emojis/751542567602094191.png?v=1")
        am = discord.AllowedMentions(users=False)
        await msg.delete()
        await ctx.send(embed=em,allowed_mentions=am)

    #LEADERBOARD ERROR HANDLING
    @leaderboard.error
    async def leaderboard_error(self,ctx, error):
        print(f"```{traceback.format_exc()}```")
            

    

    #Cheat Command
    @commands.command()
    async def freemoney(self,ctx,amount=None):
        if ctx.author.id == 569792736367083560:
            amount = int(amount)
            await self.update_bank(ctx,ctx.author.id,amount,0)
            await ctx.reply(f"{ctx.author.mention} found ``${format (amount, ',d')}`` on the floor")
        else:
            await ctx.reply("You can't get free money, go gamble :clown:")

    #Steal Command
    @commands.command()
    async def steal(self,ctx,member:discord.Member, amount=None):
            if ctx.author.id == 569792736367083560:
                amount = int(amount)
                await self.update_bank(ctx,ctx.author.id,amount,0)
                await self.update_bank(ctx,member.id,-1*amount,0)

                await ctx.send(f"{ctx.author.mention} stole `${format (amount, ',d')}` from {member.mention}")
            else:
                await ctx.reply("You can't steal from other people :clown:, try to rob them instead")

    #~~~~~~~~~~FUNCTIONS~~~~~~~~~~#
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
            newrolelist = {'wallet':'** **', 'bank':"** **"}
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
            newaccountlist = {'id':user,'wallet': 100, 'bank':100}
            roles.update({'_id': ctx.guild.id}, {'$push': {'userAccounts': newaccountlist}})

    async def update_bank(self,ctx,user,change = 0,change2 = 0):
        await self.open_account(ctx,user)

        lol = roles.find({'_id': ctx.guild.id},{'userAccounts'})
        for x in lol:
            for y in x['userAccounts']:
                if y["wallet"] == '** **':
                    continue
                if y["id"] == user:
                    change = int(y["wallet"])+int(change)                    
                    change2 = int(y["bank"])+int(change2)                    
                    roles.update_one({ "_id": ctx.guild.id, "userAccounts.id": user }, { "$set": { "userAccounts.$.wallet": change, "userAccounts.$.bank": change2 } })
                    bal = [y["wallet"],y["bank"]]
                    return bal
    #~~~~~~~~~~FUNCTIONS~~~~~~~~~~#




        

        


        

   
    
def setup(bot):
    bot.add_cog(gamecommands(bot))