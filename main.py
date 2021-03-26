from templatebot import Bot
from discord import Intents
from os import getenv
from botconfig.client import BotConfig

intents = Intents.none()
intents.voice_states = True
intents.messages = True
intents.guilds = True

bot = Bot(
    name="Airhorn Supremacy",
    command_prefix="ah!",
    intents=Intents.default(),
    logging_url=getenv("WEBHOOK"),
    help_command=None,
)
bot.config = BotConfig(getenv("BOT_ID"), getenv("CONFIG_TOKEN"))

bot.load_initial_cogs("cogs.airhorn", "cogs.config")

bot.run(getenv("TOKEN"))
