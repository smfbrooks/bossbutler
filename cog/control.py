import logging

import discord
from discord.ext import commands


class Control(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.log = logging.getLogger('bossbutler.cog.control')

    @commands.command()
    @commands.guild_only()
    async def stop(self, ctx):
        """Stop playing the alarm and leave the voice channel"""
        self.log.debug(f'{ctx.author}:{ctx.command}:{ctx.message}')
        if ctx.voice_client:
            msg = f'Leaving {ctx.voice_client.channel}.'
            await ctx.send(msg)
            self.log.info(msg)
            await ctx.voice_client.disconnect()
        else:
            await ctx.send('I am not connected to any channels right now...')

    @commands.command()
    @commands.guild_only()
    async def play(self, ctx):
        """Immediately play the currently configured alarm"""
        self.log.debug(f'{ctx.author}:{ctx.command}:{ctx.message}')
        if not ctx.voice_client:
            await ctx.send(f'I am not even in a voice channel right now... You will have to send me somewhere first.')
            raise commands.CommandError('Cannot play when not in a channel.')

        msg = f'Playing the alarm now.'
        await ctx.send(msg)
        self.log.info(msg)
        ctx.voice_client.play(discord.FFmpegPCMAudio(self.bot.settings[ctx.guild.id].get('yt_file'), executable=self.bot.ffmpeg))

    @commands.command()
    @commands.guild_only()
    async def join(self, ctx, *channel: str):
        """Immediately join a voice channel, leaving any other"""
        ch_name = ' '.join(channel)
        self.log.debug(f'{ctx.author}:{ctx.command}:{ctx.message}')
        self.log.info(f'{ctx.message.author} asked me to move to {ch_name}.')
        await ctx.send(f'Joining {ch_name}.')
        if ctx.voice_client:
            self.log.warn(f'I am already connected to {ctx.voice_client.channel}, but I will move anyways.')
            await ctx.voice_client.disconnect()
        try:
            await discord.utils.get(ctx.guild.voice_channels, name=ch_name).connect()
        except Exception as e:
            self.log.exception(f'Cannot join {ch_name}: {e}')
            raise commands.CommandError(f'Unable to join {ch_name}.')
