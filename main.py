import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)
message_log_channel = None  # Global variable to store the log channel

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.event
async def on_message(message):
    global message_log_channel
    if not message.author.bot and message_log_channel:  # Ignore bot messages
        log_message = f"User {message.author}: {message.content}"
        await message_log_channel.send(log_message)
    await bot.process_commands(message)

# Command to start logging messages
@bot.command()
@commands.has_permissions(administrator=True)
async def messagelog(ctx):
    global message_log_channel
    if message_log_channel is None:
        guild = ctx.guild
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            guild.me: discord.PermissionOverwrite(read_messages=True)
        }
        message_log_channel = await guild.create_text_channel('message-log', overwrites=overwrites)
        await ctx.send(f'Message logging started in {message_log_channel.mention}.')
    else:
        await ctx.send('Message logging is already active.')

# Command to stop logging messages
@bot.command()
@commands.has_permissions(administrator=True)
async def stopmessagelog(ctx):
    global message_log_channel
    if message_log_channel is not None:
        await message_log_channel.delete()
        message_log_channel = None
        await ctx.send('Message logging stopped.')
    else:
        await ctx.send('Message logging is not active.')

# Moderation commands

@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f'Banned {member.mention} for {reason}')

@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f'Kicked {member.mention} for {reason}')

@bot.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount: int):
    await ctx.channel.purge(limit=amount)
    await ctx.send(f'Cleared {amount} messages', delete_after=5)

@bot.command()
@commands.has_permissions(manage_channels=True)
async def lock(ctx):
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)
    await ctx.send('Channel locked.')

@bot.command()
@commands.has_permissions(manage_channels=True)
async def unlock(ctx):
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)
    await ctx.send('Channel unlocked.')

@bot.command()
@commands.has_permissions(mute_members=True)
async def mute(ctx, member: discord.Member, *, reason=None):
    muted_role = discord.utils.get(ctx.guild.roles, name="Muted")
    if not muted_role:
        muted_role = await ctx.guild.create_role(name="Muted")

        for channel in ctx.guild.channels:
            await channel.set_permissions(muted_role, speak=False, send_messages=False)

    await member.add_roles(muted_role, reason=reason)
    await ctx.send(f'Muted {member.mention} for {reason}')

@bot.command()
@commands.has_permissions(mute_members=True)
async def unmute(ctx, member: discord.Member):
    muted_role = discord.utils.get(ctx.guild.roles, name="Muted")
    await member.remove_roles(muted_role)
    await ctx.send(f'Unmuted {member.mention}')

@bot.command()
@commands.has_permissions(administrator=True)
async def warn(ctx, member: discord.Member, *, reason=None):
    await ctx.send(f'{member.mention} has been warned for: {reason}')

@bot.command()
@commands.has_permissions(administrator=True)
async def slowmode(ctx, seconds: int):
    await ctx.channel.edit(slowmode_delay=seconds)
    await ctx.send(f'Slowmode set to {seconds} seconds.')



@bot.command()
@commands.has_permissions(manage_roles=True)
async def addrole(ctx, member: discord.Member, role: discord.Role):
    await member.add_roles(role)
    await ctx.send(f'Added role {role.mention} to {member.mention}')

@bot.command()
@commands.has_permissions(manage_roles=True)
async def removerole(ctx, member: discord.Member, role: discord.Role):
    await member.remove_roles(role)
    await ctx.send(f'Removed role {role.mention} from {member.mention}')

@bot.command()
@commands.has_permissions(administrator=True)
async def announce(ctx, *, message):
    await ctx.send(f'@everyone {message}')

@bot.command()
@commands.has_permissions(administrator=True)
async def lockdown(ctx):
    for channel in ctx.guild.channels:
        await channel.set_permissions(ctx.guild.default_role, send_messages=False)
    await ctx.send('Server is in lockdown.')

@bot.command()
@commands.has_permissions(administrator=True)
async def unlockdown(ctx):
    for channel in ctx.guild.channels:
        await channel.set_permissions(ctx.guild.default_role, send_messages=True)
    await ctx.send('Server lockdown lifted.')



@bot.command()
@commands.has_permissions(administrator=True)
async def say(ctx, *, message):
    await ctx.message.delete()
    await ctx.send(message)

@bot.command()
@commands.has_permissions(administrator=True)
async def dm(ctx, member: discord.Member, *, message):
    await member.send(message)
    await ctx.send(f'Sent a DM to {member.mention}')

@bot.command()
@commands.has_permissions(administrator=True)
async def nuke(ctx):
    new_channel = await ctx.channel.clone()
    await ctx.channel.delete()
    await new_channel.send('This channel has been nuked.')

@bot.command()
@commands.has_permissions(administrator=True)
async def create_channel(ctx, channel_name):
    guild = ctx.guild
    await guild.create_text_channel(name=channel_name)
    await ctx.send(f'Created channel {channel_name}')

@bot.command()
@commands.has_permissions(administrator=True)
async def delete_channel(ctx, channel: discord.TextChannel):
    await channel.delete()
    await ctx.send(f'Deleted channel {channel.name}')

@bot.command()
@commands.has_permissions(manage_nicknames=True)
async def nick(ctx, member: discord.Member, *, nickname):
    await member.edit(nick=nickname)
    await ctx.send(f'Changed nickname for {member.mention} to {nickname}')



@bot.command()
@commands.has_permissions(administrator=True)
async def poll(ctx, *, question):
    message = await ctx.send(f'**POLL:** {question}')
    await message.add_reaction('👍')
    await message.add_reaction('👎')

@bot.command()
@commands.has_permissions(administrator=True)
async def roleinfo(ctx, *, role: discord.Role):
    await ctx.send(f'Role {role.name} has ID {role.id} and is assigned to {len(role.members)} members.')

@bot.command()
@commands.has_permissions(administrator=True)
async def listroles(ctx):
    roles = ctx.guild.roles
    roles_list = "\n".join([role.name for role in roles])
    await ctx.send(f"Roles in this server:\n ` {roles_list} ` ")

@bot.command()
@commands.has_permissions(administrator=True)
async def listmembers(ctx):
    members = ctx.guild.members
    members_list = "\n".join([member.name for member in members])
    await ctx.send(f"Members in this server:\n ` {members_list} `")

@bot.command()
@commands.has_permissions(manage_roles=True)
async def createrole(ctx, *, name):
    await ctx.guild.create_role(name=name)
    await ctx.send(f'Created role {name}')

@bot.command()
@commands.has_permissions(administrator=True)
async def deleterole(ctx, *, role: discord.Role):
    await role.delete()
    await ctx.send(f'Deleted role {role.name}')

@bot.command()
@commands.has_permissions(manage_channels=True)
async def rename_channel(ctx, channel: discord.TextChannel, new_name: str):
    await channel.edit(name=new_name)
    await ctx.send(f'Channel renamed to {new_name}')


bot.run('YOUR TOKEN!')




