from discord.ext import commands
import discord

class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{self.bot.user} has logged on.')

    @commands.Cog.listener()
    async def on_error(self, event, *args, **kwargs):
      print('----------')
      print('An error occurred')
      print(args[0])
      print('----------')
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        UI = discord.Embed(description=error)
        await ctx.channel.send(embed=UI)
def setup(bot):
    bot.add_cog(Events(bot))