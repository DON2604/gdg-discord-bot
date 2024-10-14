import discord
from PIL import Image, ImageSequence
import requests
from io import BytesIO
import os

async def send_welcome_message(member):
    channel = discord.utils.get(member.guild.text_channels, name='welcome')
    if channel:


        avatar_url = member.display_avatar.url
        response = requests.get(avatar_url)
        avatar = Image.open(BytesIO(response.content)).convert("RGBA")

        gif_path = 'background.gif'
        gif = Image.open(gif_path)

        frames = []
        avatar = avatar.resize((100, 100))


        for frame in ImageSequence.Iterator(gif):
            frame = frame.convert("RGBA")
            frame_copy = frame.copy()
            frame_copy.paste(avatar, (50, 50), avatar)
            frames.append(frame_copy)


        frames = [frames[-1]] + frames[:-1]


        output_path = f'output_{member.id}.gif'
        frames[0].save(
            output_path, save_all=True, append_images=frames[1:], 
            duration=gif.info['duration'], loop=0
        )


        await channel.send(f'Welcome to the server, {member.mention}!', file=discord.File(output_path))


        if os.path.exists(output_path):
            os.remove(output_path)

def setup_welcome(bot):
    @bot.event
    async def on_member_join(member):
        await send_welcome_message(member)
