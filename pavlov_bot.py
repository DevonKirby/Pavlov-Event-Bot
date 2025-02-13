# Other useful libraries
from dotenv import load_dotenv
import os

# Imports for Discord API
import discord
from discord.ext import commands

# Load .env file
load_dotenv()

# Access .env variables
BOT_TOKEN = os.getenv("BOT_TOKEN")
PUBLIC_KEY = os.getenv("PUBLIC_KEY")
APPLICATION_ID = os.getenv("APPLICATION_ID")

# Set up the bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Event: Bot ready
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")



# Run the bot
bot.run(BOT_TOKEN)