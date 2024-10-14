import discord
from discord import Interaction
from .presence_logging import presence_logs  

ids = [825022764368265277, 723517069739425874] 
def setup_export_presence(bot):
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
