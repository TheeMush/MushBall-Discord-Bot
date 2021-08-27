import discord
import traceback
import requests
import asyncio
import random
import json
from discord.ext import commands

class bar(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['drink','drinks'])
    async def bar(self,ctx):
        try:
            drink = u"\U0001F379"
            cocktail = u"\U0001F378"
            paper = u"\U0001F4D6"
            qm = 	u"\u2753"
            cancel = "\u274C"

            barembed = discord.Embed(title="React with: ",color = discord.Colour.random())
            barembed.set_author(name="MushBall's Bar", icon_url=self.client.user.avatar_url)
            barembed.add_field(name=f"{drink}  To get a specific drinks recipe",value="** **",inline=False)
            barembed.add_field(name=f"{cocktail}  To get a random drink with a specific ingredient",value="** **",inline=False)
            barembed.add_field(name=f"{paper}  For a list of drinks with a specific ingredient",value="** **",inline=False)
            barembed.add_field(name=f"{qm}  For a completely random drink",value="** **",inline=False)
            barembed.add_field(name=f"{cancel}  To exit",value="** **")


            buttons = [drink,cocktail,paper,qm,cancel]

            msg = await ctx.send(embed=barembed)     
            for button in buttons:
                await msg.add_reaction(button)

            try:
                reaction, user = await self.client.wait_for("reaction_add", check=lambda reaction, user: user == ctx.author and reaction.emoji in buttons, timeout=60.0)

            except asyncio.TimeoutError:
                barembed.add_field(name="\nYou didn't reply fast enough!",value="** **",inline=False)
                await msg.clear_reactions()
                await msg.edit(embed=barembed)
                return

            if reaction.emoji == drink:
                await msg.clear_reactions()
                async def search(ctx,query):
                    payload ={'s':query}
                    try:
                        r= requests.get('https://www.thecocktaildb.com/api/json/v1/1/search.php',params=payload)
                    except Exception as e:
                        print("Connection Failed !")
                        exit()
                    json_response = r.json()

                    drinks = json_response['drinks']
                    if drinks != None:
                        for i in drinks:
                            drinkname = i["strDrink"]
                            drinkinstructions = i["strInstructions"]
                            count=1
                            ingredients = []
                            while(count!=-1):
                                if i['strIngredient'+ str(count) ] != None:
                                    if i['strMeasure'+str(count)] == None:
                                        i['strMeasure'+str(count)] = '** **'
                                    ingredients.append(f"• {i['strMeasure'+str(count)]} `{i['strIngredient'+str(count)]}`")
                                    count+=1
                                else:
                                    count=-1

                            for x in ingredients:
                                text = '\n'.join(ingredients)

                            drinkurl = i["strDrinkThumb"]

                            break

                        embed = discord.Embed(title=drinkname,color = discord.Colour.random())
                        embed.set_author(name="MushBall's Bar", icon_url=self.client.user.avatar_url)
                        embed.add_field(name="Ingredients:",value=text)
                        embed.add_field(name="Instructions",value=drinkinstructions)
                        embed.set_thumbnail(url=drinkurl)
                        await msg.edit(embed=embed)
                    else:
                        embed = discord.Embed(color = discord.Colour.random())
                        embed.set_author(name="MushBall's Bar", icon_url=self.client.user.avatar_url)
                        embed.add_field(name="\nNo drinks found, try checking out the list of drinks!",value="** **",inline=False)
                        await msg.edit(embed=embed)

                async def start(ctx):
                    embed = discord.Embed(title=f"{drink} Say A Cocktail Name {drink}",color = discord.Colour.random())
                    embed.set_author(name="MushBall's Bar", icon_url=self.client.user.avatar_url)
                    embed.set_footer(text="Say <EXIT> to quit or <RANDOM> for a random drink!")
                    await msg.edit(embed=embed)

                    def check(message):
                        return message.author == ctx.author

                    try:
                        message = await self.client.wait_for('message', check=check, timeout= 30)
                    except asyncio.TimeoutError:
                        embed.add_field(name="\nYou didn't reply fast enough!",value="** **",inline=False)
                        await msg.edit(embed=embed)
                        return

                    choice = message.content
                    query=choice

                    if query.upper()=="EXIT":
                        await ctx.send("See you again, Enjoy your drink \U0001F942 !")
                    elif query.upper()=='RANDOM':
                        f = r"http://www.thecocktaildb.com/api/json/v1/1/random.php"
                        data = requests.get(f)
                        tt = json.loads(data.text)
                        
                        
                        for i in (tt["drinks"]):
                            drinkname = i["strDrink"]
                            drinkinstructions = i["strInstructions"]
                            count=1
                            ingredients = []
                            while(count!=-1):
                                if i['strIngredient'+ str(count) ] != None:
                                    if i['strMeasure'+str(count)] == None:
                                        i['strMeasure'+str(count)] = '** **'
                                    ingredients.append(f"• {i['strMeasure'+str(count)]} `{i['strIngredient'+str(count)]}`")
                                    count+=1
                                else:
                                    count=-1

                            for x in ingredients:
                                text = '\n'.join(ingredients)

                            drinkurl = i["strDrinkThumb"]

                            break

                        embed = discord.Embed(title=drinkname,color = discord.Colour.random())
                        embed.set_author(name="MushBall's Bar", icon_url=self.client.user.avatar_url)
                        embed.add_field(name="Ingredients:",value=text)
                        embed.add_field(name="Instructions",value=drinkinstructions)
                        embed.set_thumbnail(url=drinkurl)
                        await msg.edit(embed=embed)

                    else:
                        await search(ctx,query)
                await start(ctx)        

            elif reaction.emoji == cocktail:
                embed = discord.Embed(title=f"{cocktail} Enter An Ingredient {cocktail}",color = discord.Colour.random())
                embed.set_author(name="MushBall's Bar", icon_url=self.client.user.avatar_url)
                await msg.edit(embed=embed)
                await msg.clear_reactions()


                def check(message):
                    return message.author == ctx.author

                try:
                    message = await self.client.wait_for('message', check=check, timeout= 30)
                except asyncio.TimeoutError:
                    embed.add_field(name="\nYou didn't reply fast enough!",value="** **",inline=False)
                    await msg.edit(embed=embed)
                    return

                choice = message.content

                payload ={'i':choice}
                try:
                    r= requests.get('https://www.thecocktaildb.com/api/json/v1/1/filter.php?',params=payload)
                except Exception as e:
                    await ctx.send("Connection Failed!")
                try:
                    json_response = r.json()
                except:
                    embed = discord.Embed(color = discord.Colour.random())
                    embed.set_author(name="MushBall's Bar", icon_url=self.client.user.avatar_url)
                    embed.add_field(name="\nNo drinks found, try checking out the list of drinks!",value="** **",inline=False)
                    await msg.edit(embed=embed)
                    return

                drinks = json_response['drinks']
                if drinks != None:
                    drinklist = []
                    for i in drinks:
                        drinklist.append(i['strDrink'])

                    randrink = random.choice(drinklist)

                    payload ={'s':randrink}
                    try:
                        r= requests.get('https://www.thecocktaildb.com/api/json/v1/1/search.php',params=payload)
                    except Exception as e:
                        print("Connection Failed !")
                        exit()
                    json_response = r.json()

                    drinks = json_response['drinks']
                    if drinks != None:
                        for i in drinks:
                            drinkname = i["strDrink"]
                            drinkinstructions = i["strInstructions"]
                            count=1
                            ingredients = []
                            while(count!=-1):
                                if i['strIngredient'+ str(count) ] != None:
                                    if i['strMeasure'+str(count)] == None:
                                        i['strMeasure'+str(count)] = '** **'
                                    ingredients.append(f"• {i['strMeasure'+str(count)]} `{i['strIngredient'+str(count)]}`")
                                    count+=1
                                else:
                                    count=-1

                            for x in ingredients:
                                text = '\n'.join(ingredients)

                            drinkurl = i["strDrinkThumb"]

                            break

                        embed = discord.Embed(title=drinkname,color = discord.Colour.random())
                        embed.set_author(name="MushBall's Bar", icon_url=self.client.user.avatar_url)
                        embed.add_field(name="Ingredients:",value=text)
                        embed.add_field(name="Instructions",value=drinkinstructions)
                        embed.set_thumbnail(url=drinkurl)
                        await msg.edit(embed=embed)
                    else:
                        embed = discord.Embed(color = discord.Colour.random())
                        embed.set_author(name="MushBall's Bar", icon_url=self.client.user.avatar_url)
                        embed.add_field(name="\nNo drinks found, try checking out the list of drinks!",value="** **",inline=False)
                        await msg.edit(embed=embed)
                    
                else:
                    await ctx.send("No results found !")

            elif reaction.emoji == paper:
                embed = discord.Embed(title=f"{paper} Enter An Ingredient {paper}",color = discord.Colour.random())
                embed.set_author(name="MushBall's Bar", icon_url=self.client.user.avatar_url)
                await msg.edit(embed=embed)
                await msg.clear_reactions()

                def check(message):
                        return message.author == ctx.author

                try:
                    message = await self.client.wait_for('message', check=check, timeout= 30)
                except asyncio.TimeoutError:
                    embed.add_field(name="\nYou didn't reply fast enough!",value="** **",inline=False)
                    await msg.edit(embed=embed)
                    return

                choice = message.content

                payload ={'i':choice}
                try:
                    r= requests.get('https://www.thecocktaildb.com/api/json/v1/1/filter.php?',params=payload)
                except Exception as e:
                    await ctx.send("Connection Failed !")
                try:
                    json_response = r.json()
                except:
                    embed = discord.Embed(color = discord.Colour.random())
                    embed.set_author(name="MushBall's Bar", icon_url=self.client.user.avatar_url)
                    embed.add_field(name="\nNo drinks found, try something else!",value="** **",inline=False)
                    await msg.edit(embed=embed)
                    return

                drinks = json_response['drinks']
                if drinks != None:
                    drinklist = []
                    for i in drinks:
                        
                        drinklist.append(f"• `{i['strDrink']}`")

                        

                    

                    testlist = []
                    count = 1
                    self.client.help_pages = []
                    for x in drinklist:
                        testlist.append(x)

                        if len(testlist) > 6:
                            for x in testlist:
                                text = '\n'.join(testlist)

                            embedvar = 'page' + str(count)
                            embedvar = discord.Embed(title=f"Drinks with {choice.title()}:",description=text,color = discord.Colour.random())
                            embedvar.set_author(name="MushBall's Bar", icon_url=self.client.user.avatar_url)
                            self.client.help_pages.append(embedvar)
                            count+=1
                            drinklist = drinklist[7:]
                            testlist.clear()


                    for x in drinklist:
                        text = '\n'.join(drinklist)
                    embedvar = discord.Embed(title=f"Drinks with {choice.title()}:",description=text,color = discord.Colour.random())
                    embedvar.set_author(name="MushBall's Bar", icon_url=self.client.user.avatar_url)
                    self.client.help_pages.append(embedvar)

                    buttons = [u"\u2B05", u"\u27A1"] # skip to start, left, right, skip to end
                    current = 0
                    msg = await ctx.send(embed=self.client.help_pages[current])
                    
                    for button in buttons:
                        await msg.add_reaction(button)
                        
                    while True:
                        try:
                            reaction, user = await self.client.wait_for("reaction_add", check=lambda reaction, user: user == ctx.author and reaction.emoji in buttons, timeout=12.0)

                        except asyncio.TimeoutError:
                            await msg.clear_reactions()
                            return 

                        else:
                            previous_page = current
                                
                            if reaction.emoji == u"\u2B05":
                                if current > 0:
                                    current -= 1
                                    
                            elif reaction.emoji == u"\u27A1":
                                if current < len(self.client.help_pages)-1:
                                    current += 1

                            for button in buttons:
                                await msg.remove_reaction(button, ctx.author)

                            if current != previous_page:
                                await msg.edit(embed=self.client.help_pages[current])

            elif reaction.emoji == qm:
                await msg.clear_reactions()
                f = r"http://www.thecocktaildb.com/api/json/v1/1/random.php"
                data = requests.get(f)
                tt = json.loads(data.text)
                
                
                for i in (tt["drinks"]):
                    drinkname = i["strDrink"]
                    drinkinstructions = i["strInstructions"]
                    count=1
                    ingredients = []
                    while(count!=-1):
                        if i['strIngredient'+ str(count) ] != None:
                            if i['strMeasure'+str(count)] == None:
                                i['strMeasure'+str(count)] = '** **'
                            ingredients.append(f"• {i['strMeasure'+str(count)]} `{i['strIngredient'+str(count)]}`")
                            count+=1
                        else:
                            count=-1

                    for x in ingredients:
                        text = '\n'.join(ingredients)

                    drinkurl = i["strDrinkThumb"]

                    break

                embed = discord.Embed(title=drinkname,color = discord.Colour.random())
                embed.set_author(name="MushBall's Bar", icon_url=self.client.user.avatar_url)
                embed.add_field(name="Ingredients:",value=text)
                embed.add_field(name="Instructions",value=drinkinstructions)
                embed.set_thumbnail(url=drinkurl)
                await msg.edit(embed=embed)

            else:
                barembed.add_field(name="\nCancelled!",value="** **",inline=False)
                await msg.edit(embed=barembed)
                await msg.clear_reactions()
                return
        except:
            print(f"```{traceback.format_exc()}```")

    


def setup(client):
    client.add_cog(bar(client))