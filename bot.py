import discord
from dotenv import load_dotenv
import os
from commands.role_selection import setup_role_selection
from commands.welcome import setup_welcome
from commands.modal import setup_modal
from commands.export_responses import setup_export_responses
from commands.presence_logging import setup_presence_logging
from commands.export_presence import setup_export_presence

load_dotenv()

api_key = os.getenv("API_KEY")
intents = discord.Intents.default()
intents.members = True
intents.voice_states = True  

bot = discord.Bot(intents=intents)
@bot.event
async def on_ready():
    print(f'Bot is ready as {bot.user}')

setup_welcome(bot)
setup_modal(bot)
setup_export_responses(bot)
setup_presence_logging(bot)
setup_export_presence(bot)
setup_role_selection(bot)

bot.run(api_key)
