import discord
from discord.ext import commands
from discord import app_commands

intents = discord.Intents.default()
intents.guilds = True
bot = commands.Bot(command_prefix="!", intents=intents)

class EmbedModal(discord.ui.Modal, title="Create Embed"):
    embed_title = discord.ui.TextInput(label="Title", required=True)
    embed_description = discord.ui.TextInput(label="Description", style=discord.TextStyle.paragraph, required=True)
    embed_color = discord.ui.TextInput(label="Hex Color (e.g. #00ff00)", default="#00ff00", required=False)

    async def on_submit(self, interaction: discord.Interaction):
        try:
            color = int(self.embed_color.value.strip("#"), 16)
        except:
            color = 0x00ff00
        embed = discord.Embed(title=self.embed_title.value, description=self.embed_description.value, color=color)
        embed.set_footer(text="Sent via UI Embed Bot")
        view = ChannelView(embed)
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

class ChannelDropdown(discord.ui.Select):
    def __init__(self, embed):
        self.embed = embed
        options = [
            discord.SelectOption(label=ch.name, value=str(ch.id))
            for ch in bot.get_all_channels()
            if isinstance(ch, discord.TextChannel)
        ][:25]
        super().__init__(placeholder="Choose a channel", options=options)

    async def callback(self, interaction: discord.Interaction):
        channel = bot.get_channel(int(self.values[0]))
        if channel:
            await channel.send(embed=self.embed)
            await interaction.response.send_message(f"✅ Embed sent to #{channel.name}", ephemeral=True)

class ChannelView(discord.ui.View):
    def __init__(self, embed):
        super().__init__()
        self.add_item(ChannelDropdown(embed))

@bot.tree.command(name="embedbuilder")
async def embedbuilder(interaction: discord.Interaction):
    btn = discord.ui.Button(label="➕ Create Embed", style=discord.ButtonStyle.primary)
    async def callback(interaction_btn):
        await interaction_btn.response.send_modal(EmbedModal())
    btn.callback = callback
    view = discord.ui.View()
    view.add_item(btn)
    await interaction.response.send_message("Click to build embed:", view=view, ephemeral=True)

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"Logged in as {bot.user}")

bot.run("YOUR_BOT_TOKEN")
