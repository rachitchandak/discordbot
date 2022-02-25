from os import stat
from discord.ext import commands 
import discord
import json
import asyncio

class TemporaryVoice(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def setup_voice(self, ctx):
        vc_id = ctx.author.voice.channel.id
        vc_cat_id = ctx.author.voice.channel.category.id
        temp_voice_key = "TemporaryVoiceDetails"
        temp_voice_data = {"ChannelId": vc_id, "CategoryId": vc_cat_id}

        try:
            with open('config.json') as file:
                data = json.load(file)
            data[temp_voice_key] = temp_voice_data

            with open('config.json', 'w') as file:
                json.dump(data, file, indent=1)
        except:
            data = {}
            data[temp_voice_key] = data[temp_voice_data]
            with open('config.json', 'w') as file:
                json.dump(data, file, indent=1)
    
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.member.bot:
            return
        channel = self.bot.get_channel(payload.channel_id)
        
        with open('config.json') as file:
            data = json.load(file)

        tmp_vc_cat = data['TemporaryVoiceDetails']['CategoryId']
        if tmp_vc_cat == channel.category.id:
                if payload.emoji.name == "🔒":
                    
                    channel = payload.member.voice.channel
                    if channel is None:
                        return
                    guild = self.bot.get_guild(payload.guild_id)
                    await channel.set_permissions(guild.default_role, connect=False)
                    channel = self.bot.get_channel(payload.channel_id)
                    
                    message = await channel.fetch_message(payload.message_id)
                    status = message.embeds[0].description.split('`')[-2].replace("Unlocked", "Locked")
                    lock_page = discord.Embed(title=f"{payload.member.display_name} Private Chat", description=f"Welcome {payload.member.display_name} to your private channel.\nIt will be deleted with the Voice Channel.\n\n**Currently:**\n`{status}`\n\n")
                    lock_page.add_field(name="🔒 Lock the channel", value="\u200b", inline=False)
                    lock_page.add_field(name="🔓 Unlock the channel", value="\u200b", inline=True)
                    lock_page.add_field(name="🔼 Increase bitrate", value="\u200b", inline=False)
                    lock_page.add_field(name="🔽 Decrease bitrate", value="\u200b", inline=True)

                    
                    await message.edit(embed=lock_page)

                    reaction = discord.utils.get(message.reactions, emoji=payload.emoji.name)
                    await reaction.remove(payload.member)

                elif payload.emoji.name == "🔓":
                    channel = payload.member.voice.channel
                    if channel is None:
                        return 
                    guild = self.bot.get_guild(payload.guild_id)
                    await channel.set_permissions(guild.default_role, connect=True)
                    channel = self.bot.get_channel(payload.channel_id)
                    
                    message = await channel.fetch_message(payload.message_id)
                    status = message.embeds[0].description.split('`')[-2].replace("Locked", "Unlocked")
                    lock_page = discord.Embed(title=f"{payload.member.display_name} Private Chat", description=f"Welcome {payload.member.display_name} to your private channel.\nIt will be deleted with the Voice Channel.\n\n**Currently:**\n`{status}`\n\n")
                    lock_page.add_field(name="🔒 Lock the channel", value="\u200b", inline=False)
                    lock_page.add_field(name="🔓 Unlock the channel", value="\u200b", inline=True)
                    lock_page.add_field(name="🔼 Increase bitrate", value="\u200b", inline=False)
                    lock_page.add_field(name="🔽 Decrease bitrate", value="\u200b", inline=True)

                    
                    await message.edit(embed=lock_page)

                    reaction = discord.utils.get(message.reactions, emoji=payload.emoji.name)
                    await reaction.remove(payload.member)


                elif payload.emoji.name == "🔼":
                    channel = payload.member.voice.channel
                    if channel is None:
                        return 
                    bitrate = channel.bitrate
                    if bitrate == 256000:
                        UI = discord.Embed(description="256kbps is the maximum bitrate.")
                        channel = self.bot.get_channel(payload.channel_id)
                        msg = await channel.send(embed=UI)
                        await asyncio.sleep(5)
                        await msg.delete()
                        
                    else:
                        bitrate = bitrate*2
                        await channel.edit(bitrate=bitrate)
                        channel = self.bot.get_channel(payload.channel_id)
                        bitrate = str(bitrate).rstrip('000') + 'kbps'
                        message = await channel.fetch_message(payload.message_id)
                        status = message.embeds[0].description.split('`')[-2].split('@')
                        status[1] = bitrate
                        status='@'.join(status)
                        lock_page = discord.Embed(title=f"{payload.member.display_name} Private Chat", description=f"Welcome {payload.member.display_name} to your private channel.\nIt will be deleted with the Voice Channel.\n\n**Currently:**\n`{status}`\n\n")
                        lock_page.add_field(name="🔒 Lock the channel", value="\u200b", inline=False)
                        lock_page.add_field(name="🔓 Unlock the channel", value="\u200b", inline=True)
                        lock_page.add_field(name="🔼 Increase bitrate", value="\u200b", inline=False)
                        lock_page.add_field(name="🔽 Decrease bitrate", value="\u200b", inline=True)
                        await message.edit(embed=lock_page)

                    message = await channel.fetch_message(payload.message_id)
                    reaction = discord.utils.get(message.reactions, emoji=payload.emoji.name)
                    await reaction.remove(payload.member)

                elif payload.emoji.name == "🔽":
                    channel = payload.member.voice.channel
                    if channel is None:
                        return 
                    bitrate = channel.bitrate
                    if bitrate == 32000:
                        UI = discord.Embed(description="32kbps is the minimum bitrate.")
                        channel = self.bot.get_channel(payload.channel_id)
                        msg = await channel.send(embed=UI)
                        await asyncio.sleep(5)
                        await msg.delete()
                        
                    else:
                        bitrate = bitrate//2
                        await channel.edit(bitrate=bitrate)
                        channel = self.bot.get_channel(payload.channel_id)
                        bitrate = str(bitrate).rstrip('000') + 'kbps'
                        message = await channel.fetch_message(payload.message_id)
                        status = message.embeds[0].description.split('`')[-2].split('@')
                        status[1] = bitrate
                        status='@'.join(status)
                        lock_page = discord.Embed(title=f"{payload.member.display_name} Private Chat", description=f"Welcome {payload.member.display_name} to your private channel.\nIt will be deleted with the Voice Channel.\n\n**Currently:**\n`{status}`\n\n")
                        lock_page.add_field(name="🔒 Lock the channel", value="\u200b", inline=False)
                        lock_page.add_field(name="🔓 Unlock the channel", value="\u200b", inline=True)
                        lock_page.add_field(name="🔼 Increase bitrate", value="\u200b", inline=False)
                        lock_page.add_field(name="🔽 Decrease bitrate", value="\u200b", inline=True)
                        await message.edit(embed=lock_page)
                        
                    message = await channel.fetch_message(payload.message_id)
                    reaction = discord.utils.get(message.reactions, emoji=payload.emoji.name)
                    await reaction.remove(payload.member)


    

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        try:
            with open("config.json", 'r') as file:
                data = json.load(file)
                channel_id = data["TemporaryVoiceDetails"]["ChannelId"]
                category_id = data["TemporaryVoiceDetails"]["CategoryId"]
            if after.channel != None and after.channel.id != None:
                if after.channel.id == channel_id:
                    for guild in self.bot.guilds:
                        category = discord.utils.get(guild.categories, id = category_id)
                        user_voice_channel = await guild.create_voice_channel(name=f"{member.display_name}\'s voice", category = category)
                        user_text_channel = await guild.create_text_channel(name=f"{member.display_name}\'s chat", category = category)
                        await user_text_channel.set_permissions(guild.default_role, connect=False, read_messages=False, send_messages=False)
                        await user_text_channel.set_permissions(member, connect=True, read_messages=True, send_messages=True)
                        await user_voice_channel.set_permissions(member, connect=True, mute_members=True, manage_channels=True)
                        await member.move_to(user_voice_channel)
                        lock_page = discord.Embed(title=f"{member.display_name} Private Chat", description=f"Welcome {member.display_name} to your private channel.\nIt will be deleted with the Voice Channel.\n\n**Currently:**\n`Unlocked@64kbps.`\n\n")
                        lock_page.add_field(name="🔒 Lock the channel", value="\u200b", inline=False)
                        lock_page.add_field(name="🔓 Unlock the channel", value="\u200b", inline=True)
                        lock_page.add_field(name="🔼 Increase bitrate", value="\u200b", inline=False)
                        lock_page.add_field(name="🔽 Decrease bitrate", value="\u200b", inline=True)

                        msg = await user_text_channel.send(embed=lock_page)

                        await msg.add_reaction("🔒")
                        await msg.add_reaction("🔓")
                        await msg.add_reaction("🔼")
                        await msg.add_reaction("🔽")

                        def check_channel(x, y, z):
                                return len(user_voice_channel.members) == 0

                        await self.bot.wait_for("voice_state_update", check=check_channel)
                        await user_voice_channel.delete()
                        await user_text_channel.delete()
        except:
            return 

def setup(bot):
    bot.add_cog(TemporaryVoice(bot))