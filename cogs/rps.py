import discord
import asyncio
from discord.ext import commands
from cogs.Lists.functions import update_bank
intents = discord.Intents.default()
intents.members = True


class rps(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def rps(self,ctx, member:discord.Member = None,amount = None):
        try:
            if amount == None:
                embed = discord.Embed(description="• **.rps** `@USER` `AMOUNT`", color=0xFF0000)
                embed.set_author(name = "RPS Usage:",icon_url=ctx.author.avatar_url)
                await ctx.reply(embed=embed)
                return

            amount = int(amount)
            bal = await update_bank(ctx,ctx.author.id,0,0)
            bal2 = await update_bank(ctx,member.id,0,0)

            if amount>bal[0]:
                embed = discord.Embed(description="You don't have that much!", color=0xFF0000)
                embed.set_author(name = "Rock Paper Scissors",icon_url=ctx.author.avatar_url)
                await ctx.reply(embed=embed)
                return
            if amount<0:
                embed = discord.Embed(description="You can't put a negative!", color=0xFF0000)
                embed.set_author(name = "Rock Paper Scissors",icon_url=ctx.author.avatar_url)
                await ctx.reply(embed=embed)
                return

            embed = discord.Embed(title=f":rock::newspaper::scissors: Rock Paper Scissors :scissors::newspaper::rock:",description = f"{ctx.author.mention} wants to play with {member.mention}",  color=discord.Colour.random())
            embed.set_footer(text="React with your answer")
            buttons = [u"\U0001f44d",u"\U0001F44E"] 

            msg = await ctx.send(embed=embed)
            
            for button in buttons:
                await msg.add_reaction(button)
                
            while True:
                try:
                    reaction, user = await self.client.wait_for("reaction_add", check=lambda reaction, user: user == member and reaction.emoji in buttons, timeout=60.0)

                except asyncio.TimeoutError:
                    await ctx.reply("Player didn't reply fast enough")
                    return 

                else:

                    if reaction.emoji == u"\U0001f44d":
                        await msg.clear_reactions()
                        if amount>bal2[0]:
                            embed1 = discord.Embed(title=f":rock::newspaper::scissors: Rock Paper Scissors :scissors::newspaper::rock:", color=discord.Colour.random())
                            embed1.add_field(name="‎‎‎‎‎‎‎‎‎‎‎‎‎‎",value=f"{member.mention} doesn't have ${format (amount, ',d')}",inline=False)
                            await msg.edit(embed=embed1)
                            return

                        #Checks
                        channel = member.dm_channel
                        if channel is None:
                            channel = await member.create_dm()

                        #Sends DM
                        embed2 = discord.Embed(title=f":rock::newspaper::scissors: Rock Paper Scissors :scissors::newspaper::rock:",description=f"Waiting for {ctx.author.mention}'s choice", color=discord.Colour.random())
                        await msg.edit(embed=embed2)

                        dmembed = discord.Embed(title=f":rock::newspaper::scissors: Rock Paper Scissors :scissors::newspaper::rock:", color=discord.Colour.random())
                        dmembed.set_footer(text="React with your answer")

                        dm1 = await ctx.author.send(embed=dmembed)
                        dmbutton = [u"\U0001FAA8",u"\U0001F4F0",u"\u2702"] 
                        for button in dmbutton:
                            await dm1.add_reaction(button)

                        try:
                            response, user = await self.client.wait_for("reaction_add", check=lambda reaction, user: user == ctx.author and reaction.emoji in dmbutton, timeout=60.0)
                            
                            #Sends 2nd DM
                            embed3 = discord.Embed(title=f":rock::newspaper::scissors: Rock Paper Scissors :scissors::newspaper::rock:", description=f"{ctx.author.mention} made their choice! Waiting for {member.mention}'s choice", color=discord.Colour.random())
                            await msg.edit(embed=embed3)
                            
                            dm2 = await channel.send(embed = dmembed)
                            for button in dmbutton:
                                await dm2.add_reaction(button)
                            
                            response2, user = await self.client.wait_for("reaction_add", check=lambda reaction, user: user == member and reaction.emoji in dmbutton, timeout=60.0)
                        except asyncio.TimeoutError:
                            await ctx.reply("Player didn't reply fast enough")
                            return

                        #Logic
                        if response2.emoji == response.emoji:
                            result="It's a Tie, folks"
                            embed4 = discord.Embed(title=f"Rock Paper Scissors", color=discord.Colour.random())
                            embed4.add_field(name=f"{ctx.author.name} Chose:",value=f"{response.emoji}",inline=True)
                            embed4.add_field(name=f"{member.name} Chose:",value=f"{response2.emoji}",inline=True)
                            embed4.add_field(name=f"{result}",value=f"Play again!",inline=False)
                            await msg.edit(embed=embed4)
                            return

                        elif response2.emoji == u"\U0001F4F0" and response.emoji == u"\U0001FAA8":
                            result=member.name+ " Wins!"
                            winner = member
                            loser = ctx.author

                        elif response2.emoji == u"\U0001FAA8" and response.emoji == u"\u2702":
                            result=member.name + " Wins!"
                            winner = member
                            loser = ctx.author

                        elif response2.emoji == u"\u2702" and response.emoji == u"\U0001F4F0":
                            result=member.name + " Wins!"
                            winner = member
                            loser = ctx.author

                        elif response2.emoji == u"\U0001FAA8" and response.emoji == u"\U0001F4F0":
                            result=ctx.author.name + " Wins!"
                            winner = ctx.author
                            loser = member

                        elif response2.emoji == u"\u2702" and response.emoji == u"\U0001FAA8":
                            result=ctx.author.name + " Wins!"
                            winner = ctx.author
                            loser = member

                        elif response2.emoji == u"\U0001F4F0" and response.emoji == u"\u2702":
                            result=ctx.author.name + " Wins!"
                            winner = ctx.author
                            loser = member

                        else:
                            result="Someone did something wrong, try playing again"
                        #Sends Results
                        embed5 = discord.Embed(title=f":rock::newspaper::scissors: Rock Paper Scissors Results :scissors::newspaper::rock:", color=discord.Colour.random())
                        embed5.add_field(name=f"{ctx.author.name} Chose:",value=f"{response.emoji}",inline=True)
                        embed5.add_field(name=f"{member.name} Chose:",value=f"{response2.emoji}",inline=True)
                        embed5.add_field(name=f":money_with_wings: {result} :money_with_wings:",value=f"`${format (2*amount, ',d')}` has been added into {winner.mention}'s account",inline=False)
                        await msg.edit(embed=embed5)
                        await update_bank(ctx,loser.id,-1*amount,0)
                        await update_bank(ctx,winner.id,amount,0)
                        return
                            
                    elif reaction.emoji == u"\U0001F44E":
                        await msg.clear_reactions()
                        embed6 = discord.Embed(title=f":rock::newspaper::scissors: Rock Paper Scissors :scissors::newspaper::rock:", description=f"{member.mention} doesn't want to play", color=0x00ffff)
                        await msg.edit(embed=embed6)
                        return

                    for button in buttons:
                        await msg.remove_reaction(button, ctx.author)
        except Exception as e:
            print(e)



def setup(client):
    client.add_cog(rps(client))