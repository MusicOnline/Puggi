import platform

import discord  # type: ignore
from discord.ext import commands  # type: ignore

import botto


class Meta(commands.Cog):
    """Meta commands related to the bot."""

    def __init__(self, bot: botto.Botto) -> None:
        self.bot: botto.Botto = bot

    def get_statistics_embed(self) -> discord.Embed:
        total_members: int = sum(1 for m in self.bot.get_all_members())
        total_users: int = self.bot.user_count
        total_online: int = len(
            {
                m
                for m in self.bot.get_all_members()
                if m.status is not discord.Status.offline
            }
        )

        text_channels: int = sum(
            1
            for channel in self.bot.get_all_channels()
            if isinstance(channel, discord.TextChannel)
        )
        voice_channels: int = sum(
            1
            for channel in self.bot.get_all_channels()
            if isinstance(channel, discord.VoiceChannel)
        )
        total_channels: int = text_channels + voice_channels

        total_guilds: int = self.bot.guild_count
        assert self.bot.ready_time is not None
        up_since: str = self.bot.ready_time.strftime("%d %b %y")
        ping: int = self.bot.ping
        with self.bot.process.oneshot():
            cpu_usage: float = self.bot.process.cpu_percent()
            ram_usage: float = self.bot.process.memory_full_info().uss / 2 ** 20

        embed: discord.Embed = discord.Embed(colour=botto.config.MAIN_COLOUR)
        embed.add_field(
            name="Member Stats",
            value=(
                f"{total_members} total members\n"
                f"{total_users} unqiue users\n"
                f"{total_online} users online"
            ),
        )
        embed.add_field(
            name="Channel Stats",
            value=(
                f"{total_channels} total\n"
                f"{text_channels} text channels\n"
                f"{voice_channels} voice channels"
            ),
        )
        embed.add_field(name="Other Stats", value=f"{total_guilds} guilds")
        embed.add_field(
            name="Uptime",
            value=(
                f"{self.bot.humanize_uptime(brief=True)}\n" f"(Since {up_since} UTC)"
            ),
        )
        embed.add_field(name="Connection", value=f"{ping} ms current")
        embed.add_field(name="Process", value=f"{cpu_usage}% CPU\n{ram_usage:.2f} MiB")

        embed.set_footer(
            text=(
                f"Made with discord.py {discord.__version__}, Python "
                f"{platform.python_version()} and love."
            )
        )

        return embed

    @botto.command()
    async def botstats(self, ctx: botto.Context) -> None:
        """Show general statistics of the bot."""
        embed: discord.Embed = self.get_statistics_embed()
        await ctx.send(embed=embed)

    @botto.command()
    async def ping(self, ctx: botto.Context) -> None:
        """Show connection statistics of the bot."""
        await ctx.send(f"ws pong: **{self.bot.ping} ms**")

    @botto.command()
    async def uptime(self, ctx: botto.Context) -> None:
        """Show uptime of the bot."""
        await ctx.send(f"Online since **{self.bot.humanize_uptime()}** ago.")

    @botto.command()
    async def invite(self, ctx: botto.Context) -> None:
        """Show invite link of the bot."""
        await ctx.send(f"<{discord.utils.oauth_url(ctx.me.id)}>")

    @botto.command()
    async def source(self, ctx: botto.Context) -> None:
        """Show GitHub link to source code."""
        await ctx.send("https://github.com/MusicOnline/Botto")

    @botto.command(aliases=["suggest", "feedback", "report", "contact"])
    async def support(self, ctx: botto.Context) -> None:
        """Show support server link."""
        await ctx.send("Contact Music#9755 here: https://discord.gg/wp7Wxzs")

    @botto.command(enabled=False)
    async def vote(self, ctx: botto.Context) -> None:
        """Support the bot by voting!"""
        pass


def setup(bot: botto.Botto) -> None:
    bot.add_cog(Meta(bot))
