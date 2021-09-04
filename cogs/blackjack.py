import discord
import asyncio
import random
from discord.ext import commands
from cogs.Lists.functions import update_bank

gold = 0xFFD700
red = 0xFF0000
cyan = 0x00ffff

class blackjack(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases = ["bj"])
    async def blackjack(self,ctx, amount = None):
        if amount == None:
            embed = discord.Embed(description="• **.blackjack** `AMOUNT`\n• Aliases = `.bj`", color=red)
            embed.set_author(name = "BlackJack Usage:",icon_url=ctx.author.avatar_url)
            await ctx.reply(embed=embed)
            return

        bal = await update_bank(ctx,ctx.author.id,0,0)
        amount = int(amount)

        if amount>bal[0]:
            embed = discord.Embed(description="You don't have that much!", color=red)
            embed.set_author(name = "BlackJack",icon_url=ctx.author.avatar_url)
            await ctx.reply(embed=embed)
            return
        if amount<0:
            embed = discord.Embed(description="You can't put a negative!!", color=red)
            embed.set_author(name = "BlackJack",icon_url=ctx.author.avatar_url)
            await ctx.reply(embed=embed)
            return

        await update_bank(ctx,ctx.author.id,-1*amount,0)

        # The Card class definition
        class Card:
            def __init__(self, suit, value, card_value):
                
                # Suit of the Card like Spades and Clubs
                self.suit = suit
        
                # Representing Value of the Card like A for Ace, K for King
                self.value = value
        
                # Score Value for the Card like 10 for King
                self.card_value = card_value
            # Function to await ctx.send the cards
        async def print_cards(cards, hidden):
                
            s = ""
            for card in cards:
                if card.value == '10':
                    s = s + " **|{}{}|** ".format(card.value,card.suit)
                else:
                    s = s + " **|{}{}|** ".format(card.value,card.suit)
            return s     
            
        
            

        # Cards for both dealer and player
        player_cards = []
        dealer_cards = []

        # Scores for both dealer and player
        player_score = 0
        dealer_score = 0

        # The type of suit
        suits = ["Spades", "Hearts", "Clubs", "Diamonds"]
    
        # The suit value 
        suits_values = {"Spades":"\u2664", "Hearts":"\u2661", "Clubs": "\u2667", "Diamonds": "\u2662"}
    
        # The type of card
        cards = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
    
        # The card value
        cards_values = {"A": 11, "2":2, "3":3, "4":4, "5":5, "6":6, "7":7, "8":8, "9":9, "10":10, "J":10, "Q":10, "K":10}
    
        # The deck of cards
        deck = []
    
        # Loop for every type of suit
        for suit in suits:
    
            # Loop for every type of card in a suit
            for card in cards:
    
                # Adding card to the deck
                deck.append(Card(suits_values[suit], card, cards_values[card]))
        

        # Initial dealing for player and dealer
        while len(player_cards) < 2:

            # Randomly dealing a card
            player_card = random.choice(deck)
            player_cards.append(player_card)
            deck.remove(player_card)
            player_card1 = random.choice(deck)
            player_cards.append(player_card1)
            deck.remove(player_card1)
            # Updating the player score
            player_score += player_card.card_value  + player_card1.card_value

            # In case both the cards are Ace, make the first ace value as 1 
            if len(player_cards) == 2:
                if player_cards[0].card_value == 11 and player_cards[1].card_value == 11:
                    player_cards[0].card_value = 1
                    player_score -= 10

            # await ctx.send player cards and score 
            slots = "<a:slots:847746097711677461>"
            embed = discord.Embed(title=f"{slots} MushBall's Casino {slots}",description="**:gem:__BlackJack__:gem:**", color=0x00ffff)
            embed.add_field(name=f"{ctx.author.name}'s Cards': (**{player_score}**)",value=f"{await print_cards(player_cards, False)}",inline=False)
            # await ctx.send(f"PLAYER CARDS: {await print_cards(player_cards, False)}\nPLAYER SCORE = {player_score}")

            # Randomly dealing a card
            dealer_card = random.choice(deck)
            dealer_cards.append(dealer_card)
            deck.remove(dealer_card)
            dealer_card1 = random.choice(deck)
            dealer_cards.append(dealer_card1)
            deck.remove(dealer_card1)

            # Updating the dealer score
            dealer_score += dealer_card.card_value + dealer_card1.card_value

            # await ctx.send dealer cards and score, keeping in mind to hide the second card and score
            embed.add_field(name=f"Dealer's Cards': (**{dealer_score}**)",value=f"{await print_cards(dealer_cards, False)}",inline=False)
            await ctx.send(embed=embed)     
            
            # In case both the cards are Ace, make the second ace value as 1 
            if len(dealer_cards) == 2:
                if dealer_cards[0].card_value == 11 and dealer_cards[1].card_value == 11:
                    dealer_cards[1].card_value = 1
                    dealer_score -= 10


        # Player gets a blackjack   
        if player_score == 21:
            embed = discord.Embed(title=f"{slots} MushBall's Casino {slots}",description="**:gem:__BlackJack__:gem:**", color=0xFFD700)
            embed.add_field(name=f"{ctx.author.name}'s Cards': (**{player_score}**)",value=f"{await print_cards(player_cards, False)}",inline=False)
            embed.add_field(name=f"Dealer's Cards': (**{dealer_score}**)",value=f"{await print_cards(dealer_cards, False)}",inline=False)
            embed.set_footer(text=f"You won ${format (2*amount, ',d')}")
            await ctx.send(embed=embed)
            await update_bank(ctx,ctx.author.id,2*amount,0)
            return


        # Managing the player moves
        while player_score < 21:
            def check(message):
                return message.author == ctx.author and message.content.lower() in ['stand', 'hit']
            await asyncio.sleep(0.5)
            await ctx.reply('Would you like to hit or stand?')

            try:
                message = await self.client.wait_for('message', check=check, timeout= 30)
            except asyncio.TimeoutError:
                await ctx.reply("You didn't make a decision fast enough")

            choice = message.content

        
            # If player decides to HIT
            if choice.upper() in ('HIT','H'):
                await asyncio.sleep(1.0)
                # Dealing a new card
                player_card = random.choice(deck)
                player_cards.append(player_card)
                deck.remove(player_card)

                # Updating player score
                player_score += player_card.card_value

                # Updating player score in case player's card have ace in them
                c = 0
                while player_score > 21 and c < len(player_cards):
                    if player_cards[c].card_value == 11:
                        player_cards[c].card_value = 1
                        player_score -= 10
                        c += 1
                    else:
                        c += 1 

                # Check if player busts
                if player_score > 21:
                    embed = discord.Embed(title=f"{slots} MushBall's Casino {slots}",description="**:gem:__BlackJack__:gem:**", color=0xff0000)
                    embed.add_field(name=f"{ctx.author.name}'s Cards': (**{player_score}**)",value=f"{await print_cards(player_cards, False)}",inline=False)
                    embed.add_field(name=f"Dealer's Cards': (**{dealer_score}**)",value=f"{await print_cards(dealer_cards, False)}",inline=False)
                    embed.set_footer(text="You bust, sucks to suck")
                    await ctx.send(embed=embed)
                    return
                        

                # await ctx.send player and dealer cards
                embed = discord.Embed(title=f"{slots} MushBall's Casino {slots}",description="**:gem:__BlackJack__:gem:**", color=0x00ffff)
                embed.add_field(name=f"{ctx.author.name}'s Cards': (**{player_score}**)",value=f"{await print_cards(player_cards, False)}",inline=False)
                embed.add_field(name=f"Dealer's Cards': (**{dealer_score}**)",value=f"{await print_cards(dealer_cards, False)}",inline=False)
                await ctx.send(embed=embed)
            
            
                
            # If player decides to Stand
            if choice.upper() in ('STAND','S'):
                await asyncio.sleep(1.0)
                break
            

        # Check if player has a Blackjack
        if player_score == 21:
            embed = discord.Embed(title=f"{slots} MushBall's Casino {slots}",description="**:gem:__BlackJack__:gem:**", color=0xFFD700)
            embed.add_field(name=f"{ctx.author.name}'s Cards': (**{player_score}**)",value=f"{await print_cards(player_cards, False)}",inline=False)
            embed.add_field(name=f"Dealer's Cards': (**{dealer_score}**)",value=f"{await print_cards(dealer_cards, False)}",inline=False)
            embed.set_footer(text=f"You won ${format (2*amount, ',d')}")
            await ctx.send(embed=embed)
            await update_bank(ctx,ctx.author.id,2*amount,0)
            return
            

        # Check if player busts
        if player_score > 21:
            embed = discord.Embed(title=f"{slots} MushBall's Casino {slots}",description="**:gem:__BlackJack__:gem:**", color=0xff0000)
            embed.add_field(name=f"{ctx.author.name}'s Cards': (**{player_score}**)",value=f"{await print_cards(player_cards, False)}",inline=False)
            embed.add_field(name=f"Dealer's Cards': (**{dealer_score}**)",value=f"{await print_cards(dealer_cards, False)}",inline=False)
            embed.set_footer(text="You bust, sucks to suck")
            await ctx.send(embed=embed)
            return


        # Managing the dealer moves
        while dealer_score < 17:
            # Dealing card for dealer
            dealer_card = random.choice(deck)
            dealer_cards.append(dealer_card)
            deck.remove(dealer_card)

            # Updating the dealer's score
            dealer_score += dealer_card.card_value

            # Updating player score in case player's card have ace in them
            c = 0
            while dealer_score > 21 and c < len(dealer_cards):
                if dealer_cards[c].card_value == 11:
                    dealer_cards[c].card_value = 1
                    dealer_score -= 10
                    c += 1
                else:
                    c += 1

            # Send player and dealer cards
            if dealer_score > 17:
                # Player Wins
                if player_score > dealer_score:
                    embed = discord.Embed(title=f"{slots} MushBall's Casino {slots}",description="**:gem:__BlackJack__:gem:**", color=0xFFD700)
                    embed.add_field(name=f"{ctx.author.name}'s Cards': (**{player_score}**)",value=f"{await print_cards(player_cards, False)}",inline=False)
                    embed.add_field(name=f"Dealer's Cards': (**{dealer_score}**)",value=f"{await print_cards(dealer_cards, False)}",inline=False)
                    embed.set_footer(text=f"You won ${format (2*amount, ',d')}")
                    await update_bank(ctx,ctx.author.id,2*amount,0)
                    await ctx.send(embed=embed)
                    return   

                # Dealer busts
                if dealer_score > 21:        
                    embed = discord.Embed(title=f"{slots} MushBall's Casino {slots}",description="**:gem:__BlackJack__:gem:**", color=0xFFD700)
                    embed.add_field(name=f"{ctx.author.name}'s Cards': (**{player_score}**)",value=f"{await print_cards(player_cards, False)}",inline=False)
                    embed.add_field(name=f"Dealer's Cards': (**{dealer_score}**)",value=f"{await print_cards(dealer_cards, False)}",inline=False)
                    embed.set_footer(text=f"The dealer busts, you won ${format (2*amount, ',d')}")
                    await update_bank(ctx,ctx.author.id,2*amount,0)
                    await ctx.send(embed=embed)
                    return 
        

        # Dealer busts
        if dealer_score > 21:        
            embed = discord.Embed(title=f"{slots} MushBall's Casino {slots}",description="**:gem:__BlackJack__:gem:**", color=0xFFD700)
            embed.add_field(name=f"{ctx.author.name}'s Cards': (**{player_score}**)",value=f"{await print_cards(player_cards, False)}",inline=False)
            embed.add_field(name=f"Dealer's Cards': (**{dealer_score}**)",value=f"{await print_cards(dealer_cards, False)}",inline=False)
            embed.set_footer(text=f"The dealer busts, you won ${format (2*amount, ',d')}")
            await update_bank(ctx,ctx.author.id,2*amount,0)
            await ctx.send(embed=embed)
            return

        # Dealer gets a blackjack
        if dealer_score == 21:
            embed = discord.Embed(title=f"{slots} MushBall's Casino {slots}",description="**:gem:__BlackJack__:gem:**", color=0xff0000)
            embed.add_field(name=f"{ctx.author.name}'s Cards': (**{player_score}**)",value=f"{await print_cards(player_cards, False)}",inline=False)
            embed.add_field(name=f"Dealer's Cards': (**{dealer_score}**)",value=f"{await print_cards(dealer_cards, False)}",inline=False)
            embed.set_footer(text="The dealer won, sucks to suck")
            await ctx.send(embed=embed)
            return
        # TIE Game
        if dealer_score == player_score:
            embed = discord.Embed(title=f"{slots} MushBall's Casino {slots}",description="**:gem:__BlackJack__:gem:**", color=0x00ffff)
            embed.add_field(name=f"{ctx.author.name}'s Cards': (**{player_score}**)",value=f"{await print_cards(player_cards, False)}",inline=False)
            embed.add_field(name=f"Dealer's Cards': (**{dealer_score}**)",value=f"{await print_cards(dealer_cards, False)}",inline=False)
            embed.set_footer(text="It's a tie, gamble some more")
            await ctx.send(embed=embed)
            await update_bank(ctx,ctx.author.id,amount,0)
            return

        # Player Wins
        elif player_score > dealer_score:
            embed = discord.Embed(title=f"{slots} MushBall's Casino {slots}",description="**:gem:__BlackJack__:gem:**", color=0xFFD700)
            embed.add_field(name=f"{ctx.author.name}'s Cards': (**{player_score}**)",value=f"{await print_cards(player_cards, False)}",inline=False)
            embed.add_field(name=f"Dealer's Cards': (**{dealer_score}**)",value=f"{await print_cards(dealer_cards, False)}",inline=False)
            embed.set_footer(text=f"You won ${format (2*amount, ',d')}")
            await update_bank(ctx,ctx.author.id,2*amount,0)
            await ctx.send(embed=embed)
            return                 

        # Dealer Wins
        else:
            embed = discord.Embed(title=f"{slots} MushBall's Casino {slots}",description="**:gem:__BlackJack__:gem:**", color=0xff0000)
            embed.add_field(name=f"{ctx.author.name}'s Cards': (**{player_score}**)",value=f"{await print_cards(player_cards, False)}",inline=False)
            embed.add_field(name=f"Dealer's Cards': (**{dealer_score}**)",value=f"{await print_cards(dealer_cards, False)}",inline=False)
            embed.set_footer(text="The dealer won, sucks to suck")
            await ctx.send(embed=embed)     
            return  

def setup(client):
    client.add_cog(blackjack(client))