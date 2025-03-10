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
intents.voice_states = True
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

@bot.command()
async def join(ctx):
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        await channel.connect()
        await ctx.send(f"Joined {channel.name}!")
    else:
        await ctx.send("You must be in a voice channel for me to join!")

@bot.command()
async def leave(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send("Left the voice channel!")
    else:
        await ctx.send("I'm not in a voice channel.")

@bot.event
async def on_voice_state_update(member, before, after):
    guild_id = member.guild.id
    if guild_id in target_users and target_users[guild_id] == member.id:
        if after.channel and not before.channel:
            channel = after.channel
            if not member.guild.voice_client:
                await channel.connect()

        if member.voice and member.voice.self_stream:
            voice_client = member.guild.voice_client
            if voice_client:
                await member.guild.system_channel.send(f"{member.display_name} is speaking!")

# Run bot
bot.run(TOKEN)