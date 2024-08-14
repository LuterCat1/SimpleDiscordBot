# Discord Moderation Bot

This is a simple Discord bot built using Python and the `discord.py` library. The bot provides several moderation commands and a message logging feature that can be toggled on and off by server administrators.

## Features

- **Message Logging**: The bot can create a private channel where all messages in the server are logged. This feature can be activated with the `!messagelog` command and deactivated with the `!stopmessagelog` command.
  
- **Moderation Commands**: The bot includes various moderation commands to manage server members and channels.

## Commands

### Message Logging
- `!messagelog`: Creates a private text channel called `message-log` and logs all server messages in that channel.
- `!stopmessagelog`: Stops logging messages and deletes the `message-log` channel.

### User Moderation
- `!ban <member> [reason]`: Bans the specified member from the server.
- `!kick <member> [reason]`: Kicks the specified member from the server.
- `!mute <member> [reason]`: Mutes the specified member by adding a "Muted" role that restricts speaking and sending messages.
- `!unmute <member>`: Unmutes the specified member.
- `!warn <member> [reason]`: Sends a warning to the specified member.
- `!nick <member> <nickname>`: Changes the nickname of the specified member.

### Message Management
- `!clear <amount>`: Deletes the specified number of messages from the current channel.
- `!slowmode <seconds>`: Sets a slowmode delay in the current channel.
- `!lock`: Locks the current channel, preventing non-admins from sending messages.
- `!unlock`: Unlocks the current channel, allowing everyone to send messages again.

### Role Management
- `!addrole <member> <role>`: Adds a specified role to a member.
- `!removerole <member> <role>`: Removes a specified role from a member.
- `!createrole <name>`: Creates a new role with the specified name.
- `!deleterole <role>`: Deletes the specified role.
- `!roleinfo <role>`: Provides information about the specified role.
- `!listroles`: Lists all roles in the server.

### Channel Management
- `!create_channel <channel_name>`: Creates a new text channel with the specified name.
- `!delete_channel <channel>`: Deletes the specified text channel.
- `!rename_channel <channel> <new_name>`: Renames the specified text channel to a new name.
- `!lockdown`: Locks all channels in the server.
- `!unlockdown`: Unlocks all channels in the server.

### Miscellaneous
- `!announce <message>`: Sends an announcement to the current channel mentioning everyone.
- `!say <message>`: The bot repeats the specified message.
- `!dm <member> <message>`: Sends a direct message to the specified member.
- `!nuke`: Clones the current channel and deletes the original, effectively clearing all messages in it.
- `!poll <question>`: Creates a poll with thumbs-up and thumbs-down reactions for voting.
- `!listmembers`: Lists all members in the server.

## Installation

1. Clone the repository or download the source code.
2. Install the required dependencies using pip:
   ```bash
   pip install discord.py
