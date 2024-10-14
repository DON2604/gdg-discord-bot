import discord

responses = []

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

def setup_modal(bot):
    @bot.slash_command()
    async def send_modal(ctx):
        await ctx.response.send_modal(MyModal(title="Testing Form"))
