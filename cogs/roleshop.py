from discord.ext import commands
import discord
from pymongo import MongoClient
import traceback
import asyncio
from discord.utils import get
from cogs.Lists.functions import update_bank


cluster = MongoClient("mongodb+srv://testbot:testbot123@testbot.78blp.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
roles = cluster["discord"]["roleshop"]

class roleshop(commands.Cog):

    def __init__(self, client):
        self.client = client

    #Role Help Embed for Admins
    @commands.command(aliases=['roles'])
    @commands.check_any(commands.is_owner(),commands.has_permissions(administrator=True))
    async def role(self,ctx):
        field = []
        field.append("`.rolecreate 'NAME'` - Creates roles for server")
        field.append("`.roledelete @ROLE` - Deletes roles from server")
        field.append("`.shopadd '@ROLE' 'PRICE'` - Adds role to shop")
        field.append("`.shopdel @ROLE` - Deletes role from shop")
        text = '\n'.join(field)

        embed = discord.Embed(title="Subcommands",description=text,color=0x00ffff)
        embed.set_author(name="Roles", icon_url=ctx.author.avatar_url)
        embed.set_footer(text="Make sure to @ Mention the role")

        await ctx.send(embed=embed)

    #Create Server Role Command
    @commands.command(aliases=['rolecreate'])
    @commands.check_any(commands.is_owner(),commands.has_permissions(administrator=True))
    async def createrole(self,ctx, *, content = None):
        if content == None:
            await ctx.invoke(self.client.get_command('role'))
            return

        guild = ctx.guild
        role = await guild.create_role(name=content,mentionable=False)  
        roleid = role.id
        embed = discord.Embed(title='**Created A New Role:**', description=f"<@&{roleid}>",color=0xFFD700)
        embed.set_author(name="Roles", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)
        

    #Delete Server Role Command
    @commands.command(aliases=['roledel','deleterole','roledelete'])
    @commands.check_any(commands.is_owner(),commands.has_permissions(administrator=True))
    async def delrole(self, ctx, *,role_name:discord.Role = None):

        #Checks if role is already in shop
        lol = roles.find({'_id': ctx.guild.id},{'rolesArray'})
        namelist = []
        for x in lol:
            for y in x['rolesArray']:
                name = list(y.items())[0][1]
                namelist.append(name)
        if str(role_name.id) in namelist:
            embed = discord.Embed(title='**Error:**', description=f"That role is in the shop!\nPlease delete it from the shop first\n\n**.shopdel <@&{role_name.id}>**",color=0xFF0000)
            embed.set_author(name="Roles", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)
            return

        #Successful Delete
        embed = discord.Embed(title='**Deleted The Role:**', description=f"<@&{role_name.id}>",color=0xFF0000)
        embed.set_author(name="Roles", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)
        await role_name.delete()

    #DELETE SERVER ROLE ERROR HANDLING
    @delrole.error
    async def delrole_error(self,ctx, error):
        if isinstance(error, commands.errors.RoleNotFound):
            embed = discord.Embed(title="**Error: That role wasn't found**", description=f".delrole `@ROLE`",color=0xFF0000)
            embed.set_footer(text="Make sure to @ Mention the role")
            embed.set_author(name=f"{ctx.message.guild.name}  ", icon_url=ctx.guild.icon_url)
            await ctx.send(embed=embed)
        elif isinstance(error, commands.errors.MissingPermissions):
            embed = discord.Embed(title="**Error: You don't have the correct permissions**",color=0xFF0000)
            embed.set_author(name=f"{ctx.message.guild.name}  ", icon_url=ctx.guild.icon_url)
            await ctx.send(embed=embed)
        
        elif isinstance(error, commands.errors.CheckAnyFailure):
            return
        else:
            await ctx.invoke(self.client.get_command('role'))
            print(traceback.format_exc())

    #Shop Command
    @commands.command(aliases=['roleshop','store'])
    async def shop(self,ctx):

        def price_sort(sort_list):
    
            def get_price(text):
                return int(text.split(":** $")[1].replace(",",""))

            return sorted(sort_list,key=lambda x:get_price(x),reverse=True)


        lol = roles.find({'_id': ctx.guild.id},{'rolesArray'})
        embedlist = []
        for x in lol:
            for y in x['rolesArray']:
                name = list(y.items())[0][1]
                price = list(y.items())[1][1]

                if '** **' in name:
                    continue
                
                role = get(ctx.guild.roles, id=int(name))
                if role == None:
                    continue

                embedlist.append(f"• <@&{name}> **:** ${format (price, ',d')}")

        embedlist = price_sort(embedlist)

        for x in embedlist:
            text = '\n'.join(embedlist)

        #If shop is empty
        if not embedlist:
            embed = discord.Embed(title="__Roles__",description='** **',color=discord.Colour.random())
            embed.set_author(name=f"{ctx.message.guild.name} | Shop  ", icon_url=ctx.guild.icon_url)
            embed.set_footer(text="There's no roles to buy :(")
            await ctx.send(embed=embed)
            return

        embed = discord.Embed(title="__Roles__",description=text,color=discord.Colour.random())
        embed.set_author(name=f"{ctx.message.guild.name} | Shop  ", icon_url=ctx.guild.icon_url)
        embed.set_footer(text='Do <.buy @ROLE> or <.buy "ROLE"> to buy a role!')
        await ctx.send(embed=embed)
    
    #SHOP ERROR HANDLING
    @shop.error
    async def shoperror(self,ctx,error):
        print(f"```{traceback.format_exc()}```")


    #Shop Add Command
    @commands.command(aliases=['addshop'])
    @commands.check_any(commands.is_owner(),commands.has_permissions(administrator=True))
    async def shopadd(self,ctx, rolename:discord.Role = None, price = None):
        await self.open_shop(ctx)

        #Checks if role is already in shop
        lol = roles.find({'_id': ctx.guild.id},{'rolesArray'})
        namelist = []
        for x in lol:
            for y in x['rolesArray']:
                name = list(y.items())[0][1]
                namelist.append(name)
        if str(rolename.id) in namelist:
            embed = discord.Embed(title='ERROR:', description="That role is already in the shop!",color=0xFF0000)
            embed.set_author(name=f"{ctx.message.guild.name}  ", icon_url=ctx.guild.icon_url)
            await ctx.send(embed=embed)
            return

        #Adds role to shop
        price = int(price)
        newrolelist = {'rolename':str(rolename.id), 'price':price}
        roles.update({'_id': ctx.guild.id}, {'$push': {'rolesArray': newrolelist}})

        embed = discord.Embed(title='**Added To Shop:**', description=f"**Role:** <@&{rolename.id}>\n **Price:** ${format (price, ',d')}",color=0xFFD700)
        embed.set_author(name=f"{ctx.message.guild.name}  ", icon_url=ctx.guild.icon_url)
        await ctx.send(embed=embed)

    #SHOP ADD ERROR HANDLING
    @shopadd.error
    async def shopadd_error(self,ctx, error):
        if isinstance(error, commands.errors.RoleNotFound):
            embed = discord.Embed(title="**Error: That role wasn't found**", description=f".shopadd `@ROLE` `PRICE`",color=0xFF0000)
            embed.set_footer(text="Make sure to @ Mention the role")
            embed.set_author(name=f"{ctx.message.guild.name}  ", icon_url=ctx.guild.icon_url)
            await ctx.send(embed=embed)
        elif isinstance(error, commands.errors.MissingPermissions):
            embed = discord.Embed(title="**Error: You don't have the correct permissions**",color=0xFF0000)
            embed.set_author(name=f"{ctx.message.guild.name}  ", icon_url=ctx.guild.icon_url)
            await ctx.send(embed=embed)
        elif isinstance(error, commands.errors.CheckAnyFailure):
            return
        else:
            await ctx.invoke(self.client.get_command('role'))
            print(f"```{traceback.format_exc()}```")

    #Shop Delete Command
    @commands.command(aliases=['delshop','shopdelete','deleteshop','shopremove','removeshop'])
    @commands.check_any(commands.is_owner(),commands.has_permissions(administrator=True))
    async def shopdel(self,ctx,rolename:discord.Role = None):
        #Checks if role is in shop
        lol = roles.find({'_id': ctx.guild.id},{'rolesArray'})
        namelist = []
        for x in lol:
            for y in x['rolesArray']:
                name = list(y.items())[0][1]
                namelist.append(name)

        if str(rolename.id) in namelist:
            roles.update({'_id': ctx.guild.id}, {'$pull': { 'rolesArray': {'rolename': str(rolename.id)} }})

            embed = discord.Embed(title='**Deleted Role From Shop:**', description=f"<@&{rolename.id}>",color=0xFF0000)
            embed.set_author(name=f"{ctx.message.guild.name}  ", icon_url=ctx.guild.icon_url)
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title='**ERROR:**', description="That role isn't in the shop!",color=0xFF0000)
            embed.set_author(name=f"{ctx.message.guild.name}  ", icon_url=ctx.guild.icon_url)
            await ctx.send(embed=embed)

    #SHOP DELETE ERROR HANDLING
    @shopdel.error
    async def shopdel_error(self,ctx, error):
        if isinstance(error, commands.errors.RoleNotFound):
            embed = discord.Embed(title="**Error: That role wasn't found**", description=f"Make sure you @ mention the role when deleting from the shop\n\n.shopdel `@ROLE`",color=0xFF0000)
            embed.set_author(name=f"{ctx.message.guild.name}  ", icon_url=ctx.guild.icon_url)
            await ctx.send(embed=embed)
        elif isinstance(error, commands.errors.MissingPermissions):
            embed = discord.Embed(title="**Error: You don't have the correct permissions**",color=0xFF0000)
            embed.set_author(name=f"{ctx.message.guild.name}  ", icon_url=ctx.guild.icon_url)
            await ctx.send(embed=embed)
        elif isinstance(error, commands.errors.CheckAnyFailure):
            return
        else:
            await ctx.invoke(self.client.get_command('role'))
            print(f"```{traceback.format_exc()}```")            

    #Buy Command
    @commands.command(aliases=['shopbuy','buyrole','rolebuy'])
    async def buy(self,ctx,buyrole:discord.Role = None,member:discord.Member=None):
        if buyrole == None:
            await ctx.invoke(self.client.get_command('shop'))
            return

        if member == None:
            if buyrole in ctx.author.roles:
                embed = discord.Embed(description=f"Are you sure you want to get remove the '{buyrole.mention}' role?", color=discord.Colour.random())
                embed.set_footer(text="React with your answer")
                embed.set_author(name="Remove Role", icon_url=ctx.author.avatar_url)

                buttons = [u"\U0001f44d",u"\U0001F44E"] 

                msg = await ctx.send(embed=embed)
                
                for button in buttons:
                    await msg.add_reaction(button)

                try:
                    reaction, user = await self.client.wait_for("reaction_add", check=lambda reaction, user: user == ctx.author and reaction.emoji in buttons, timeout=60.0)

                except asyncio.TimeoutError:
                    await ctx.reply("You didn't reply fast enough")
                    return

                if reaction.emoji == u"\U0001f44d":
                    embed = discord.Embed(description=f"Succesfully removed the {buyrole.mention} role!", color=discord.Colour.random())
                    embed.set_author(name="Remove Role", icon_url=ctx.author.avatar_url)
                    await msg.edit(embed=embed)
                    await ctx.author.remove_roles(buyrole)
                    await msg.clear_reactions()
                    return
                else:
                    embed = discord.Embed(description=f"Cancelled!", color=discord.Colour.random())
                    embed.set_author(name="Remove Role", icon_url=ctx.author.avatar_url)
                    await msg.edit(embed=embed)
                    await msg.clear_reactions()
                    return


                
        

        #Checks if role is in shop
        lol = roles.find({'_id': ctx.guild.id},{'rolesArray'})
        namelist = []
        for x in lol:
            for y in x['rolesArray']:
                name = list(y.items())[0][1]
                namelist.append(name)

        if str(buyrole.id) in namelist:
            lol = roles.find({'_id': ctx.guild.id},{'rolesArray'})
            amountlist=[]
            for x in lol:
                for y in x['rolesArray']:
                    name = list(y.items())[0][1]
                    price = list(y.items())[1][1]

                    if str(name) == str(buyrole.id):
                        amountlist.append(int(price))
                        break

            amount = int(amountlist[0])

            bal = await update_bank(ctx,ctx.author.id,0,0)
            if amount>bal[0]:
                await ctx.reply("You don't have that much")
                return

            buyrole = (discord.utils.get(ctx.guild.roles, id=buyrole.id))
            await update_bank(ctx,ctx.author.id,-1*amount,0)
            am = discord.AllowedMentions(roles=False)

            if member != None:
                if buyrole in member.roles:
                    embed = discord.Embed(title=f"**:money_with_wings:  |  They already have that role**",color=0xFF0000)
                    embed.set_author(name=f"{ctx.message.guild.name} | Shop  ", icon_url=ctx.author.avatar_url)
                    await ctx.send(embed=embed)
                    return

                await member.add_roles(buyrole)
                await ctx.reply(f"**:money_with_wings: | You bought the {buyrole.mention} Role for {member.mention}!**",allowed_mentions=am)
                return

            await ctx.author.add_roles(buyrole)
            await ctx.reply(f"**:money_with_wings: | You bought the {buyrole.mention} Role!**",allowed_mentions=am)

        else:
            embed = discord.Embed(title="**Error: That role wasn't found**", description=f".buy `@ROLE`",color=0xFF0000)
            embed.set_footer(text="Make sure to @ Mention the role or put the role name in wuoyes")
            embed.set_author(name=f"{ctx.message.guild.name}  ", icon_url=ctx.guild.icon_url)
            await ctx.send(embed=embed)

    #BUY ERROR HANDLING
    @buy.error
    async def buy_error(self,ctx, error):
        if isinstance(error, commands.errors.RoleNotFound):
            embed = discord.Embed(title="**Error: That role wasn't found**", description=f"Make sure you @ mention the role or spell it correctly (Case-Sensitive) when buying\n\n.buy `@ROLE`",color=0xFF0000)
            embed.set_author(name=f"{ctx.message.guild.name}  ", icon_url=ctx.guild.icon_url)
            await ctx.send(embed=embed)
        else:
            print(traceback.format_exc())

    #Remove Roles
    @commands.command()
    async def remove(self,ctx,member:discord.Member,role:discord.Role):
        if ctx.author.id == 569792736367083560:
            await ctx.message.delete()
            await member.remove_roles(role)
        else:
            return

    #FUNCTIONS
    async def open_shop(self,ctx):
        check = roles.find({})
        serverlist = []
        for x in check:
            serverlist.append(x.get('_id'))

        if ctx.guild.id in serverlist:
            yon = True
        else:
            yon = False
        if yon == True:
            return
        elif yon == False:
            newshop = {"_id" : ctx.guild.id}
            roles.insert_one(newshop)
            newrolelist = {'rolename':'** **', 'price':"** **"}
            roles.update({'_id': ctx.guild.id}, {'$push': {'rolesArray': newrolelist}})

   
    
def setup(bot):
    bot.add_cog(roleshop(bot))