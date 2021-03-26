from _asyncio import get_event_loop

from discord.ext import commands
from templatebot import Bot
from discord.ext.tasks import loop
from random import randint, choice
from discord import FFmpegPCMAudio, Guild
from asyncio import get_event_loop
from io import BytesIO


class Airhorn(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
        self.loop = get_event_loop()
        self.valid_clips = ["airhorn", "rickroll"]
        self.playing_in = []
        self.scan.start()

    @loop(seconds=10)
    async def scan(self):
        await self.bot.logger.info("Playing voice clips")
        for guild in self.bot.guilds:
            if randint(1, 5) != 4 and False:
                continue
            self.loop.create_task(self.airboom(guild))

    async def airboom(self, guild: Guild):
        channel = await self.get_channel(guild)
        if channel is None:
            await self.bot.logger.info("No channel")
            return
        clip_name = await self.get_clip(guild)
        if clip_name is None:
            await self.bot.logger.info("No clips")
            return
        self.playing_in.append(guild.id)

        await self.bot.logger.info("Playing effect")
        audio = FFmpegPCMAudio("effects/%s.mp3" % clip_name)
        voice_state = await channel.connect()
        await self.bot.logger.info("Connected to VC")
        voice_state.play(audio, after=self._after_play(guild.id))

    async def after_play(self, guild_id):
        await self.bot.get_guild(guild_id).voice_client.disconnect(force=True)
        self.playing_in.remove(guild_id)

    def _after_play(self, guild_id):
        def inner(err):
            self.after_play(guild_id)

        return inner

    async def get_clip(self, guild: Guild):
        config = await self.bot.config.get_config(guild.id)
        if not isinstance(config, dict):
            config = {}
        clips = config.get("effects", ["rickroll"])
        if not isinstance(clips, list):
            return None
        new_clips = []
        for clip in clips:
            if clip in self.valid_clips:
                new_clips.append(clip)

        if len(new_clips) == 0:
            return None
        return choice(new_clips)

    async def get_channel(self, guild: Guild):
        config = await self.bot.config.get_config(guild.id)
        if not isinstance(config, dict):
            config = {}
        blocked_channels = config.get("blocked_channels", [])
        if not isinstance(blocked_channels, list):
            return None
        if guild.id in self.playing_in:
            return None

        channels = []
        for channel in guild.voice_channels:
            if len(channel.members) != 1 and channel.id not in blocked_channels:
                channels.append(channel)
        if len(channels) == 0:
            return None
        return choice(channels)


def setup(bot: Bot):
    bot.add_cog(Airhorn(bot))
