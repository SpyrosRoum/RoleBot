import discord
from discord.ext import commands


class Names(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def change_region(self, member: discord.Member, new_region):
        regions = ["[EU]", "[SA]", "[AF]", "[NA]", "[NE]", "[AS]", "[OC]"]
        regions.remove(new_region)
        platforms = ["[PC]", "[XBOX]", "[PS4]"]

        if new_region in member.display_name:
            new = member.display_name.replace(new_region, "")
            return new

        old = member.display_name.split()
        old_platforms = filter(lambda w: w in platforms, old)

        new = " ".join(old_platforms)
        new += f" {new_region}" 
        
        for word in old:
            if word not in regions and word not in platforms: 
                new += f" {word}"
        
        return new
        

    def change_plat(self, member: discord.Member, new_plat):
        if new_plat in member.display_name:
            new = member.display_name.replace(new_plat, "")
            return new

        return f"{new_plat} {member.display_name}"

    @commands.command(brief='')
    async def EU(self, ctx):
        """EU"""
        member = ctx.author
        await member.edit(nick=self.change_region(member, "[EU]"))

    @commands.command(brief='')
    async def SA(self, ctx):
        """SA"""
        member = ctx.author
        await member.edit(nick=self.change_region(member, "[SA]"))

    @commands.command(brief='')
    async def AF(self, ctx):
        """AF"""
        member = ctx.author
        await member.edit(nick=self.change_region(member, "[AF]"))

    @commands.command(brief='')
    async def NA(self, ctx):
        """NA"""
        member = ctx.author
        await member.edit(nick=self.change_region(member, "[NA]"))

    @commands.command(brief='')
    async def NE(self, ctx):
        """NE"""
        member = ctx.author
        await member.edit(nick=self.change_region(member, "[NE]"))

    @commands.command(brief='')
    async def AS(self, ctx):
        """AS"""
        member = ctx.author
        await member.edit(nick=self.change_region(member, "[AS]"))

    @commands.command(brief='')
    async def OC(self, ctx):
        """OC"""
        member = ctx.author
        await member.edit(nick=self.change_region(member, "[OC]"))

    @commands.command(brief='')
    async def PC(self, ctx):
        """PC"""
        member = ctx.author
        await member.edit(nick=self.change_plat(member, "[PC]"))
        

    @commands.command(brief='')
    async def ps4(self, ctx):
        """ps4"""
        member = ctx.author
        await member.edit(nick=self.change_plat(member, "[PS4]"))

    @commands.command(brief='')
    async def xbox(self, ctx):
        """xbox"""
        member = ctx.author
        await member.edit(nick=self.change_plat(member, "[XBOX]"))

def setup(bot):
    bot.add_cog(Names(bot))


