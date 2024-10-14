import discord

# Define the role IDs and their corresponding emojis for selection
ROLE_IDS = {
    "📱 Android Dev": 1295094540687900785,
    "⚙️ CP": 1295094540675452967,
    "🌐 Web Dev": 1295094540675452965,
    "🛡️ Cyber Sec.": 1295094540675452964,
    "🎨 UI/UX": 1295094540675452963,
    "🌐 Web3": 1295094540675452962,
    "🤖 AI/ML": 1295094540675452961,
    "☁️ DevOps & Cloud": 1295094540675452960,
    "🛠️ Open Source": 1295344664798429315,
    "🔌 Hardware & IoT": 1295344768456327168,
}

class RoleButton(discord.ui.Button):
    def __init__(self, role_name):
        super().__init__(label=role_name, style=discord.ButtonStyle.primary)
        self.role_name = role_name

    async def callback(self, interaction: discord.Interaction):
        guild = interaction.guild
        role = discord.utils.get(guild.roles, id=ROLE_IDS[self.role_name])

        if role in interaction.user.roles:
            await interaction.user.remove_roles(role)
            await interaction.response.send_message(
                f"🚫 Removed **{role.name}** role.", ephemeral=True
            )
        else:
            await interaction.user.add_roles(role)
            await interaction.response.send_message(
                f"✅ Added **{role.name}** role.", ephemeral=True
            )

class RoleSelectView(discord.ui.View):
    def __init__(self):
        super().__init__()
        for role_name in ROLE_IDS.keys():
            self.add_item(RoleButton(role_name))

def create_help_embed() -> discord.Embed:
    """Creates an embed explaining how to use the role selection feature."""
    embed = discord.Embed(
        title="🧑‍💻 Role Selection Guide",
        description=(
            "Click the buttons below to add or remove roles.\n"
            "If you already have a role, clicking the button will remove it.\n"
            "Otherwise, clicking the button will add it to you.\n\n"
            "**Why Choose Roles?**\n"
            "Get notified about events, updates, and discussions related to specific topics!"
        ),
        color=discord.Color.blurple(),
    )
    embed.set_footer(text="Select or deselect roles freely!")
    return embed

async def role_selection(ctx: discord.Interaction):
    """Sends the role selection embed and view."""
    embed = create_help_embed()
    view = RoleSelectView()

    await ctx.response.send_message(
        embed=embed, view=view, ephemeral=True  
    )

def setup_role_selection(bot):
    """Register the role selection command."""
    @bot.slash_command(description="Role selection command")
    async def select_role(ctx: discord.Interaction):
        await role_selection(ctx)
