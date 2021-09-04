import discord
from discord.ext import commands
from discord.message import Message
from pymongo import MongoClient
import traceback
import datetime
import random
import time
intents = discord.Intents.default()
intents.members = True

cluster = MongoClient("mongodb+srv://testbot:testbot123@testbot.78blp.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
roles = cluster["discord"]["afk"]

class afk(commands.Cog):
    try:
        def __init__(self, client):
            self.client = client

        global namelist
        namelist = [] 

        


        @commands.command()
        async def afk(self,ctx,message = None):
            try:
                if message == None:
                    message = None
                else:
                    message = ctx.message.content.split(' ', 1)[1]
                
                await self.update_list(ctx.guild.id)
                global namelist
                for x in namelist:
                    if x == ctx.author.id:
                        await self.off_afk(ctx,ctx.author.id)
                        await self.update_list(ctx.guild.id)
                        return

                await self.update_afk(ctx,ctx.author.id,message)
            except Exception:
                print(traceback.format_exc()) 
                
        @commands.Cog.listener()
        async def on_message(self, message):
            try:
                
                await self.update_list(message.guild.id)
                if message.author.id != self.client.user.id:
                    yuh = message.mentions

                    #Checks if message is a reply or contains a mention
                    #This runs instantly
                    if not yuh:
                        #Checks if author was AFK. If yes, takes off AFK
                        await self.update_list(message.guild.id)
                        global namelist
                        for x in namelist:
                            if x == message.author.id:
                                if '.afk' in message.content:
                                    await self.update_list(message.guild.id)
                                else:
                                    await self.off_afk(message,message.author.id)
                                    await self.update_list(message.guild.id)
                        
                        return

                    else:
                        lol = roles.find({'_id': message.guild.id},{'userAccounts'})
                        namelist = []
                        userid = None

                        #Checks if author was AFK. If yes, takes off AFK
                        await self.update_list(message.guild.id)
                        for x in namelist:
                            if x == message.author.id:
                                if '.afk' in message.content:
                                    pass
                                else:
                                    await self.off_afk(message,message.author.id)

                        #Loops through DB and appends all AFK users names to 'namelist'
                        for x in lol:
                            for y in x['userAccounts']:
                                name = list(y.items())[0][1]
                                msg = list(y.items())[1][1]
                                time = list(y.items())[2][1]
                                namelist.append(name)
                                
                                #Checks if user was mentioned in message
                                if str(name) in message.content:
                                    userid = name
                                    afkmsg = msg
                                    timeused = time
                                    break
                                else:
                                    userid = None

                                if yuh:
                                    for x in yuh:
                                        repliedtoauthor = x
                                        break

                                    if name == repliedtoauthor.id:
                                        userid = name
                                        afkmsg = msg
                                        timeused = time
                                        break
                        
                        #User was found in AFK List(namelist) sends out AFK message                
                        if userid != None:
                            afkuser = await message.guild.fetch_member(int(name))

                            dt = datetime.datetime.strptime(str(timeused), "%Y-%m-%d %H:%M:%S")
                            newdt = datetime.datetime.strftime(dt, "%b %d %y %H:%M")

                            if afkmsg == None:
                                embed = discord.Embed(color=discord.Colour.random())
                            else:
                                embed = discord.Embed(description=afkmsg,color=discord.Colour.random())

                            embed.set_author(name=f"{afkuser.name} is AFK", icon_url=afkuser.avatar_url)
                            embed.set_footer(text=newdt)
                            await message.reply(embed=embed)

                        

                        #print(f"whole command {message.author.name } {datetime.datetime.now() - begin_time}")

                        await self.update_list(message.guild.id)
                        


            except:
                print(f"```{traceback.format_exc()}```")
                

        

        async def update_list(self,guildid):
            global namelist
            namelist.clear()
            lol = roles.find({'_id': guildid},{'userAccounts'})
            for x in lol:
                for y in x['userAccounts']:
                    name = list(y.items())[0][1]
                    namelist.append(name)

        try:
            async def open_list(self,ctx,userid,message):
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
                    newrolelist = {'userid':'** **', 'afkMessage':"** **",'time':"** **"}
                    roles.update({'_id': ctx.guild.id}, {'$push': {'userAccounts': newrolelist}})

                lol = roles.find({'_id': ctx.guild.id},{'userAccounts'})
                namelist = []
                for x in lol:
                    for y in x['userAccounts']:
                        name = list(y.items())[0][1]
                        namelist.append(name)
        except:
            print(traceback.format_exc()) 
        try:
            async def update_afk(self,ctx,userid,message):
                await self.open_list(ctx,userid,message)

                lol = roles.find({'_id': ctx.guild.id},{'userAccounts'})
                namelist = []
                for x in lol:
                    for y in x['userAccounts']:
                        name = list(y.items())[0][1]
                        namelist.append(name)

                time = datetime.datetime.now().replace(microsecond=0)
                newaccountlist = {'id':userid,'afkMessage': message,'time':time}
                roles.update({'_id': ctx.guild.id}, {'$push': {'userAccounts': newaccountlist}})
                from cogs.Lists.lists import goodbyes
                ranbye = random.choice(goodbyes)
                await ctx.reply(ranbye)
                if ctx.author.nick == None:
                    name = ctx.author.name
                else:
                    name = ctx.author.nick
                await ctx.author.edit(nick=f'[AFK] {name}')
        except:
            print(traceback.format_exc()) 

        try:
            async def off_afk(self,ctx,userid):
                roles.update({'_id': ctx.guild.id}, {'$pull': { 'userAccounts': {'id': userid} }})
                emote = "<:WelcomeBack:864944208304406548>"

                if type(ctx) == Message:
                    await ctx.add_reaction(emote)
                else:
                    await ctx.message.add_reaction(emote)

                nick = ctx.author.nick.replace('[AFK]', '')
                await ctx.author.edit(nick=nick)
        except:
            print(traceback.format_exc()) 

    except Exception:
        print(traceback.format_exc())  

        


        

   
    
def setup(bot):
    bot.add_cog(afk(bot))