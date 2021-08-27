import discord
import random
import asyncio
from discord.ext import commands

class Help(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def lose(self,ctx):
        await ctx.send("hi")
    

    @commands.command()
    async def help(self,ctx):
        #Help Pages
        page1 = discord.Embed(title="Commands List", description="Use the buttons below to navigate between help pages.", color=0x01a500)
        page1.set_author(name="MushBall")
        page1.set_thumbnail(url="https://cdn.frankerfacez.com/emoticon/388352/4")
        page1.add_field(name="**.casinohelp**",value="Gamble a little bit, its fun",inline=False)
        page1.add_field(name="**.customhelp**", value="If you wanna see custom commands",inline=False)
        page1.add_field(name="**.mushball ''insert question here''** ",value="I answer yes or no questions",inline=False)
        page1.add_field(name="**.kith `<@USER>`**",value="Give someone a kith",inline=False)
        page1.add_field(name="**.slap `<@USER>`**",value="Slap someone, they probably deserve it",inline=False)
        page1.add_field(name="**.pat `<@USER>`**",value="Everyone deserves some headpats",inline=False)
        page1.set_footer(text="@Mush if you wanna suggest something")
        
        page2 = discord.Embed(title="Commands List", description="Page 2", color=0x01a500)
        page2.set_author(name="MushBall")
        page2.set_thumbnail(url="https://cdn.frankerfacez.com/emoticon/388352/4")
        page2.add_field(name="**.glock `<@USER>`**",value="Some people just need to get glocked",inline=False)
        page2.add_field(name="**.yeet `<@USER>`**",value="I yeet a mf",inline=False)
        page2.add_field(name="**.homies `<@USER>`**", value="Always kiss your homies",inline=False)
        page2.add_field(name="**.mushsleep `<@USER>`**",value="I politely tell the person you @ to goto sleep",inline=False)
        page2.add_field(name="**.salty `<@USER>`**",value="For when someones being salty",inline=False)
        page2.add_field(name="**.mushmatch `<@USER>`**",value="Based off a very advanced algorithm and not a random number, I'll tell you the compatibility % of you and another person (I can rig this for a price)",inline=False)
        page2.set_footer(text="@Mush if you wanna suggest something")

        page3 = discord.Embed(title="Commands List", description="Last Page", color=0x01a500)
        page3.set_author(name="MushBall")
        page3.set_thumbnail(url="https://cdn.frankerfacez.com/emoticon/388352/4")
        page3.add_field(name="**.mushcrypto**",value="I give a summary of the crypto market today that I wrote and definitely didn't steal",inline=False)
        page3.add_field(name="**.fuck**", value="Just do it and see for yourself",inline=False)
        page3.add_field(name="**.food/.drink**",value="I suggest something random to eat/drink",inline=False)
        page3.add_field(name="**.hi**",value="Say hi to me, I get lonely",inline=False)
        page3.add_field(name="**.bye**",value="Be nice and say bye",inline=False)
        page3.add_field(name="**.shots**", value="SHOTS",inline=False)
        page3.set_footer(text="@Mush if you wanna suggest something")

        self.client.help_pages = [page1, page2, page3]
        buttons = [u"\u2B05", u"\u27A1"] # skip to start, left, right, skip to end
        current = 0
        msg = await ctx.send(embed=self.client.help_pages[current])
        
        for button in buttons:
            await msg.add_reaction(button)
            
        while True:
            try:
                reaction, user = await self.client.wait_for("reaction_add", check=lambda reaction, user: user == ctx.author and reaction.emoji in buttons, timeout=60.0)

            except asyncio.TimeoutError:
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

    @commands.command()
    async def customhelp(self,ctx):
        #Help Pages
        page1 = discord.Embed(title="Custom Commands List", description="Use the buttons below to navigate between help pages.", color=0x01a500)
        page1.set_author(name="MushBall")
        page1.set_thumbnail(url="https://cdn.frankerfacez.com/emoticon/388352/4")
        page1.set_footer(text="@Mush if you want your own personal command but no guarantees i'll make it")
        page1.add_field(name="**.yumo `<@USER>`**",value="Slap someone",inline=False)
        page1.add_field(name="**.cabby**", value="I send random cabbage gifs",inline=False)
        page1.add_field(name="**.chea**",value="I send a gif of Chea",inline=False)
        page1.add_field(name="**.moggles**",value="Let me share some wisdom from Old Man Moggles",inline=False)
        page1.add_field(name="**.annie**",value="Get some plant facts from Annie", inline=False)
        page1.add_field(name="**.angie**",value="Say something nice to Ang! (If you'd like to add to this list @Mush or DM him)",inline=False)
        page1.add_field(name="**.sleppy**", value="Swag", inline=False)
        page1.set_footer(text= "@Mush if you want your own personal command but no guarantees i'll make it")
        
        page2 = discord.Embed(title="Commands List", description="Page 2", color=0x01a500)
        page2.set_author(name="MushBall")
        page2.set_thumbnail(url="https://cdn.frankerfacez.com/emoticon/388352/4")
        page2.add_field(name="**.salty `<@USER>`**",value="If someones being salty",inline=False)
        page2.add_field(name="**.dev**", value="GREEK GOD SUMMER", inline=False)
        page2.add_field(name="**.rio `<@USER>`**",value="Give someone a kith",inline=False)
        page2.add_field(name="**.pat**", value="Pat someone", inline=False)
        page2.add_field(name="**.patrick *playlist***",value="Let me give you a song to listen to. Add *playlist* if you want the full playlist",inline=False)
        page2.add_field( name="**.goose *playlist***",value="Check out Goose's song of the day. Add *playlist* if you want the full playlist",inline=False)
        page2.add_field(name="**.sarah**", value="*NUGGIES*", inline=False)
        
        page2.set_footer(text="@Mush if you want your own personal command but no guarantees i'll make it")

        page3 = discord.Embed(title="Commands List", description="Last Page", color=0x01a500)
        page3.set_author(name="MushBall")
        page3.set_thumbnail(url="https://cdn.frankerfacez.com/emoticon/388352/4")
        page3.add_field(name="**.zhu `<@USER>`**",value="Drink some joose",inline=False)
        page3.add_field(name="**.bubu**",value="Lemme give you the best pickup lines ever", inline=False)
        page3.add_field(name="**.dahlia**",value="Idk I just do nothing",inline=False)
        page3.add_field(name="**.waylan**", value="Simp time", inline=False)
        page3.add_field(name="**.charie**", value="**PRAISE VODKA**", inline=False)
        page3.add_field(name="**.scribbles `<@USER>`**", value="Glock a mf", inline=False)
        page3.add_field(name="**.burg**", value="I just make no sense", inline=False)
        page3.set_footer(text="@Mush if you want your own personal command but no guarantees i'll make it")

        self.client.help_pages = [page1, page2, page3]
        buttons = [u"\u2B05", u"\u27A1"] # skip to start, left, right, skip to end
        current = 0
        msg = await ctx.send(embed=self.client.help_pages[current])
        
        for button in buttons:
            await msg.add_reaction(button)
            
        while True:
            try:
                reaction, user = await self.client.wait_for("reaction_add", check=lambda reaction, user: user == ctx.author and reaction.emoji in buttons, timeout=60.0)

            except asyncio.TimeoutError:
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

    @commands.command()
    async def casinohelp(self,ctx):
        #Help Pages
        page1 = discord.Embed(title="**Page 1 | __Games__**", color=0x01a500)
        page1.set_author(name="Commands List")
        page1.set_thumbnail(url="https://cdn.frankerfacez.com/emoticon/388352/4")
        page1.add_field(name="**.coinflip `<heads or tails>` `<amount>`**", value="Gamble on a coinflip *win 2x your bet*", inline=False)
        page1.add_field(name="**.highlow `<amount>` `<high/low>`**", value="Bet on wheter a randum number is going to be high or low *win 2x your bet*", inline=False)
        page1.add_field(name="**.blackjack `<amount>`**", value="Lets see if you can beat the dealer *win 3x your bet*", inline=False)
        page1.add_field(name="**.slots `<amount>`**", value="Try your luck playing slots *win 10x your bet*", inline=False)
        page1.add_field(name="**.cups `1-4` `<amount>`**", value="Guess which cup the ball is under *win 3x your bet*", inline=False)
        page1.add_field(name="**.lottery**", value="For when you're feeling lucky", inline=False)
        page1.set_footer(text="@Mush if you wanna suggest something")
        
        page2 = discord.Embed(title="**Page 2 | __2 Player Games__**", color=0x01a500)
        page2.set_author(name="Commands List")
        page2.set_thumbnail(url="https://cdn.frankerfacez.com/emoticon/388352/4")
        page2.add_field(name="**.rps `<@USER>` `<amount>`**", value="Play rock, paper, scissors with someone *win whatever you bet*", inline=False)
        page2.add_field(name="**.ttt `<@USER>` `<amount>`**", value="Play tic tac toe with someone *win whatever you bet*", inline=False)
        page2.add_field(name="**.connect4 `<bot (optional)>` `<amount>`**", value="Play connect4 with me or with someone *win whatever you bet*", inline=False)
        page2.set_footer(text="@Mush if you wanna suggest something")

        page3 = discord.Embed(title="**Page 3 | __Casino Commands__**", color=0x01a500)
        page3.set_author(name="Commands List")
        page3.set_thumbnail(url="https://cdn.frankerfacez.com/emoticon/388352/4")
        page3.add_field(name="**.balance**", value="Check your current balance", inline=False)
        page3.add_field(name="**.deposit**", value="Deposits your money into your bank", inline=False)
        page3.add_field(name="**.withdraw**", value="Withdraws money into your wallet", inline=False)
        page3.add_field(name="**.daily**", value="Get your daily free money", inline=False)
        page3.add_field(name="**.rob `<@USER>`**", value="Steal someones money", inline=False)
        page3.add_field(name="**.shophelp**", value="Checkout the giftshop", inline=False)
        page3.add_field(name="**.leaderboard**", value="See who's the richest", inline=False)
        page3.set_footer(text="@Mush if you wanna suggest something")

        page4 = discord.Embed(title="**Page 4 | _Shop Commands__**", color=0x01a500)
        page4.set_author(name="Commands List")
        page4.set_thumbnail(url="https://cdn.frankerfacez.com/emoticon/388352/4")
        page4.add_field(name="**.shop**", value="See what roles are for sale", inline=False)
        page4.add_field(name="**.buy `<@ROLE>`\`'ROLE NAME'`**", value="Buy a role from the shop. If role isn't mentionably surround role name with quotes", inline=False)
        page4.set_footer(text="@Mush if you wanna suggest something")

        self.client.help_pages = [page1, page2, page3, page4]
        buttons = [u"\u2B05", u"\u27A1"] # skip to start, left, right, skip to end
        current = 0
        msg = await ctx.send(embed=self.client.help_pages[current])
        
        for button in buttons:
            await msg.add_reaction(button)
            
        while True:
            try:
                reaction, user = await self.client.wait_for("reaction_add", check=lambda reaction, user: user == ctx.author and reaction.emoji in buttons, timeout=60.0)

            except asyncio.TimeoutError:
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


def setup(client):
    client.add_cog(Help(client))