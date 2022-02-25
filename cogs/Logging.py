from datetime import datetime
from discord.ext import commands
import discord
from pytz import timezone
import json


class Logging(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @commands.command()
    async def setup_mod_logs(self, ctx):
        try:
            with open('config.json') as file:
                data = json.load(file)
            data['ModLoggingDetails'] = {'ChannelId':ctx.channel.id, 'CategoryId': ctx.channel.category.id}

            with open('config.json', 'w') as file:
                json.dump(data, file, indent=1)

        except:
            data = {}
            data['ModLoggingDetails'] = {'ChannelId':ctx.channel.id, 'CategoryId': ctx.channel.category.id}
            with open('config.json', 'w') as file:
                json.dump(data, file, indent=1)

    @commands.command()
    async def setup_message_logs(self, ctx):
        try:
            with open('config.json') as file:
                data = json.load(file)
            data['MessageLoggingDetails'] = {'ChannelId':ctx.channel.id, 'CategoryId': ctx.channel.category.id}

            with open('config.json', 'w') as file:
                json.dump(data, file, indent=1)

        except:
            data = {}
            data['MessageLoggingDetails'] = {'ChannelId':ctx.channel.id, 'CategoryId': ctx.channel.category.id}
            with open('config.json', 'w') as file:
                json.dump(data, file, indent=1)

    @commands.command()
    async def setup_voice_logs(self, ctx):
        try:
            with open('config.json') as file:
                data = json.load(file)
            data['VoiceLoggingDetails'] = {'ChannelId':ctx.channel.id, 'CategoryId': ctx.channel.category.id}

            with open('config.json', 'w') as file:
                json.dump(data, file, indent=1)

        except:
            data = {}
            data['VoiceLoggingDetails'] = {'ChannelId':ctx.channel.id, 'CategoryId': ctx.channel.category.id}
            with open('config.json', 'w') as file:
                json.dump(data, file)

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.author.bot:
            return
        with open('config.json') as file:
            data = json.load(file)
        channel_id = data['MessageLoggingDetails']['ChannelId']
        IST = timezone('Asia/Kolkata')
        time = str(datetime.now(IST).time()).split('.')[0]
        channel = self.bot.get_channel(channel_id)
        UI = discord.Embed(description=f'{message.content}', color=0xFF0000)
        await channel.send(f'`{time}` ❌ {message.author}\'s message deleted from {message.channel.mention}', embed=UI)
    
    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if before.author.bot or before.content == after.content:
            return
        try:
            with open('config.json') as file:
                data = json.load(file)
            channel_id = data['MessageLoggingDetails']['ChannelId']
            IST = timezone('Asia/Kolkata')
            time = str(datetime.now(IST).time()).split('.')[0]
            channel = self.bot.get_channel(channel_id)
            UI = discord.Embed(color=0xFFD100)
            UI.add_field(name='Before: ', value=f'{before.content}', inline=False)
            UI.add_field(name='After: ', value=f'{after.content}', inline=False)
            await channel.send(f'`{time}` ⚠️ {before.author}\'s edited a message in {before.channel.mention}', embed=UI)
        except:
            pass

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        with open('config.json') as file:
            data = json.load(file)
        channel_id = data['VoiceLoggingDetails']['ChannelId']
        channel = self.bot.get_channel(channel_id)
        IST = timezone('Asia/Kolkata')
        if before.channel == None:
            page = discord.Embed(title=f"{member} joined {after.channel.name} at `{str(datetime.now(IST).time()).split('.')[0]}`", color=0x00FF00)
            await channel.send(embed=page)
        elif after.channel == None:
            page = discord.Embed(title=f"{member} left {before.channel.name} at `{str(datetime.now(IST).time()).split('.')[0]}`", color=0xFF0000)
            await channel.send(embed=page)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        IST = timezone('Asia/Kolkata')
        with open('config.json') as file:
            data = json.load(file)
        channel_id = data['ModLoggingDetails']['ChannelId']
        channel = self.bot.get_channel(channel_id)
        UI = discord.Embed(
            title=f'{member.display_name} left the server',
            timestamp=datetime.now(IST),
            color=0xFF0000
        )
        
        UI.set_footer(text=member.guild.name, icon_url=member.guild.icon_url)
        await channel.send(embed=UI)
        
        

def setup(bot):
    bot.add_cog(Logging(bot))

