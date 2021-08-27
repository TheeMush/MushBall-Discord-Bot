import discord
import json
import os
from discord.ext import commands
from discord.ext.commands import MissingPermissions

import discord
import logging

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

intents = discord.Intents.default()
intents.members = True




client = commands.Bot(command_prefix='.', intents=intents)
client.remove_command("help")

#LOG INTO CONSOLE
@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

#Slowdown Message
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CommandOnCooldown):
        if error.retry_after > 60:
            minutes = str(error.retry_after // 60)
            await ctx.send(f"<a:hourglass:857868080435560520> **| Cooldown** {minutes} minutes")
        else:
            await ctx.send(f"<a:hourglass:857868080435560520> **| Cooldown:** {round(error.retry_after)} seconds")
            return

#COG COMMANDS
@client.command()
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')
    await ctx.send("Loaded")
@client.command()
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')
    await ctx.send("Unloaded")
@client.command()
async def reload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')
    client.load_extension(f'cogs.{extension}')
    await ctx.send("Reloaded")
for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        if filename.startswith('__init__'):
            pass
        client.load_extension(f'cogs.{filename[:-3]}')

#Token
with open('token.json') as f:
    data = json.load(f)
    token = data["TOKEN"]

client.run(token)
