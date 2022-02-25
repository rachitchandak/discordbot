from discord.ext import commands
import discord

class Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def callvote(self, ctx, mode, *args):
        if mode.lower() == 'yesno':
            emojis = ("👍", "👎")
            page = discord.Embed(description=' '.join(args))
            UI = await ctx.send(embed=page)

            for emoji in emojis:
                await UI.add_reaction(emoji)
        if mode.lower() == 'options':
            emoji_list = ['1️⃣','2️⃣','3️⃣','4️⃣','5️⃣','6️⃣','7️⃣','8️⃣','9️⃣']

            if len(args) > 9:
                await ctx.channel.send("More than 9 options are not allowed.")
                return

            vote = discord.Embed(title="Vote for your Favourite.", color=15105570)

            for num, stuff in enumerate(args):
                vote.add_field(name=stuff, value='`' + emoji_list[num]+ '`', inline=True)

            msg = await ctx.channel.send(embed=vote)

            for emoji in range(len(args)):
                await msg.add_reaction(emoji_list[emoji])
        await ctx.message.delete()

    @commands.command()
    async def server(self, ctx):
        server = ctx.message.guild
        online = 0
        for i in server.members:
            if str(i.status) == 'online' or str(i.status) == 'idle' or str(i.status) == 'dnd':
                    online += 1
           
        text_channels = 0
        voice_channels = 0

        for i in server.channels:
            if type(i) == discord.channel.TextChannel:
                text_channels += 1
            elif type(i) == discord.channel.VoiceChannel:
                voice_channels += 1
        

        info = discord.Embed()
        info.add_field(name=':crown: Owner', value=server.owner.mention)
        info.add_field(name=':id: ID', value=server.id)
        info.add_field(name=f':busts_in_silhouette: Members ({server.member_count})', value=str(online)+" online")
        info.add_field(name=f':speech_balloon: Channels ({str(text_channels + voice_channels)})', value=f'{text_channels} Text | {voice_channels} Voice')
        info.add_field(name=':calender: Created At', value=server.created_at.__format__('%A, %d. %B %Y'))
        info.set_thumbnail(url=server.icon_url)
        info.set_author(name=server.name, icon_url=server.icon_url)

        await ctx.channel.send(embed=info)
    
    @commands.command()
    async def afk(self, ctx):
        username = str(ctx.author.nick)
        if username.startswith("[AFK]"):
            username = username[6:]
            await ctx.message.author.edit(nick=username)
        else:
          if ctx.author.nick is not None:
            afkName = f"[AFK] {ctx.author.nick}"
          else:
            afkName = f"[AFK] {ctx.message.author.name}"
          await ctx.message.author.edit(nick=afkName)
          await ctx.message.delete()
    


        
    





def setup(bot):
    bot.add_cog(Commands(bot))
