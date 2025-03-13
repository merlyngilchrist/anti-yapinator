import discord
from discord.ext import commands
from discord import app_commands
import os
from dotenv import load_dotenv
import logging
import asyncio

# Load bot token from .env file
load_dotenv()
TOKEN = os.getenv("DISCORD_BOT_TOKEN")

if TOKEN is None:
    raise ValueError("DISCORD_BOT_TOKEN is missing from .env file!")

# Define bot with a command prefix
intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Dictionary to store the target user per server
target_users = {}
allowed_roles = {}

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("bot.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

async def play_alert(guild):
    voice_client = guild.voice_client
    if not voice_client or not voice_client.is_connected():
        logger.error(f"Bot is not connected to a voice channel in {guild.name}.")
        return
    
    if not voice_client.is_playing():
        audio_path = "aaauuuggghhh.ogg"
        if os.path.exists(audio_path):
            source = discord.FFmpegPCMAudio(audio_path, executable="C:\\ffmpeg\\ffmpeg.exe")
            voice_client.play(source, after=lambda e: logger.info(f"Finished playing alert in {guild.name}"))
            logger.info(f"Played alert in {guild.name}")
        else:
            logger.error(f"Audio file '{audio_path}' not found.")

async def monitor_voice_activity(guild):
    while guild.voice_client and guild.voice_client.is_connected():
        target_id = target_users.get(guild.id)
        if not target_id:
            await asyncio.sleep(2)
            continue

        channel = guild.voice_client.channel
        members = channel.members
        
        if len(members) == 1:  # Only bot in the channel
            logger.info(f"Leaving {channel.name} as it's empty.")
            await guild.voice_client.disconnect()
            return
        
        for member in members:
            if member.id == target_id and member.voice and not member.voice.self_mute:
                logger.info(f"{member.name} is speaking in {channel.name}")
                await play_alert(guild)
                
        await asyncio.sleep(1)

@bot.event
async def on_ready():
    logger.info(f"Logged in as {bot.user} (ID: {bot.user.id})")

    try:
        synced = await bot.tree.sync()
        logger.info(f"Synced {len(synced)} command(s)")
    except Exception as e:
        logger.error(f"Failed to sync commands: {e}")

@bot.tree.command(name="ping", description="Replies with Pong!")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message("Pong!")

@bot.event
async def on_voice_state_update(member, before, after):
    guild = member.guild
    if member == bot.user:
        return

    if guild.id in target_users and target_users[guild.id] == member.id:
        if after.channel and (not before.channel or before.channel != after.channel):
            channel = after.channel
            if not guild.voice_client or not guild.voice_client.is_connected():
                voice_client = await channel.connect()
                logger.info(f"Bot joined {channel.name}.")
                await asyncio.sleep(1)
                asyncio.create_task(monitor_voice_activity(guild))

@bot.command()
async def set_allowed_role(ctx, role: discord.Role):
    if ctx.author == ctx.guild.owner:
        if ctx.guild.id not in allowed_roles:
            allowed_roles[ctx.guild.id] = []
        allowed_roles[ctx.guild.id].append(role.id)
        await ctx.send(f"Role {role.name} is now allowed to use bot commands.")
    else:
        await ctx.send("Only the server owner can set allowed roles.")

@bot.command()
async def show_allowed_roles(ctx):
    roles = allowed_roles.get(ctx.guild.id, [])
    if roles:
        role_names = [ctx.guild.get_role(role_id).mention for role_id in roles if ctx.guild.get_role(role_id)]
        await ctx.send("Allowed roles: " + ", ".join(role_names))
    else:
        await ctx.send("No roles have been set as allowed.")

@bot.command()
async def target(ctx, member: discord.Member):
    if member == bot.user:
        await ctx.send("I can't target myself!")
        return
    if ctx.author.guild_permissions.administrator or any(role.id in allowed_roles.get(ctx.guild.id, []) for role in ctx.author.roles):
        target_users[ctx.guild.id] = member.id
        logger.info(f"Target set: {member.name} (ID: {member.id}) in guild {ctx.guild.name}")
        await ctx.send(f"Target set to {member.mention}!")
    else:
        await ctx.send("You don't have permission to use this command.")

@bot.command()
async def remove_target(ctx):
    if ctx.author.guild_permissions.administrator or any(role.id in allowed_roles.get(ctx.guild.id, []) for role in ctx.author.roles):
        target_users.pop(ctx.guild.id, None)
        await ctx.send("Target has been removed.")
    else:
        await ctx.send("You don't have permission to use this command.")

@bot.command()
async def help_commands(ctx):
    help_text = """
    **Bot Commands:**
    `!set_allowed_role @role` - Allow a role to manage the bot
    `!show_allowed_roles` - Show all allowed roles
    `!target @user` - Set a user as the target
    `!remove_target` - Remove the current target
    `!join` - Bot joins your voice channel
    `!leave` - Bot leaves the current voice channel
    `!help_commands` - Show this help message
    """
    await ctx.send(help_text)

bot.run(TOKEN)
