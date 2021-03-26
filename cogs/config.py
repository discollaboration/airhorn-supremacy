from discord.ext import commands
from templatebot import Bot
from botconfig.client import BotConfig

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
"""


class Config(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.command()
    async def config(self, ctx: commands.Context):
        if ctx.author.guild_permissions.administrator:
            print("Granting access")
            await self.bot.config.grant_access(ctx.guild.id, ctx.author.id)
        else:
            print("Revoking access")
            await self.bot.config.revoke_access(ctx.guild.id, ctx.author.id)
        await ctx.send(config_response)


def setup(bot: Bot):
    bot.add_cog(Config(bot))
