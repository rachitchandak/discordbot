from discord.ext import commands
import discord

token = ""

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())
   
bot.load_extension('cogs.Commands')
bot.load_extension('cogs.Events')
bot.load_extension('cogs.ReactRoles')
bot.load_extension('cogs.TemporaryVoice')
bot.load_extension('cogs.Logging')
bot.load_extension('cogs.InviteTracker')

bot.run(token)
