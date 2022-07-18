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
        # Emoji variables
        EMOJI_DRINK = u"\U0001F379"
        EMOJI_COCKTAIL = u"\U0001F378"
        EMOJI_PAPER = u"\U0001F4D6"
        EMOJI_QUESTION = 	u"\u2753"
        EMOJI_CANCEL = "\u274C"

        # Menu Embed
        barembed = discord.Embed(title="React with: ",color = discord.Colour.random())
        barembed.set_author(name="MushBall's Bar", icon_url=self.client.user.avatar_url)
        barembed.add_field(name=f"{EMOJI_DRINK}  To get a specific drinks recipe",value="** **",inline=False)
        barembed.add_field(name=f"{EMOJI_COCKTAIL}  To get a random drink with a specific ingredient",value="** **",inline=False)
        barembed.add_field(name=f"{EMOJI_PAPER}  For a list of drinks with a specific ingredient",value="** **",inline=False)
        barembed.add_field(name=f"{EMOJI_QUESTION}  For a completely random drink",value="** **",inline=False)
        barembed.add_field(name=f"{EMOJI_CANCEL}  To exit",value="** **")


        buttons = [EMOJI_DRINK,EMOJI_COCKTAIL,EMOJI_PAPER,EMOJI_QUESTION,EMOJI_CANCEL]

        # Adds the reactions to the menu
        msg = await ctx.send(embed=barembed)     
        for button in buttons:
            await msg.add_reaction(button)

        try:
            # Waits for a reaction (60 seconds max)
            reaction, user = await self.client.wait_for("reaction_add", check=lambda reaction, user: user == ctx.author and reaction.emoji in buttons, timeout=60.0)

        except asyncio.TimeoutError:
            barembed.add_field(name="\nYou didn't reply fast enough!",value="** **",inline=False)
            await msg.clear_reactions()
            await msg.edit(embed=barembed)
            return

        if reaction.emoji == EMOJI_DRINK:
            await msg.clear_reactions()
            async def search(ctx,query):
                payload ={'s':query}
                try:
                    r= requests.get('https://www.thecocktaildb.com/api/json/v1/1/search.php',params=payload)
                except Exception as e:
                    print("Connection Failed !")
                    exit()
                jsonResponse = r.json()

                drinksResponse = jsonResponse['drinks']
                if drinksResponse != None:
                    for drink in drinksResponse:
                        drinkName = drink["strDrink"]
                        drinkInstructions = drink["strInstructions"]
                        ingredients = []
                        count = 1
                        while(count!=-1):
                            if drink['strIngredient'+ str(count)]:
                                if not drink['strMeasure'+str(count)]:
                                    drink['strMeasure'+str(count)] = '** **'
                                ingredients.append(f"• {drink['strMeasure'+str(count)]} `{drink['strIngredient'+str(count)]}`")
                                count += 1
                            else:
                                count = -1

                        ingredientList = '\n'.join(ingredients)

                        drinkurl = drink["strDrinkThumb"]

                        break

                    embed = discord.Embed(title=drinkName,color = discord.Colour.random())
                    embed.set_author(name="MushBall's Bar", icon_url=self.client.user.avatar_url)
                    embed.add_field(name="Ingredients:", value=ingredientList)
                    embed.add_field(name="Instructions", value=drinkInstructions)
                    embed.set_thumbnail(url=drinkurl)
                    await msg.edit(embed=embed)
                else:
                    embed = discord.Embed(color = discord.Colour.random())
                    embed.set_author(name="MushBall's Bar", icon_url=self.client.user.avatar_url)
                    embed.add_field(name="\nNo drinks found, try checking out the list of drinks!",value="** **",inline=False)
                    await msg.edit(embed=embed)

            async def start(ctx):
                embed = discord.Embed(title=f"{EMOJI_DRINK} Say A Cocktail Name {EMOJI_DRINK}",color = discord.Colour.random())
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

                        ingredientList = '\n'.join(ingredients)

                        drinkurl = i["strDrinkThumb"]

                        break

                    embed = discord.Embed(title=drinkname,color = discord.Colour.random())
                    embed.set_author(name="MushBall's Bar", icon_url=self.client.user.avatar_url)
                    embed.add_field(name="Ingredients:",value=ingredientList)
                    embed.add_field(name="Instructions",value=drinkinstructions)
                    embed.set_thumbnail(url=drinkurl)
                    await msg.edit(embed=embed)

                else:
                    await search(ctx,query)
            await start(ctx)        

        elif reaction.emoji == EMOJI_COCKTAIL:
            embed = discord.Embed(title=f"{EMOJI_COCKTAIL} Enter An Ingredient {EMOJI_COCKTAIL}",color = discord.Colour.random())
            embed.set_author(name="MushBall's Bar", icon_url=self.client.user.avatar_url)
            await msg.edit(embed=embed)
            await msg.clear_reactions()


            def check(message):
                return message.author == ctx.author

            try:
                # Waits for a message (30 seconds max)
                message = await self.client.wait_for('message', check=check, timeout=30)
            except asyncio.TimeoutError:
                embed.add_field(name="\nYou didn't reply fast enough!",value="** **",inline=False)
                await msg.edit(embed=embed)
                return

            choice = message.content

            payload ={'i':choice}
            try:
                r = requests.get('https://www.thecocktaildb.com/api/json/v1/1/filter.php?',params=payload)
            except Exception as e:
                await ctx.send("Connection Failed!")
            try:
                jsonResponse = r.json()
            except:
                embed = discord.Embed(color = discord.Colour.random())
                embed.set_author(name="MushBall's Bar", icon_url=self.client.user.avatar_url)
                embed.add_field(name="\nNo drinks found, try checking out the list of drinks!",value="** **",inline=False)
                await msg.edit(embed=embed)
                return

            drinksResponse = jsonResponse['drinks']
            if not drinksResponse:
                drinkList = []
                for drink in drinksResponse:
                    drinkList.append(drink['strDrink'])

                ranDrink = random.choice(drinkList)

                payload ={'s':ranDrink}
                try:
                    r= requests.get('https://www.thecocktaildb.com/api/json/v1/1/search.php',params=payload)
                except Exception as e:
                    print("Connection Failed !")
                    exit()
                jsonResponse = r.json()

                drinksResponse = jsonResponse['drinks']
                if drinksResponse:
                    for drink in drinksResponse:
                        drinkname = drink["strDrink"]
                        drinkinstructions = drink["strInstructions"]
                        count=1
                        ingredients = []
                        while(count!=-1):
                            if drink['strIngredient'+ str(count)]:
                                if not drink['strMeasure'+str(count)]:
                                    drink['strMeasure'+str(count)] = '** **'
                                ingredients.append(f"• {drink['strMeasure'+str(count)]} `{drink['strIngredient'+str(count)]}`")
                                count+=1
                            else:
                                count=-1

                        ingredientList = '\n'.join(ingredients)

                        drinkurl = drink["strDrinkThumb"]

                        break

                    embed = discord.Embed(title=drinkname,color = discord.Colour.random())
                    embed.set_author(name="MushBall's Bar", icon_url=self.client.user.avatar_url)
                    embed.add_field(name="Ingredients:",value=ingredientList)
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

        elif reaction.emoji == EMOJI_PAPER:
            embed = discord.Embed(title=f"{EMOJI_PAPER} Enter An Ingredient {EMOJI_PAPER}",color = discord.Colour.random())
            embed.set_author(name="MushBall's Bar", icon_url=self.client.user.avatar_url)
            await msg.edit(embed=embed)
            await msg.clear_reactions()

            def check(message):
                    return message.author == ctx.author

            try:
                # Waits for a message (30 seconds max)
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
                jsonResponse = r.json()
            except:
                embed = discord.Embed(color = discord.Colour.random())
                embed.set_author(name="MushBall's Bar", icon_url=self.client.user.avatar_url)
                embed.add_field(name="\nNo drinks found, try something else!",value="** **",inline=False)
                await msg.edit(embed=embed)
                return

            drinksResponse = jsonResponse['drinks']
            if drinksResponse != None:
                drinkList = []
                for drink in drinksResponse:
                    drinkList.append(f"• `{drink['strDrink']}`")

                page = []
                count = 1
                self.client.help_pages = []
                for drink in drinkList:
                    page.append(drink)

                    if len(page) > 6:
                        ingredientList = '\n'.join(page)

                        embedvar = 'page' + str(count)
                        embedvar = discord.Embed(title=f"Drinks with {choice.title()}:",description=ingredientList,color = discord.Colour.random())
                        embedvar.set_author(name="MushBall's Bar", icon_url=self.client.user.avatar_url)
                        self.client.help_pages.append(embedvar)
                        count+=1
                        drinkList = drinkList[7:]
                        page.clear()


                ingredientList = '\n'.join(drinkList)
                embedvar = discord.Embed(title=f"Drinks with {choice.title()}:",description=ingredientList,color = discord.Colour.random())
                embedvar.set_author(name="MushBall's Bar", icon_url=self.client.user.avatar_url)
                self.client.help_pages.append(embedvar)

                buttons = [u"\u2B05", u"\u27A1"] # left, right
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

        elif reaction.emoji == EMOJI_QUESTION:
            await msg.clear_reactions()
            f = r"http://www.thecocktaildb.com/api/json/v1/1/random.php"
            data = requests.get(f)
            tt = json.loads(data.text)
            
            
            for drink in (tt["drinks"]):
                drinkname = drink["strDrink"]
                drinkinstructions = drink["strInstructions"]
                count=1
                ingredients = []
                while(count!=-1):
                    if drink['strIngredient'+ str(count) ] != None:
                        if drink['strMeasure'+str(count)] == None:
                            drink['strMeasure'+str(count)] = '** **'
                        ingredients.append(f"• {drink['strMeasure'+str(count)]} `{drink['strIngredient'+str(count)]}`")
                        count+=1
                    else:
                        count=-1

                for drink in ingredients:
                    ingredientList = '\n'.join(ingredients)

                drinkurl = drink["strDrinkThumb"]

                break

            embed = discord.Embed(title=drinkname,color = discord.Colour.random())
            embed.set_author(name="MushBall's Bar", icon_url=self.client.user.avatar_url)
            embed.add_field(name="Ingredients:",value=ingredientList)
            embed.add_field(name="Instructions",value=drinkinstructions)
            embed.set_thumbnail(url=drinkurl)
            await msg.edit(embed=embed)

        else:
            barembed.add_field(name="\nCancelled!",value="** **",inline=False)
            await msg.edit(embed=barembed)
            await msg.clear_reactions()
            return
        

    


def setup(client):
    client.add_cog(bar(client))
