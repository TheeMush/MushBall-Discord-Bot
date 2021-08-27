from discord.ext import commands
import discord
import asyncio
from cogs.Lists.functions import update_bank

gold = 0xFFD700
red = 0xFF0000
cyan = 0x00ffff


class ttt(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def emote(self,ctx):
        up_left = "1\N{variation selector-16}\N{combining enclosing keycap}"
        await ctx.send(up_left)

    @commands.command(aliases=['tictactoe'])
    async def ttt(self,ctx, member: discord.Member = None,amount = None):
        if amount == None:
                embed = discord.Embed(description="• **.tictactoe** `AMOUNT`\n• Aliases = `.ttt`", color=red)
                embed.set_author(name = "TicTacToe Usage:",icon_url=ctx.author.avatar_url)
                await ctx.reply(embed=embed)
                return

        amount = int(amount)
        bal = await update_bank(ctx,ctx.author.id,0,0)
        bal2 = await update_bank(ctx,member.id,0,0)

        if amount>bal[0]:
            embed = discord.Embed(description="You don't have that much!", color=red)
            embed.set_author(name = "TicTacToe",icon_url=ctx.author.avatar_url)
            await ctx.reply(embed=embed)
            return
        if amount<0:
            embed = discord.Embed(description="You can't put a negative!!", color=red)
            embed.set_author(name = "TicTacToe",icon_url=ctx.author.avatar_url)
            await ctx.reply(embed=embed)
            return

        embed = discord.Embed(title=":x::o::x: Tic Tac Toe :x::o::x:", color=cyan)
        embed.add_field(name="‎‎‎‎‎‎‎‎‎‎‎‎‎‎",value=f"{ctx.author.mention} wants to play with {member.mention}",inline=False)
        embed.add_field(name="React with your answer",value="‎‎‎‎‎‎‎‎‎‎‎‎‎‎",inline=False)
        buttons = [u"\U0001f44d",u"\U0001F44E"] 

        msg = await ctx.send(embed=embed)
        
        for button in buttons:
            await msg.add_reaction(button)
            
        while True:
            try:
                reaction, user = await self.client.wait_for("reaction_add", check=lambda reaction, user: user == member and reaction.emoji in buttons, timeout=60.0)

            except asyncio.TimeoutError:
                return 
            
            else:
                if reaction.emoji == u"\U0001f44d":
                    if amount>bal2[0]:
                        embed1 = discord.Embed(title=":x::o::x: Tic Tac Toe :x::o::x:", color=red)
                        embed1.add_field(name="‎‎‎‎‎‎‎‎‎‎‎‎‎‎",value=f"{member.mention} doesn't have ${format (amount, ',d')}",inline=False)
                        await msg.edit(embed=embed1)
                        return

                    await msg.delete()

                    from cogs.TTT.tic_tac_toe import TicTacToe
                    TTT = TicTacToe(ctx, [ctx.author, member],amount)
                    await TTT.start()
                    while TTT.winner == None:
                        await asyncio.sleep(1)

                    await update_bank(ctx,TTT.loser.id,-1*amount,0)
                    await update_bank(ctx,TTT.winner.id,amount,0)


                elif reaction.emoji == u"\U0001F44E":
                        embed6 = discord.Embed(title=":x::o::x: Tic Tac Toe :x::o::x:", description=f"{member.mention} doesn't want to play", color=0x00ffff)
                        await msg.edit(embed=embed6)
                        return          




def setup(bot):
    bot.add_cog(ttt(bot))