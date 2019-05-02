import discord
from discord.ext import commands

import asyncio

import os

import json


def get_prefix(bot, message):
    if not message.guild:
        return commands.when_mentioned_or(":")(bot, message)

    with open("prefixes.json", 'r') as f:
        prefixes = json.load(f)

    if str(message.guild.id) not in prefixes:
        return commands.when_mentioned_or(":")(bot, message)

    prefix = prefixes[str(message.guild.id)]
    return commands.when_mentioned_or(prefix)(bot, message)

bot = commands.Bot(command_prefix=get_prefix)
TOKEN = open("TOKEN.TXT", "r").read()


bot.remove_command('help')

@bot.event
async def on_ready():
    print("Logged in as")
    print(bot.user.name)
    print("------------")


@bot.command(name="reload")
@commands.is_owner()
async def _reload(ctx, module):
    try:
        module = module.lower().title()
        bot.reload_extension("cogs." + module)
        await ctx.send(f"{module} reloaded")
    except Exception as e:
        await ctx.send('\N{PISTOL}')
        await ctx.send(f'{type(e).__name__}: {e}')
        raise e


for cog in os.listdir(".\\cogs"):
    if cog.endswith(".py") and not cog.startswith("_"):
        try:
            cog = f"cogs.{cog.replace('.py', '')}"
            bot.load_extension(cog)
        except Exception as e:
            print(f"{cog} can not be loaded:")
            raise e

bot.run(TOKEN)
