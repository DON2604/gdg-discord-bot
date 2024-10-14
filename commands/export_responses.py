import discord
import pandas as pd
from discord import Interaction

responses = []  

ids = [825022764368265277, 723517069739425874] 

def setup_export_responses(bot):
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
