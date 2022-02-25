# DiscordBot

## _All things one can ask for from a discord bot_

## Features

- Exclusive cool commands like !afk, !server and !callvote
- Can log everything. Joining and leaving voice channels, deleting or editing messages.
- Easiest bot to setup React Roles for your server.
- Create personal voice channels on joining, deleting when there are no members on the voice channel


## Commands 


- !afk - adds afk tag to yourself while you are away, use !afk again to remove the tag
- !callvote - Calls a vote. Has 2 modes, yesno and options. 
    ```
    !callvote yesno <Vote Content>
    !callvote options <Options Seperated by Spaces>
    ```
- !server - Display Server Information 
- !add_role - Add React Role for a paticular role.
    ```
    !add_role <emoji> <mention role> <role name>
    ```
- !react_roles - Start React Roles in the channel where !react_roles was executed.
- !setup_voice - Join the VoiceChannel that you want to be Personal Channel and run the command 
- !setup_message_logs - Run in the TextChannel you wanna get message logs (Edits and Deletes)
- !setup_mod_logs - Run in the TextChannel you wanna get member joining and leaving.
- !setup_voice_logs - Run in the TextChannel you wanna VoiceChannels logs in.

## Installation

Download the Zip File or Clone the Repository and install Requirements

```sh
git clone https://github.com/rachitchandak/discordbot
cd discordbot
pip3 install -r requirements.txt 
```



Get yourself an Application Token, Open `main.py` file and add your token in the variable named TOKEN. Upload these files on a server and run the main file.

After you get the text `bot logged on`, invite the bot to your server. On devoloper portal, Copy the Bot ID. Go to `https://discord.com/api/oauth2/authorize?client_id=123456789012345678&permissions=8&scope=bot%20applications.commands
` and make sure you replace the client_id in the link with your Bot ID.

Select the server and you should be good to go.

## Caution

you will have to setup the bot before you start using it
if setup is incomplete, the terminal may show errors. Use `!add_role` and `!react_role` and `!setup_voice` to complete setup.

If you don't wanna setup everything, go to `main.py` and remove the bot.load_extensions() for the Cogs you don't want.

Make sure PRESENCE INTENT and SERVER MEMBERS INTENT is ticked on on the discord developer portal.
