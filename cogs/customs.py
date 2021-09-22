import discord
import random
from discord.ext import commands

class Customs(commands.Cog):

    def __init__(self, client):
        self.client = client

    #Yumi Command
    @commands.cooldown(1, 10, commands.BucketType.member)
    @commands.command()
    async def yumi(self, ctx):
        from cogs.Lists.lists import yumi
        ranyumi = random.choice(yumi)
        await ctx.send(ranyumi)

    #Cabby Command
    @commands.cooldown(1, 15, commands.BucketType.member)
    @commands.command()
    async def cabby(self, ctx):
        from cogs.Lists.lists import cabgif
        rancab = random.choice(cabgif)
        await ctx.send(rancab)

    #Chea Command
    @commands.cooldown(1, 30, commands.BucketType.member)
    @commands.command()
    async def chea(self, ctx):
        embed=discord.Embed(title="**CHEA**", color=discord.Colour.random())
        embed.set_image(url="https://cdn.discordapp.com/attachments/830924379898380298/832695027641745408/image0.gif")
        await ctx.send(embed=embed)

    #Wisdom Command
    @commands.command(aliases = ["moggles","mog"])
    @commands.cooldown(1, 30, commands.BucketType.member)
    async def mogwisdom(self, ctx):
        from cogs.Lists.lists import moglist
        ranmog = random.choice(moglist)
        await ctx.send(f"```fix\n {ranmog}```")

    #Squishy
    @commands.command()
    async def bread(self, ctx):
        bread = [
            "https://cdn.discordapp.com/attachments/820153490747031554/832773597805936708/video0.mp4",
            "https://cdn.discordapp.com/attachments/820153490747031554/820163209704898580/video0.mp4",
            "https://cdn.discordapp.com/attachments/820153490747031554/820163181582090260/video0.mp4"
        ]
        ranbread = random.choice(bread)
        await ctx.send(ranbread)

    #Annie
    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.member)
    async def annie(self, ctx):
        if ctx.author.id == 507016626034573312:
            await ctx.send("**FUN FACT: Annie is 5'3**")
        else:
            from cogs.Lists.annie import embedlist
            ranembed = random.choice(embedlist)
            await ctx.send(embed=ranembed)

    #Angie
    @commands.command(aliases = ["ang"])
    async def angie(self, ctx):
        from cogs.Lists.lists import angie
        ranang = random.choice(angie)
        await ctx.send(f"<@303208527126855680> {ranang}")

    #Sleppy
    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.member)
    async def sleppy(self, ctx):
        await ctx.send("*Swag*")

    #Dev
    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.member)
    async def dev(self, ctx):
        from cogs.Lists.lists import gymgifs
        rangym = random.choice(gymgifs)
        yee = "<a:PEPEYEE:833943064002691113>"
        embed=discord.Embed(description=f"***{yee}{yee}{yee} GREEK GOD SUMMER {yee}{yee}{yee}***", color=discord.Colour.random())
        embed.set_image(url=f"{rangym}")
        await ctx.send(embed=embed)

    #Patricks Songs
    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.member)
    async def patrick(self,ctx):
        if ".patrick playlist" in ctx.message.content:
            await ctx.send(
                "https://open.spotify.com/playlist/5wMtOKDDtDUxkwPNGoCW43?si=a6801fd738264eff"
            )
        else:
            from cogs.Lists.lists import songs
            from cogs.Lists.lists import patrick
            ranpatrick = random.choice(patrick)
            ransong = random.choice(songs)
            await ctx.send(f"**{ranpatrick}**\n{ransong}")

    #Goose
    @commands.command()
    async def gooseupload(self,ctx, arg1):
        if ctx.author.id == 569792736367083560:
            f = open("goose.txt", "a")
            f.truncate(0)
            f.write(arg1)
            f.close()
            #open and read the file after the appending:
            f = open("goose.txt", "r")
            await ctx.message.delete()
            await ctx.send("Succesfully updated", delete_after=2)
        elif ctx.author.id == 250432585006579712:
            f = open("goose.txt", "a")
            f.truncate(0)
            f.write(arg1)
            f.close()
            #open and read the file after the appending:
            f = open("goose.txt", "r")
            await ctx.message.delete()
            await ctx.send("Succesfully updated", delete_after=2)
        else:
            await ctx.send("You cant use this command")

    @commands.command()
    async def goose(self, ctx):
        if ".goose playlist" in ctx.message.content:
            await ctx.send("https://open.spotify.com/playlist/5g1NWwu5lNy18uxtEoHzzv?si=Dki9DiPeSICCUqB1svpvyQ")
        else:
            f = open("goose.txt", "r")
            goosesong = f.read()
            await ctx.send(f"**Goose's Song of The Day:**\n{goosesong}")

    #Sara
    @commands.command(aliases=['nuggies'])
    async def sarah(self,ctx):
        if "557976700286140426" in ctx.message.content:
            from cogs.Lists.lists import saragifs
            ransara = random.choice(saragifs)
            await ctx.send(f"<@557976700286140426> {ransara}")
        else:
            from cogs.Lists.lists import nuggies
            rannug = random.choice(nuggies)
            await ctx.send(rannug)

    #Zhu
    @commands.command()
    async def zhu(self, ctx, arg1=None):
        if arg1 == None:
            embed = discord.Embed(title="**Usage:**", description=".zhu `@USER`", color=discord.Colour.random())
            await ctx.reply(embed=embed)
            return
        await ctx.send(f"Hey {arg1}, drink some joose <:juice:833807080950595594>")

    #Bubu
    @commands.command()
    async def bubu(self, ctx):
        from cogs.Lists.lists import lines
        ranline = random.choice(lines)
        await ctx.send(ranline)


    #Dahlia
    @commands.command()
    async def dahlia(self, ctx):
        await ctx.send("‎‎‎‎‎")

    #Waylan
    @commands.command(aliases=["simp"])
    @commands.cooldown(1, 5, commands.BucketType.member)
    async def waylan(self, ctx):
        from cogs.Lists.lists import waylan
        ranway = random.choice(waylan)
        await ctx.send(ranway)

    #Oen
    @commands.command()
    @commands.cooldown(1, 20, commands.BucketType.member)
    async def oen(self, ctx):
        await ctx.send("https://cdn.discordapp.com/attachments/832138050410381312/837822451873742889/oen.png")

    #Soda 
    @commands.command()
    @commands.cooldown(1, 20, commands.BucketType.member)
    async def soda(self, ctx):
        await ctx.send("https://cdn.discordapp.com/attachments/766731745542275113/837824769193279538/unknown.png")

    #Burg
    @commands.command()
    @commands.cooldown(1,10, commands.BucketType.member)
    async def burg(self, ctx):
        from cogs.Lists.lists import burg
        ranburg = random.choice(burg)
        await ctx.send(ranburg)

    #Jeff
    @commands.command()
    @commands.cooldown(1,10, commands.BucketType.member)
    async def jeff(self, ctx):
        embed = discord.Embed(color=discord.Colour.random())
        embed.set_image(url='https://cdn.discordapp.com/emojis/824637380652433409.gif?v=1')
        await ctx.send(embed=embed)

    #Franny
    @commands.command()
    @commands.cooldown(1,10, commands.BucketType.member)
    async def franny(self, ctx):
        from cogs.Lists.lists import franny
        rangym = random.choice(franny)
        embed=discord.Embed(description=f"**No Concert**", color=discord.Colour.random())
        embed.set_image(url=f"{rangym}")
        await ctx.send(embed=embed)

    #AFL
    @commands.command()
    @commands.cooldown(1, 20, commands.BucketType.member)
    async def afl(self, ctx):
        await ctx.send("https://cdn.discordapp.com/attachments/832138050410381312/889336589082329158/unknown.png")




def setup(client):
    client.add_cog(Customs(client))