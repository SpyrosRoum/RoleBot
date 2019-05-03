import discord
from discord.ext import commands

import json


async def is_guild_owner(ctx):
    return ctx.author.id == ctx.guild.owner.id

class Server_owner(commands.Cog, name="Server Owner"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(brief="Change the prefix for your server")
    @commands.check(is_guild_owner)
    async def prefix(self, ctx, *, pre):
        """prefix [prefix]"""
        with open(r"prefixes.json", 'r') as f:
            prefixes = json.load(f)

        prefixes[str(ctx.guild.id)] = pre
        await ctx.send(f"New prefix is `{pre}`")

        with open(r"prefixes.json", 'w') as f:
            json.dump(prefixes, f, indent=4)


def setup(bot):
	bot.add_cog(Server_owner(bot))
