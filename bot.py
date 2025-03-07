import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

# Load bot token from .env file
load_dotenv()
TOKEN = os.getenv("DISCORD_BOT_TOKEN")

if TOKEN is None:
    raise ValueError("DISCORD_BOT_TOKEN is missing from .env file!")

# Define bot with a command prefix
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Dictionary to store the target user per server
target_users = {}

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.command()
async def hello(ctx):
    await ctx.send(f"Hello, {ctx.author.mention}!")

@bot.command()
@commands.has_permissions(administrator=True)
async def target(ctx, member: discord.Member):
    """Set a target user for monitoring."""
    target_users[ctx.guild.id] = member.id
    await ctx.send(f"Target set to {member.mention}!")

@target.error
async def target_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You don't have permission to set a target!")
    elif isinstance(error, commands.MissingRequiredArgument):
        await cts.send("Please mention a user to set as the target. Example: '!target @username'")

# Run bot
bot.run(TOKEN)