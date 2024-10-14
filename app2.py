import discord
from discord.ext import commands
from discord import Interaction, ui
import pandas as pd
from dotenv import load_dotenv
import os
from datetime import datetime
from PIL import Image, ImageSequence
import requests
from io import BytesIO

load_dotenv()

api_key = os.getenv("API_KEY")

intents = discord.Intents.default()
intents.members = True  
intents.voice_states = True  

bot = commands.Bot(command_prefix='!', intents=intents)

responses = []
presence_logs = []
ids = [825022764368265277, 723517069739425874]  # Your Discord user IDs

@bot.event
async def on_ready():
    print(f'Bot is ready as {bot.user}')

class MyModal(discord.ui.Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        for i in range(3):
            self.add_item(discord.ui.InputText(label="Short Input"))
        self.add_item(discord.ui.InputText(label="Long Input", style=discord.InputTextStyle.long))

    async def callback(self, interaction: discord.Interaction):
        responses.append({"Name": self.children[0].value, "Feedback": self.children[1].value})
        print(responses)
        await interaction.response.send_message("Thanks for submitting", ephemeral=True)

@bot.slash_command()
async def send_modal(ctx):
    await ctx.response.send_modal(MyModal(title="Testing Form"))

@bot.slash_command(description="Export form responses as CSV (Admin only)")
async def export_responses(ctx: Interaction):
    if ctx.user.id not in ids:  
        await ctx.response.send_message("You are not authorized to use this command.", ephemeral=True)
        return

    if not responses:
        await ctx.response.send_message("No responses available to export.", ephemeral=True)
        return

    df = pd.DataFrame(responses)
    df.to_csv("responses.csv", index=False)

    await ctx.response.send_message(
        "Here is the CSV with all responses:",
        file=discord.File("responses.csv")
    )

@bot.event
async def on_voice_state_update(member, before, after):
    """Logs when members join, leave, or switch voice channels."""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    if before.channel is None and after.channel is not None:
        log = {
            "Member": str(member), 
            "Action": "Joined", 
            "Channel": after.channel.name, 
            "Time": timestamp
        }
        print(log)
        presence_logs.append(log)

    elif before.channel is not None and after.channel is None:
        log = {
            "Member": str(member), 
            "Action": "Left", 
            "Channel": before.channel.name, 
            "Time": timestamp
        }
        print(log)
        presence_logs.append(log)

    elif before.channel is not None and after.channel is not None and before.channel != after.channel:
        left_log = {
            "Member": str(member), 
            "Action": "Left", 
            "Channel": before.channel.name, 
            "Time": timestamp
        }
        joined_log = {
            "Member": str(member), 
            "Action": "Joined", 
            "Channel": after.channel.name, 
            "Time": timestamp
        }
        print(left_log)
        print(joined_log)
        presence_logs.extend([left_log, joined_log])

    if presence_logs:
        df = pd.DataFrame(presence_logs)
        df.to_csv("presence.csv", index=False)

@bot.slash_command(description="Export presence logs as CSV (Admin only)")
async def export_presence(ctx: Interaction):
    if ctx.user.id not in ids:  
        await ctx.response.send_message("You are not authorized to use this command.", ephemeral=True)
        return

    if not presence_logs:
        await ctx.response.send_message("No presence logs available to export.", ephemeral=True)
        return

    await ctx.response.send_message(
        "Here is the CSV with all presence logs:",
        file=discord.File("presence.csv")
    )

@bot.event
async def on_member_join(member):
    channel = discord.utils.get(member.guild.text_channels, name='welcome') 
    if channel:
        # Load the user's avatar
        avatar_url = member.display_avatar.url
        response = requests.get(avatar_url)
        avatar = Image.open(BytesIO(response.content)).convert("RGBA")

        # Load the GIF
        gif_path = 'background.gif' 
        gif = Image.open(gif_path)

        frames = []  
        avatar = avatar.resize((100, 100))

        for frame in ImageSequence.Iterator(gif):
            frame = frame.convert("RGBA")  
            frame_copy = frame.copy() 
            frame_copy.paste(avatar, (50, 50), avatar)  
            frames.append(frame_copy)

        output_path = f'output_{member.id}.gif'
        frames[0].save(output_path, save_all=True, append_images=frames[1:], duration=gif.info['duration'], loop=0)

        await channel.send(f'Welcome to the server, {member.mention}!', file=discord.File(output_path))

        if os.path.exists(output_path):
            os.remove(output_path)

bot.run(api_key)
