from discord.ext import commands
from templatebot import Bot

config_response = """
<https://config.farfrom.world>

**Default config**
```yml
effects:
    - airhorn
    # - rickroll
blocked_channels:
    # - 1234
```
Clip types:
`{clip_types}`

Request clips using `ah!requestclip fart`
"""


class Config(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.command()
    async def config(self, ctx: commands.Context):
        if ctx.author.guild_permissions.administrator:
            try:
                await self.bot.config.grant_access(ctx.guild.id, ctx.author.id)
            except:
                pass
        else:
            try:
                await self.bot.config.revoke_access(ctx.guild.id, ctx.author.id)
            except:
                pass
        airhorn_cog = self.bot.get_cog("Airhorn")
        await ctx.send(config_response.format(clip_types=", ".join(airhorn_cog.valid_clips)))

    @commands.command()
    async def requestclip(self, ctx, *, request):
        await self.bot.logger.warn("Effect add request: " + request)
        await ctx.send("The request is on it's way!")


def setup(bot: Bot):
    bot.add_cog(Config(bot))
