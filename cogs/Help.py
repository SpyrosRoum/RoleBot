import discord
from discord.ext import commands

import time
import asyncio

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def Nembed(self, ctx, page: int, pages, cogs, cogsD):
        if page + 1 == 1:
            embed = discord.Embed(
                description=f"Prefix: `{ctx.prefix}`\n`[argument]` = required, `(argument)` = optional",
                color=ctx.author.color,
                timestamp=ctx.message.created_at
            )
        else:
            embed = discord.Embed(
                color=ctx.author.color,
                timestamp=ctx.message.created_at
            )
        cog_name = cogs[page].replace("_", " ")
        embed.set_author(
            name=f"Help - {cog_name} - {len(cogsD[cogs[page]])} command(s)",
            icon_url=self.bot.user.avatar_url
        )
        embed.set_footer(text=f"Page {page+1}/{pages}")

        for command in cogsD[cogs[page]]:
            aliases = "None" if not command.aliases else [f"`{al}`" for al in command.aliases]
            embed.add_field(name=f'{command.name if not command.name == "show" else "show all"}', 
                            value=f"`{ctx.prefix}{command.help}`\n{command.brief}\nAliases: {'None' if aliases == 'None' else ', '.join(aliases)}")
        return embed

    @commands.command(name="help", aliases=["h"], brief="Display this message", hidden=True)
    async def help_(self, ctx, *, command=None):
        '''help'''
        # prefix = await self.bot.pg_con.fetchval(
        #     """
        #     SELECT prefix
        #       FROM prefixes
        #      WHERE id = $1
        #     """, ctx.guild.id
        # )
        # ctx.prefix = prefix or self.bot.prefix

        if not command:
            commands_ = [c for c in self.bot.commands if bool(c.cog_name) and not c.hidden and await c.can_run(ctx)]
            # commands_ = [c for c in self.bot.commands if bool(c.cog_name) and not c.hidden]
            cogs = [cog for cog in set([command.cog_name for command in commands_])]

            cogsD = {}
            for cog in cogs:
                cogsD[cog] = []
                for command in commands_:
                    if command.cog_name == cog:
                        cogsD[cog].append(command)

            pages = len(cogsD)
            page = 0

            embed = self.Nembed(ctx, page, pages, cogs, cogsD)
            msg = await ctx.send(embed=embed)

            await msg.add_reaction('⬅')
            await msg.add_reaction('➡')
            await msg.add_reaction('❌')

            def check(r, user):
                return user != self.bot.user and r.message.id == msg.id

            t_end = time.time() + 180
            while time.time() < t_end:
                try:
                    res, user = await self.bot.wait_for('reaction_add', check=check, timeout=60.0)
                except asyncio.TimeoutError:
                    continue
                    
                if str(res.emoji) == "➡":
                    try:
                        await msg.remove_reaction('➡', user)
                    except discord.Forbidden:
                        pass
                    page += 1

                    if page == pages:
                        page -= 1

                    new_embed = self.Nembed(ctx, page, pages, cogs, cogsD)
                    await msg.edit(embed=new_embed)

                elif str(res.emoji) == "⬅":
                    try:
                        await msg.remove_reaction('⬅', user)
                    except discord.Forbidden:
                        pass
                    
                    page -= 1
                    if page < 0:
                        page = 0

                    new_embed = self.Nembed(ctx, page, pages, cogs, cogsD)
                    await msg.edit(embed=new_embed)

                elif str(res.emoji) == "❌":
                    try:
                        await msg.remove_reaction("❌", user)
                    except discord.Forbidden:
                        pass
                    
                    break

            await msg.remove_reaction('⬅', self.bot.user)
            await msg.remove_reaction('➡', self.bot.user)
            await msg.remove_reaction("❌", self.bot.user)
            await msg.edit(content=f"Type `{ctx.prefix}help` or `{ctx.prefix}h`", embed=None)
        else:
            command = self.bot.get_command(command)

            if not command:
                await ctx.send(f"Use the right command derpy, try `{ctx.prefix}help`")
                return

            sub_commands = []
            if isinstance(command, commands.Group):
                sub_commands = list(command.commands) 


            embed = discord.Embed(
                description=f"Prefix: `{ctx.prefix}`\n`[argument]` = required, `(argument)` = optional",
                color=ctx.author.color,
                timestamp=ctx.message.created_at
            )

            aliases = "None" if not command.aliases else [f"`{al}`" for al in command.aliases]

            embed.add_field(
                name=command.name, 
                value=f"`{ctx.prefix}{command.help}`\n{command.brief}\nAliases: {'None' if aliases == 'None' else ', '.join(aliases)}", 
            )

            for command in sub_commands:
                embed.add_field(
                    name=f"**{command.name}**", 
                    value=f"`{ctx.prefix}{command.help}`\n{command.brief}\nAliases: {'None' if aliases == 'None' else ', '.join(aliases)}",
                    inline=False
                )
            
            await ctx.send(embed=embed)
                        


def setup(bot):
    bot.add_cog(Help(bot))
