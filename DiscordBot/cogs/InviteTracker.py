import discord
import DiscordUtils
from discord.ext import commands
import json


class Invites(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.tracker = DiscordUtils.InviteTracker(bot)

    @commands.Cog.listener()
    async def on_ready(self):
        await self.tracker.cache_invites()

    @commands.Cog.listener()
    async def on_invite_create(self, invite):
        await self.tracker.update_invite_cache(invite)

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        await self.tracker.update_guild_cache(guild)

    @commands.Cog.listener()
    async def on_invite_delete(self, invite):
        await self.tracker.remove_invite_cache(invite)

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        await self.tracker.remove_guild_cache(guild)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        inviter = await self.tracker.fetch_inviter(member)  
        with open('config.json') as file:
            data = json.load(file)
        channel_id = data['ModLoggingDetails']['ChannelId']
        channel = self.bot.get_channel(channel_id)
        embed = discord.Embed(
            title=f"{member.display_name} joined the server",
            description=f"Invited by: {inviter.mention}",
            timestamp=member.joined_at,
            color=0x00FF00
        )
        embed.set_thumbnail(url=member.avatar_url)
        embed.set_footer(text=member.guild.name, icon_url=member.guild.icon_url)
        await channel.send(embed=embed)


def setup(bot):
    bot.add_cog(Invites(bot))