import discord
from discord.ext import commands
import os  

# Discord bot setup
intents = discord.Intents.all()
intents.messages = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)


@bot.event
async def on_ready():
    # Set the custom status when the bot is ready
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="new names 👑 | broke"))
    print(f'Logged in as {bot.user.name}')


@bot.event
async def on_guild_join(guild: discord.Guild):
    # Try to find a text channel with permissions to send messages
    for channel in guild.text_channels:
        if channel.permissions_for(guild.me).send_messages:
            try:
                welcome_message = (
                    "```\n"
                    
                    "For details on how to use me, type `!help-editbot`.\n"
                    "```\n"
                )
                await channel.send(welcome_message)
                break  # Exit the loop after successfully sending the message
            except discord.Forbidden:
                # Continue to next channel if permission is denied
                continue
            except Exception as e:
                # Handle any other exceptions
                continue
    else:
        # Handle case where no suitable channel was found
        pass



@bot.tree.command(name='editch', description='Edit the name of the current channel with an emoji and new name')
@discord.app_commands.describe(emoji='Emoji to add to the channel name', new_name='New name for the channel')
async def editch(interaction: discord.Interaction, emoji: str, new_name: str):
    try:
        # Get the current channel
        channel = interaction.channel

        # Edit the channel's name
        old_name = channel.name
        new_channel_name = f"{emoji}│{new_name}"
        await channel.edit(name=new_channel_name)

        # Send result to the channel
        await interaction.response.send_message(f'Channel {old_name} renamed to {new_channel_name}.')

    except Exception as e:
        # Send error message to the channel
        await interaction.response.send_message(f"An error occurred: {str(e)}")

@bot.tree.command(name='editch_id', description='Edit the name of a specified channel with an emoji and new name')
@discord.app_commands.describe(channel_id='ID of the channel to rename', emoji='Emoji to add to the channel name', new_name='New name for the channel')
async def editch_id(interaction: discord.Interaction, channel_id: str, emoji: str, new_name: str):
    try:
        # Fetch the channel by its ID
        channel = bot.get_channel(int(channel_id))
        if channel is None:
            await interaction.response.send_message(f"Channel with ID {channel_id} not found.")
            return

        # Edit the channel's name
        old_name = channel.name
        new_channel_name = f"{emoji}│{new_name}"
        await channel.edit(name=new_channel_name)

        # Send result to the channel
        await interaction.response.send_message(f'Channel {old_name} renamed to {new_channel_name}.')

    except Exception as e:
        # Send error message to the channel
        await interaction.response.send_message(f"An error occurred: {str(e)}")

@bot.command(name='help-editbot')
async def help_editbot(ctx):
    help_message = (
        "```\n"
        "Commands for Editing Channels:\n\n"
        "`/editch` - Edit the name of the current channel.\n"
        "  Usage:\n"
        "    - Type `/editch` followed by the emoji and the new channel name.\n"
        "    - Example: `/editch 📌│New Name`\n"
        "    - This will change the name of the channel where the command was issued.\n\n"
        "`/editch_id` - Edit the name of a specified channel by its ID.\n"
        "  Usage:\n"
        "    - Type `/editch_id` followed by the channel ID, emoji, and the new channel name.\n"
        "    - Example: `/editch_id 123456789012345678 📌│New Name`\n"
        "    - This will change the name of the channel with the specified ID.\n\n"
        "Note:\n"
        "  - You can only edit a channel's name up to 2 times within a 6-10 minute period.\n"
        "```\n"
    )
    await ctx.send(help_message)



bot.run(os.getenv('DISCORD_TOKEN'))
