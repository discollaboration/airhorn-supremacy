from _asyncio import get_event_loop

from discord.ext import commands
from templatebot import Bot
from discord.ext.tasks import loop
from random import randint, choice
from discord import FFmpegPCMAudio, Guild
from asyncio import get_event_loop


class Airhorn(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
        self.loop = get_event_loop()
        self.valid_clips = ["airhorn", "rickroll"]
        self.playing_in = []
        self.scan.start()
        self.logger = self.bot.logger

    @loop(seconds=60)
    async def scan(self):
        for guild in self.bot.guilds:
            if randint(1, 15) != 4:
                continue
            self.loop.create_task(self.airboom(guild))

    async def airboom(self, guild: Guild):
        channel = await self.get_channel(guild)
        if channel is None:
            return
        clip_name = await self.get_clip(guild)
        if clip_name is None:
            return
        self.playing_in.append(guild.id)

        await self.bot.logger.info("Airbooming %s" % guild.name)

        audio = FFmpegPCMAudio("effects/%s.mp3" % clip_name)
        voice_state = await channel.connect()
        voice_state.play(audio, after=self._after_play(guild.id))

    async def after_play(self, guild_id):
        await self.bot.get_guild(guild_id).voice_client.disconnect(force=True)
        self.playing_in.remove(guild_id)

    def _after_play(self, guild_id):
        def inner(_):
            self.loop.create_task(self.after_play(guild_id))

        return inner

    async def get_clip(self, guild: Guild):
        config = await self.bot.config.get_config(guild.id)
        if not isinstance(config, dict):
            config = {}
        clips = config.get("effects", ["airhorn"])
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
            perms = channel.permissions_for(guild.me)
            if not (perms.connect and perms.view_channel and perms.speak):
                continue
            if len(channel.members) != 0 and channel.id not in blocked_channels:
                channels.append(channel)
        if len(channels) == 0:
            return None
        return choice(channels)


def setup(bot: Bot):
    bot.add_cog(Airhorn(bot))
