import discord
from discord.ext import commands
from discord.message import Message
from pymongo import MongoClient
import traceback
import datetime
import random
import humanize 
from pytz import timezone

intents = discord.Intents.default()
intents.members = True

cluster = MongoClient("mongodb+srv://testbot:testbot123@testbot.78blp.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
afkDB = cluster["discord"]["afk"]

class afk(commands.Cog):
    try:
        def __init__(self, client):
            self.client = client

        # Creates global list variable to store all ID's of users that are AFK
        global namelist
        namelist = [] 

        @commands.command()
        async def afk(self,ctx,message = None):
            try:
                # Checks if user put a message after the ".afk"
                if message == None:
                    message = None
                else:
                    message = ctx.message.content.split(' ', 1)[1]
                
                # Updates namelist with all current AFK users
                await self.update_list(ctx.guild.id)
                global namelist

                # Checks if the user is in the AFK list
                for userID in namelist:
                    if userID == ctx.author.id:
                        # If user was previously AFK, this takes them off the list and ends the command
                        await self.off_afk(ctx,ctx.author.id)
                        await self.update_list(ctx.guild.id)
                        return

                # This only runs if the user wasnt previously in the AFK list
                await self.update_afk(ctx,ctx.author.id,message)
            except Exception:
                print(traceback.format_exc()) 
                
        # This listens to all messages sent in every channel the bot has access too
        @commands.Cog.listener()
        async def on_message(self, message):
            try:
                # Updates namelist with all current AFK users
                await self.update_list(message.guild.id)

                # Makes sure the bot isnt reading its own messages
                if message.author.id != self.client.user.id:
                    # Method that returns True if the message contains a mention (ex. "Hello @mush#666" will return True)
                    mentions = message.mentions

                    #Checks if message is a reply or contains a mention
                    if not mentions:
                        # Updates namelist with all current AFK users
                        await self.update_list(message.guild.id)
                        global namelist

                        #Loops through list to check if author was AFK. If yes, takes off AFK
                        for id in namelist:
                            if id == message.author.id:
                                # 
                                if '.afk' in message.content:
                                    await self.update_list(message.guild.id)
                                else:
                                    await self.off_afk(message,message.author.id)
                                    await self.update_list(message.guild.id)
                        
                        return

                    # Runs when the message has a mention
                    else:
                        # Gets AFK info from the db
                        afkUsers = afkDB.find({'_id': message.guild.id},{'userAccounts'})

                        # Declares empty list to store afk users later
                        namelist = []
                        # This will stay None if the ping in the message wasnt a user in the AFK list DB
                        userid = None

                        # Checks if author was AFK. If yes, takes off AFK
                        await self.update_list(message.guild.id)
                        for id in namelist:
                            if id == message.author.id:
                                # Ignores if user is trying to use the .afk command
                                if '.afk' in message.content:
                                    pass
                                else:
                                    await self.off_afk(message,message.author.id)

                        # Loops through DB and appends all AFK users names to 'namelist'
                        for users in afkUsers:
                            for userList in users['userAccounts']:
                                name = list(userList.items())[0][1]
                                msg = list(userList.items())[1][1]
                                time = list(userList.items())[2][1]
                                namelist.append(name)
                                
                                #Checks if user was mentioned in message
                                if str(name) in message.content:
                                    # Changes userid from None to the users is
                                    userid = name
                                    afkmsg = msg
                                    timeused = time
                                    break
                                else:
                                    # Stores back to None (I think this is repetetive)
                                    userid = None

                                # Checks if there is a mention (Also repetetive)
                                if mentions:
                                    for ping in mentions:
                                        # Gets the first ping in a message
                                        repliedtoauthor = ping
                                        break

                                    # Makes sure that the id found in the DB matches the id in the message ping
                                    if name == repliedtoauthor.id:
                                        userid = name
                                        afkmsg = msg
                                        timeused = time
                                        break
                        
                        #User was found in AFK List(namelist) sends out AFK message                
                        if userid != None:
                            afkuser = await message.guild.fetch_member(int(name))

                            # Declares the timezone that all time/date will be measured in
                            tz = timezone('US/Eastern')

                            # Gets the time the user went AFK and converts it to a datetime object
                            dt = datetime.datetime.strptime(str(timeused), "%Y-%m-%d %H:%M:%S")
                            # Converts that into a string
                            newdt = datetime.datetime.strftime(dt, "Today At %I:%M%p")

                            # Gets current time
                            current = datetime.datetime.now(tz)
                            dt = dt.replace(tzinfo=tz)
                            current = current.replace(tzinfo=tz)

                            # Calculates how many seconds its been since the user went AFK
                            seconds = (current-dt).total_seconds()

                            # Converts seconds to a string and creates a natural time string (ex. 10 minutes, 30 seconds || 45 seconds || 2 Days 3 Hours 1 Second)
                            if seconds < 60:
                                natty = humanize.precisedelta(seconds)
                            elif seconds > 86400:
                                natty = humanize.precisedelta(seconds, suppress=['minutes', 'seconds'], format="%0.0f")
                                newdt = datetime.datetime.strftime(dt, "%b-%d %I:%M%p")
                            else:
                                natty = humanize.precisedelta(seconds, suppress=['seconds'], format="%0.0f")

                            # Checks if the user had a message when going AFK and creates an Embed
                            if afkmsg == None:
                                embed = discord.Embed(color = discord.Colour.random())
                            else:
                                embed = discord.Embed(description = afkmsg, color = discord.Colour.random())

                            # Sets embed Author
                            embed.set_author(name=f"{afkuser.name} is AFK", icon_url=afkuser.avatar_url)

                            # Try and except just in case it wasnt able to create a natural time string
                            try:
                                embed.set_footer(text=f"{newdt} | {natty.title()} Ago")
                            except:
                                embed.set_footer(text=newdt)

                            # Finally sends out the AFK embed
                            await message.reply(embed=embed)

                        # Updates AFK list one more time
                        await self.update_list(message.guild.id)
                        
            except:
                print(f"```{traceback.format_exc()}```")

        # Function that gets all current AFK users and adds it to the global namelist
        async def update_list(self,guildid):
            global namelist
            namelist.clear()
            lol = afkDB.find({'_id': guildid},{'userAccounts'})
            for x in lol:
                for y in x['userAccounts']:
                    name = list(y.items())[0][1]
                    namelist.append(name)

        try:
            # Function that Creates a database for all servers 
            async def open_list(self,ctx,userid,message):
                check = afkDB.find({})
                serverlist = []
                for x in check:
                    serverlist.append(x.get('_id'))

                if ctx.guild.id in serverlist:
                    yon = True

                else:
                    yon = False

                if yon == False:
                    newshop = {"_id" : ctx.guild.id}
                    afkDB.insert_one(newshop)
                    newrolelist = {'userid':'** **', 'afkMessage':"** **",'time':"** **"}
                    afkDB.update({'_id': ctx.guild.id}, {'$push': {'userAccounts': newrolelist}})

                lol = afkDB.find({'_id': ctx.guild.id},{'userAccounts'})
                namelist = []
                for x in lol:
                    for y in x['userAccounts']:
                        name = list(y.items())[0][1]
                        namelist.append(name)
        except:
            print(traceback.format_exc()) 
        try:
            # Funcation that adds user to the AFK database
            async def update_afk(self,ctx,userid,message):
                await self.open_list(ctx,userid,message)

                lol = afkDB.find({'_id': ctx.guild.id},{'userAccounts'})
                namelist = []
                for x in lol:
                    for y in x['userAccounts']:
                        name = list(y.items())[0][1]
                        namelist.append(name)

                tz = timezone('US/Eastern')
                timez = datetime.datetime.now(tz).replace(microsecond=0)
                timez = datetime.datetime.strftime(timez, "%Y-%m-%d %H:%M:%S")

                newaccountlist = {'id':userid,'afkMessage': message,'time':timez}
                afkDB.update({'_id': ctx.guild.id}, {'$push': {'userAccounts': newaccountlist}})

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
            # Function that takes out the user from the database
            async def off_afk(self,ctx,userid):
                afkDB.update({'_id': ctx.guild.id}, {'$pull': { 'userAccounts': {'id': userid} }})
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
