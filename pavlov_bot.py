# Other useful libraries
from dotenv import load_dotenv
import os
import random
import csv

# Imports for Discord API
import discord
from discord.ext import commands

# Load .env file
load_dotenv()

# Access .env variable
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Set up the bot
intents = discord.Intents.default()
intents.message_content = True
intents.reactions = True
intents.messages = True
intents.guilds = True
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Event: Bot ready
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")

# Command to start an event
@bot.command()
async def start_event(ctx, channel: discord.TextChannel, role: discord.Role):
    """
    Announces an event and asks users to react to participate.

    Args:
        channel (discord.TextChannel): The channel where the event message will be sent.
        role (discord.Role): The role to mention in the event message.
    """
    event_message = await channel.send(f"{role.mention} React with ✅ to participate in the event!")
    await event_message.add_reaction("✅")

    bot.event_message_id = event_message.id

# Command to pick winners
@bot.command()
async def pick_winners(ctx, channel: discord.TextChannel):
    """
    Selects 8 random users who reacted to the event message to partcipate in the event.
    The non-winners are written to a CSV file locally.
    
    Args:
        channel (discord.TextChannel): The channel where the event message is located.
    """
    if not hasattr(bot, 'event_message_id'):
        await ctx.send("No event message found. Start an event with !start_event")
        return
    
    # Grabs list of users who reacted to the event message
    event_message = await channel.fetch_message(bot.event_message_id)
    reaction = discord.utils.get(event_message.reactions, emoji="✅")
    users = [user async for user in reaction.users() if not user.bot]
    
    if users:
        # Select 8 random winners and create a list of non-winners
        winners = random.sample(users, min(8, len(users)))
        non_winners = [user for user in users if user not in winners]

        # Announces the winners
        winner_mentions = ', '.join(user.mention for user in winners)
        await channel.send(f"🎉 The participants will be: {winner_mentions} 🎉")

        # Write non-winners to a CSV file
        file_path = "non_winners.csv"
        with open(file_path, mode='w', newline='') as file:
            csv_writer = csv.writer(file)
            csv_writer.writerow(["User ID", "Username"])
            for user in non_winners:
                csv_writer.writerow([user.id, user.name]) 
    else:
        await ctx.send("No reactions found on the event message.")


# Run the bot
bot.run(BOT_TOKEN)