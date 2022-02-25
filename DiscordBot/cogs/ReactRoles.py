import json
from discord.ext import commands
import discord

class ReactRoles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def add_role(self, ctx, emoji, role: discord.Role, *, message):
        UI = discord.Embed(description=role)
        page = await ctx.channel.send(embed=UI)
        await page.add_reaction(emoji)

        role_information = {
            'role_name':role.name,
            'role_id'  :role.id,
            'emoji'    :emoji,
            'msg_id'   :page.id
        }

        try:
            with open('roles.json') as file:
                data = json.load(file)
                data.append(role_information)
            with open('roles.json', 'w') as file:
                json.dump(data, file, indent=4)
        except:
            data = []
            data.append(role_information)
            with open('roles.json', 'w') as file:
                json.dump(data, file, indent=4)
        await ctx.message.delete()

    @commands.command()
    async def react_roles(self, ctx):
        try:
            UI = discord.Embed(title=f'Welcome to {self.bot.get_guild(ctx.guild.id)}', description='React to emojis to get corresponding roles:')
            with open('roles.json') as file:
                data = json.load(file)
            emojis = ()
            for role_info in data:
                name = role_info['role_name']
                emoji = role_info['emoji']
                emojis += emoji,
                UI.add_field(name=' ' + emoji + ' '+'    '+name, value='\u200b', inline=False)
            
            page = await ctx.channel.send(embed=UI)

            for emoji in emojis:
                await page.add_reaction(emoji)

            for role_info in data:
                role_info['msg_id'] = page.id
            
            with open('roles.json', 'w') as file:
                json.dump(data, file, indent=4)

            react_role_key = "ReactRolesDetails"
            react_role_data = {'ChannelId':ctx.channel.id, 'MessageId':page.id}
            try:
                with open('config.json') as file:
                    data = json.load(file)
                data[react_role_key] = react_role_data

                with open('config.json', 'w') as file:
                    json.dump(data, file, indent=1)
            except:
                data = {}
                data[react_role_key] = react_role_data

                with open('config.json', 'w') as file:
                    json.dump(data, file, indent=1)
        except:
            UI = discord.Embed(title='React roles not setup', description='setup roles by using `add_role` command.')
            await ctx.channel.send(embed=UI)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.member.bot:
            return
        
        with open('config.json') as file:
            data = json.load(file)

        react_role_channel = data['ReactRolesDetails']['ChannelId']
        if payload.channel_id == react_role_channel:
            with open('roles.json') as file:
                roles = json.load(file)
            for role in roles:
                emoji = ""
                if role['emoji'].count(':') >= 2:
                    emoji = role['emoji'].split(':')[1]
                else:
                    emoji = role['emoji']
                if emoji == payload.emoji.name and role['msg_id'] == payload.message_id:
                    role = discord.utils.get(self.bot.get_guild(payload.guild_id).roles, id=role['role_id'])
                    await payload.member.add_roles(role) 

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        try:
            with open('roles.json') as file:
                roles = json.load(file)
            
            for role in roles:
                emoji = ''
                if role['emoji'].count(':') >= 2:
                    emoji = role['emoji'].split(':')[1]
                else:
                    emoji = role['emoji']

                if emoji == payload.emoji.name and role['msg_id'] == payload.message_id:
                    role = discord.utils.get(self.bot.get_guild(payload.guild_id).roles, id = role['role_id'])
                    await self.bot.get_guild(payload.guild_id).get_member(payload.user_id).remove_roles(role)
        except:
            pass
    
def setup(bot):
    bot.add_cog(ReactRoles(bot))

