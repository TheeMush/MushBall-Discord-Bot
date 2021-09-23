import discord
import asyncio
import random
import traceback
import math
from discord.ext import commands
from cogs.Lists.functions import update_bank
from cogs.Lists.functions import update_luck


gold = 0xFFD700
red = 0xFF0000
cyan = 0x00ffff
rcolor = discord.Colour.random()

class games(commands.Cog):

    def __init__(self, client):
        self.client = client

    #Beg command
    @commands.command()
    @commands.cooldown(1, 20, commands.BucketType.member)
    async def beg(self,ctx):
        try:
            beglist = ["I'm feeling generous, here's","You're begging? How pitiful, here's","I like you, take","And people say I'm not nice, this is for you"]
            beglist2 = ['Imagine begging','Broke ass','Just gamble',"Kinda sad you're begging"]
            takelist = ["What makes you think I'd give you money?","I worked hard for my money, I'm not giving you any","Earn your money the hard way"]
            ransent = random.choice(beglist)

            bal = await update_bank(ctx,ctx.author.id,0,0)
            total = bal[0] + bal[1]

            top_percent = 0.01 * total
            bottom_percent = 0.005 * total

            if total < 1000:
                earnings = random.randrange(100,1000)
            else:
                earnings = random.randrange(int(bottom_percent),int(top_percent))

            if top_percent > 7500:
                earnings = random.randrange(3750,7500)

            if int(top_percent) < 1:
                ranlose = random.randrange(0,(math.ceil(total/10)))
            elif int(bottom_percent) < 1:
                ranlose = random.randrange(0,(math.ceil(total/10)))
            else:
                ranlose = random.randrange(int(bottom_percent),int(top_percent))
            
            if ranlose == 1:
                if earnings > total:
                    earnings = random.randrange(0,(math.ceil(total/6)))

                embed = discord.Embed(title=random.choice(takelist),description=f"You lose `${format (earnings, ',d')}`",color=red)
                embed.set_footer(text=random.choice(beglist2))
                await update_bank(ctx,ctx.author.id,-1*earnings,0)
                await ctx.reply(embed=embed)
                return

            rannum = random.randrange(1,1000)
            if rannum == 666:
                embed = discord.Embed(description='You got lucky and found `$25,000`!',color=rcolor)
                embed.set_footer(text=random.choice(beglist2))
                await ctx.reply(embed=embed)
                await update_bank(ctx,ctx.author.id,25000,0)
                return

            embed = discord.Embed(description=f"{ransent} `${format (earnings, ',d')}`",color=rcolor)
            embed.set_footer(text=random.choice(beglist2))
            await ctx.reply(embed=embed)

            await update_bank(ctx,ctx.author.id,earnings,0)
        except Exception:
            print(f"```{traceback.format_exc()}```")

    #Coinflip Command
    @commands.command(aliases = ["coin"])
    @commands.cooldown(1, 7, commands.BucketType.member)
    async def coinflip(self,ctx,choice = None,amount = None):
        if amount == None:
            embed = discord.Embed(description="• **.coinflip** `HEADS/TAILS` `AMOUNT`\n• Aliases = `.coin`", color=red)
            embed.set_author(name = "Coinflip Usage:",icon_url=ctx.author.avatar_url)
            await ctx.reply(embed=embed)
            self.coinflip.reset_cooldown(ctx)
            return

        bal = await update_bank(ctx,ctx.author.id,0,0)
        luck = await update_luck(ctx,ctx.author.id,0)
        coin = "<a:Coin:847746675598032946>"
        amount = int(amount)

        if amount>bal[0]:
            embed = discord.Embed(description="You don't have that much!", color=red)
            embed.set_author(name = f"Coinlflip",icon_url=ctx.author.avatar_url)
            await ctx.reply(embed=embed)
            self.conflip.reset_cooldown(ctx)
            return
        if amount<0:
            embed = discord.Embed(description="You can't put a negative!", color=red)
            embed.set_author(name = f"Coinlflip",icon_url=ctx.author.avatar_url)
            await ctx.reply(embed=embed)
            self.conflip.reset_cooldown(ctx)
            return

        if choice.lower() == 'head':
            choice = "heads"
        elif choice.lower() == 'tail':
            choice = 'tails'
            
        if luck < 80:
            if choice.lower() == 'heads':
                choices = ["Heads", "Tails","Tails"]
                rancoin = random.choice(choices)
            elif choice.lower() == 'tails':
                choices = ["Heads","Heads","Tails"]
                rancoin = random.choice(choices)
        elif luck < 10:
            if choice.lower() == 'heads':
                rancoin = 'tails'
            elif choice.lower() == 'tails':
                rancoin = random.choice('heads')
        elif luck >= 50:
                choices = ["Heads", "Tails"]
                rancoin = random.choice(choices)
            

        if choice.lower() == rancoin.lower():
            embed=discord.Embed(title=f"{coin} The coin landed on {rancoin} {coin}", description=f"Congrats {ctx.author.mention}, you won **`${format (2*amount, ',d')}`**!", color=gold)
            await ctx.send(embed=embed)
            await update_bank(ctx,ctx.author.id,amount,0)
            await update_luck(ctx,ctx.author.id,-10)
        else:
            embed=discord.Embed(title=f"{coin} The coin landed on {rancoin} {coin}", description=f"Sucks to suck {ctx.author.mention}, you lost your money", color=red)
            await ctx.send(embed=embed)
            await update_bank(ctx,ctx.author.id,-1*amount,0)
            await update_luck(ctx,ctx.author.id,5)

        
        


    #Slots command
    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.member)
    async def slots(self,ctx, amount= None):
        slots = "<a:slots:847746097711677461>"

        if amount == None:
            embed = discord.Embed(description="• **.slots** `AMOUNT`", color=red)
            embed.set_author(name = "Slots Usage:",icon_url=ctx.author.avatar_url)
            await ctx.reply(embed=embed)
            self.slots.reset_cooldown(ctx)
            return

        bal = await update_bank(ctx,ctx.author.id,0,0)
        amount = int(amount)

        if amount>bal[0]:
            embed = discord.Embed(description="You don't have that much!", color=red)
            embed.set_author(name = f"{slots} Slots {slots}",icon_url=ctx.author.avatar_url)
            await ctx.reply(embed=embed)
            self.slots.reset_cooldown(ctx)
            return
        if amount<0:
            embed = discord.Embed(description="You can't put a negative!", color=red)
            embed.set_author(name = f"{slots} Slots {slots}",icon_url=ctx.author.avatar_url)
            await ctx.reply(embed=embed)
            self.slots.reset_cooldown(ctx)
            return

        slot_embed = discord.Embed(title=f"{slots} MushBall's Casino {slots}",description="**__Slot Machine__**", color=0x00ffff)
        slot_embed.add_field(name="Results",value=f"<a:slotemote:847943348009435146> <a:slotemote:847943348009435146> <a:slotemote:847943348009435146>")
        sent_embed = await ctx.send(embed=slot_embed)
        current_slot_pics = ["<a:slotemote:847943348009435146>","<a:slotemote:847943348009435146>","<a:slotemote:847943348009435146>"]
        final=[]
        for i in range(3):
            a = random.choice([":gem:",":dollar:",":moneybag:"])
            final.append(a)

        for i in range(0,len(final)):
            await asyncio.sleep(1.5)
            current_slot_pics[i] = final[i]
            new_slot_embed = None
            new_slot_embed = discord.Embed(title=f"{slots} MushBall's Casino {slots}",description="**__Slot Machine__**",color=0x00ffff)
            slot_results_str = ""        
            for thisSlot in current_slot_pics:
                slot_results_str += f"{thisSlot} "
            new_slot_embed.add_field(name="Results",value=f"{slot_results_str}")
            await sent_embed.edit(embed=new_slot_embed)
                
        if final[0] == final[1] == final[2]:
            await asyncio.sleep(1.5)
            win_slot_embed = None
            win_slot_embed = discord.Embed(title=f"{slots} MushBall's Casino {slots}",description="**__Slot Machine__**", color=0xFFD700)
            win_slot_embed.add_field(name="Results",value=f"{slot_results_str}")
            win_slot_embed.add_field(name=f"Congrats {ctx.author.name}, You Won:",value=f"**:dollar: ``${format (10*amount, ',d')}`` :dollar:**",inline=False)
            await sent_embed.edit(embed=win_slot_embed)
            await update_bank(ctx,ctx.author.id,10*amount,0)
        else:
            await asyncio.sleep(1.5)
            lost_slot_embed = None
            lost_slot_embed = discord.Embed(title=f"{slots} MushBall's Casino {slots}",description="**__Slot Machine__**", color=0xFF0000)
            lost_slot_embed.add_field(name="Results",value=f"{slot_results_str}")
            lost_slot_embed.add_field(name=f"Sorry {ctx.author.name}, you lost", value="Sucks to suck, try again",inline=False)
            await sent_embed.edit(embed=lost_slot_embed)
            await update_bank(ctx,ctx.author.id,-1*amount,0)
   


    #Highlow Command
    @commands.command(aliases = ["hl"])
    #@commands.cooldown(1, 10, commands.BucketType.member)
    async def highlow(self,ctx,amount = None,guess = None,num = None):
        embed = discord.Embed(description="• **.highlow** `<bet amount>` `<high/low>` `<number>`\n• Aliases = `.hl`\n\n**Low** = **1-16**\n**High** = **17-32**\n\n", color=red)
        embed.set_author(name = "HighLow Usage:",icon_url=ctx.author.avatar_url)
        embed.set_footer(text="<number> is optional but you win 10x if you guess correctly")

        if amount == None or guess == None:
            await ctx.reply(embed=embed)
            self.highlow.reset_cooldown(ctx)
            return
        if guess.lower() not in ('high','low'):
            await ctx.reply(embed=embed)
            self.highlow.reset_cooldown(ctx)
            return

        rannum = random.randrange(1,32)
        bal = await update_bank(ctx,ctx.author.id,0,0)
        luck = await update_luck(ctx,ctx.author.id,0)
        amount = int(amount)

        if amount>bal[0]:
            embed = discord.Embed(description="You don't have that much!", color=red)
            embed.set_author(name = "HighLow",icon_url=ctx.author.avatar_url)
            await ctx.reply(embed=embed)
            self.highlow.reset_cooldown(ctx)
            return
        if amount<0:
            embed = discord.Embed(description="You can't put a negative!", color=red)
            embed.set_author(name = "HighLow",icon_url=ctx.author.avatar_url)
            await ctx.reply(embed=embed)
            self.highlow.reset_cooldown(ctx)
            return

        await update_bank(ctx,ctx.author.id,-1*amount,0)

        if num == None:
            intnum = -1
            num = "None"
        else:
            intnum = int(num)

        if rannum > 16:
            outcome = "HIGH"
        else:
            outcome = "LOW"

        if luck < 40:
            if guess.lower() == 'high':
                choices = ["HIGH","LOW", "LOW", "LOW","LOW"]
                outcome = random.choice(choices)
            elif guess.lower() == 'low':
                choices = ["HIGH","HIGH", "HIGH","HIGH","LOW"]
                outcome = random.choice(choices)
                
        if luck < 80:
            if guess.lower() == 'high':
                choices = ["HIGH","LOW", "LOW","LOW","LOW"]
                outcome = random.choice(choices)
            elif guess.lower() == 'low':
                choices = ["HIGH","HIGH", "HIGH","LOW","HIGH"]
                outcome = random.choice(choices)

        
        embed = discord.Embed(title=":arrow_up: High Low :arrow_down:",color=rcolor)
        embed.add_field(name="Your guess:",value=f"**{guess.upper()}**\n**{num}\n**")
        embed.add_field(name="Outcome:",value=f"**{outcome}**\n**{rannum}\n**")
        embed.set_author(name="MushBall's Casino", icon_url=ctx.author.avatar_url)

        
        if intnum == rannum:
            embed.add_field(name=f"You guessed the number correctly! You win :dollar: `${format (10*amount, ',d')}` :dollar:",value="** **",inline=False)
            await update_bank(ctx,ctx.author.id,10*amount,0)
            await update_luck(ctx,ctx.author.id,-20)
        if guess.lower() == 'high' and rannum>16:
            embed.add_field(name=f"You guessed correctly! You win :dollar: `${format (2*amount, ',d')}` :dollar:",value="** **",inline=False)
            await update_bank(ctx,ctx.author.id,2*amount,0)
            await update_luck(ctx,ctx.author.id,-10)
        if guess.lower() == 'low' and rannum<=16:
            embed.add_field(name=f"You guessed correctly! You win :dollar: `${format (2*amount, ',d')}` :dollar:",value="** **",inline=False)
            await update_bank(ctx,ctx.author.id,2*amount,0)
            await update_luck(ctx,ctx.author.id,-10)
        if guess.lower() == 'high' and rannum<=16:
            embed.add_field(name=f"You guessed wrong! Sucks to suck",value="** **",inline=False)
            await update_luck(ctx,ctx.author.id,5)
        if guess.lower() == 'low' and rannum>16:
            embed.add_field(name=f"You guessed wrong! Sucks to suck",value="** **",inline=False)
            await update_luck(ctx,ctx.author.id,5)

        await ctx.send(embed=embed)

    #HIGHLOW ERROR HANDLING
    @highlow.error
    async def highlow_error(self,ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            return
        embed = discord.Embed(description="• **.highlow `<bet amount>` `<high/low>` `<number>`\n• Aliases = `.hl`\n**low** = ***1-16***, **high** = ***17-32***", color=red)
        embed.set_author(name = "HighLow Usage:",icon_url=ctx.author.avatar_url)
        embed.set_footer(text="<number> is optional but you win 10x if you guess correctly")
        await ctx.send(embed=embed)
        print(f"```{traceback.format_exc()}```")


    #Cups Command
    @commands.command(aliases=['cup'])
    @commands.cooldown(1, 7, commands.BucketType.member)
    async def cups(self,ctx, choice = None,amount = None):
        if amount == None:
            embed = discord.Embed(description="• **.cups** `1-4` `AMOUNT`", color=red)
            embed.set_author(name = "Cups Usage:",icon_url=ctx.author.avatar_url)
            await ctx.reply(embed=embed)
            self.cups.reset_cooldown(ctx)
            return

        bal = await update_bank(ctx,ctx.author.id,0,0)
        luck = await update_luck(ctx,ctx.author.id,0)
        amount = int(amount)

        if amount>bal[0]:
            embed = discord.Embed(description="You don't have that much!", color=red)
            embed.set_author(name = "Cups",icon_url=ctx.author.avatar_url)
            await ctx.reply(embed=embed)
            self.cups.reset_cooldown(ctx)
            return
        if amount<0:
            embed = discord.Embed(description="You can't put a negative!", color=red)
            embed.set_author(name = "Cups",icon_url=ctx.author.avatar_url)
            await ctx.reply(embed=embed)
            self.cups.reset_cooldown(ctx)
            return

        choice = int(choice)

        if choice>4:
            embed = discord.Embed(description="• **.cups** `1-4` `AMOUNT`", color=red)
            embed.set_author(name = "Cups Usage:",icon_url=ctx.author.avatar_url)
            await ctx.reply(embed=embed)
            self.cups.reset_cooldown(ctx)
            return

        slots = "<a:slots:847746097711677461>"
        cups = "<a:cups:859332532226621451>"
        slot_embed = discord.Embed(title=f"{slots} MushBall's Casino {slots}",description="**__Cups__**", color=0x00ffff)
        slot_embed.add_field(name="Results",value=f"{cups} {cups} {cups} {cups}")
        sent_embed = await ctx.send(embed=slot_embed)
        await asyncio.sleep(2.5)

        resultsembed = discord.Embed(title=f"{slots} MushBall's Casino {slots}",description="**__Cups__**", color=0x00ffff)

        blue = "<:bluecup:859335158430826517>"
        green = "<:greencup:859335127955537981>"
        purple = "<:purplecup:859335144350679100>"
        up = "<:cupup:859332771063660544>"
        answer = random.randint(1, 4)

        

        if answer == 1:
            resultsembed.add_field(name="Results",value=f"{up} {blue} {green} {purple}")
        elif answer == 2:
            resultsembed.add_field(name="Results",value=f"{blue} {up} {purple} {green}")
        elif answer == 3:
            resultsembed.add_field(name="Results",value=f"{green} {purple} {up} {blue}")
        elif answer == 4:
            resultsembed.add_field(name="Results",value=f"{purple} {green} {blue} {up}")

        await sent_embed.edit(embed=resultsembed)
        await asyncio.sleep(0.5)

        if choice == answer:
            resultsembed.add_field(name=f"Congrats {ctx.author.name}, You Won:",value=f"**:dollar: ``${format (3*amount, ',d')}`` :dollar:**",inline=False)
            await sent_embed.edit(embed=resultsembed)
            await update_bank(ctx,ctx.author.id,-1*amount,0)
            await update_bank(ctx,ctx.author.id,3*amount,0)
            await update_luck(ctx,ctx.author.id,-10)
            return
        else:
            resultsembed.add_field(name=f"Sorry {ctx.author.name}, you lost", value="Sucks to suck, try again",inline=False)
            await sent_embed.edit(embed=resultsembed)
            await update_bank(ctx,ctx.author.id,-1*amount,0)
            await update_luck(ctx,ctx.author.id,5)
            return

    #CUPS ERROR HANDLING
    @cups.error
    async def cups_error(self,ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            return
        embed = discord.Embed(description="• **.cups** `1-4` `AMOUNT`", color=red)
        embed.set_author(name = "Cups Usage:",icon_url=ctx.author.avatar_url)
        await ctx.reply(embed=embed)
        print(f"```{traceback.format_exc()}```")

    @commands.command()
    async def crash(self,ctx,amount = None):
        if amount == None:
            embed = discord.Embed(description="• **.crash** <`AMOUNT`>", color=red)
            embed.set_author(name = "Crash Usage:",icon_url=ctx.author.avatar_url)
            await ctx.reply(embed=embed)
            self.crash.reset_cooldown(ctx)
            return

        bal = await update_bank(ctx,ctx.author.id,0,0)
        amount = int(amount)

        if amount>bal[0]:
            embed = discord.Embed(description="You don't have that much!", color=red)
            embed.set_author(name = "Crash",icon_url=ctx.author.avatar_url)
            await ctx.reply(embed=embed)
            self.crash.reset_cooldown(ctx)
            return
        if amount<0:
            embed = discord.Embed(description="You can't put a negative!", color=red)
            embed.set_author(name = "Crash",icon_url=ctx.author.avatar_url)
            await ctx.reply(embed=embed)
            self.crash.reset_cooldown(ctx)
            return

        #ACTUAL CODE
        
        try:
            msg = await ctx.send('**Starting Crash Game** <a:loading:869964972594192414>')
            await asyncio.sleep(2.9)
            await msg.delete()

            def check(message):
                return message.author == ctx.author 

            await ctx.reply('Enter the number you want to cash out at (Between 1.0-15.0)?')

            try:
                message = await self.client.wait_for('message', check=check, timeout= 30)
            except asyncio.TimeoutError:
                await ctx.reply("You didn't make a decision fast enough")

            choice = message.content

            try:
                choice = float(choice)
                choice = round(choice,1)

                if choice > 15:
                    await ctx.send("Why tf you going over 15.0, the instructions aren't that hard ._.")
                    return
                elif choice < 1:
                    await ctx.send("Are you dumb? Choose something between 1.0 and 15.0")
                    return
            except Exception:
                await ctx.send("You fucked something up, make sure you choose a number between 1.0 and 15.0")
                return
              
            rand = random.randint(1,4)
            if rand == 1:
                x = round(random.uniform(1,1.7), 1)
            elif rand > 2:
                x = round(random.uniform(1,2), 1)
            else:
                x = round(random.uniform(1,15), 1)

            y = 1.0

            emoji = "<a:pepeToiletRocket:890318300402315264>"

            embed = discord.Embed(title = f"{emoji}  __Crash__  {emoji}", color=discord.Colour.random())
            embed.add_field(name='**Your Guess:**', value=choice,inline=True)
            embed.set_author(name = "MushBall's Casino",icon_url=ctx.author.avatar_url)

            message = await ctx.send(embed=embed)

            for z in range(15):
                z += 1
                y = round(y,1)

                embed = discord.Embed(title = f"{emoji}  __Crash__  {emoji}", color=discord.Colour.random())
                embed.add_field(name='**Your Guess:**', value=choice,inline=True)
                embed.add_field(name='**Outcome:**', value=y,inline=True)
                embed.set_author(name = "MushBall's Casino",icon_url=ctx.author.avatar_url)

                await message.edit(embed=embed)

                if y == x:
                    break

                y = y + 0.1
                
                await asyncio.sleep(1)
			
            embed = discord.Embed(title = f"{emoji}  __Crash__  {emoji}", color=discord.Colour.random())
            embed.add_field(name='**Your Guess:**', value=choice,inline=True)
            embed.add_field(name='**Outcome:**', value=x,inline=True)
            embed.set_author(name = "MushBall's Casino",icon_url=ctx.author.avatar_url)

            if choice > x:
                embed.add_field(name="**You Lost! Sucks to suck, try again**",value='** **',inline=False)
                await update_bank(ctx,ctx.author.id,-1*amount,0)
                await message.edit(embed=embed)
            elif choice <= x:
                earnings = math.ceil(choice*amount)
                embed.add_field(name = f"**You Won** ${format (earnings, ',d')}",value='** **',inline=False)
                await message.edit(embed=embed)
                await update_bank(ctx,ctx.author.id,-1*amount,0)
                await update_bank(ctx,ctx.author.id,earnings,0)


        except:
            print(f"```{traceback.format_exc()}```")

        

def setup(client):
    client.add_cog(games(client))