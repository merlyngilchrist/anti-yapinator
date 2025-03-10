import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import logging

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

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("bot.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

@bot.event
async def on_ready():
    logger.info(f"Logged in as {bot.user} (ID: {bot.user.id})")
    for guild in bot.guilds:
        logger.info(f"Connected to guild: {guild.name} (ID: {guild.id})")

@bot.command()
async def hello(ctx):
    await ctx.send(f"Hello, {ctx.author.mention}!")

@bot.command()
@commands.has_permissions(administrator=True)
async def target(ctx, member: discord.Member):
    target_users[ctx.guild.id] = member.id
    logger.info(f"Target set: {member.name} (ID: {member.id}) in guild {ctx.guild.name}")
    await ctx.send(f"Target set to {member.mention}!")

@target.error
async def target_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You don't have permission to set a target!")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please mention a user to set as the target. Example: '!target @username'")

@bot.command()
async def join(ctx):
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        try: 
            await channel.connect()
            logger.info(f"Bot joined voice channel: {channel.name} in {ctx.guild.name}")
        except discord.errors.ClientException:
            await ctx.send("I'm already in a voice channel!")
        except Exception as e:
            logger.error(f"Error joining voice channel: {e}")
            await ctx.send("Failed to join the voice channel.")
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

    if member == bot.user:
        if before.channel and not after.channel:
            logger.warning("Bot was disconnected from {before.channel.name}")
            try:
                await before.channel.connect()
                logger.info(f"Bot successfully reconnected to {before.channel.name}")
            except Exception as e:
                logger.error("Failed to reconnect: {e}")
        return
    
    if guild_id in target_users and target_users[guild_id] == member.id:
        if after.channel and not before.channel:
            channel = after.channel
            if not member.guild.voice_client:
                await channel.connect()

        if member.voice and member.voice.self_stream:
            voice_client = member.guild.voice_client
            if voice_client and not voice_client.is_playing():
                await member.guild.system_channel.send(f"{member.display_name} is speaking!")
                source = discord.FFmpegPCMAudio("alert.mp3") #changes when we get audio
                voice_client.play(source)
                logger.info(f"Played alert for {member.name} in {member.guild.name}")

@bot.command()
@commands.has_permissions(administrator=True)
async def removetarget(ctx):
    guild_id = ctx.guild.id

    if guild_id in target_users:
        removed_user_id = target_users.pop(guild_id)
        removed_user = ctx.guild.get_member(removed_user_id)
        logger.info(f"Removed target: {removed_user.name if removed_user else removed_user_id} in {ctx.guild.name}")
        
        if removed_user:
            await ctx.send(f"Target {removed_user.mention} has been removed.")
        else:
            await ctx.send(f"Target user (ID: {removed_user_id}) has been removed.")
    else:
        await ctx.send("No target is currently set for this server")

@removetarget.error
async def removetarget_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You don't have permission to remove a target!")
    else:
        logger.error(f"Error in removetarget command: {error}")

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Unknown command. Use '!help' to see available commands.")
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("You don't have permission to use this command.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Missing argument. Please provide all required details.")
    elif isinstance(error, commands.CommandInvokeError):
        await ctx.send("Something went wrong with the command. Please try again.")
        logger.error(f"Command error: {error}")
    else:
        await ctx.send("An unkown error occurred. Please try again.")
        logger.error(f"Unexpected error: {error}")

@bot.event
async def on_error(event, *args, **kwargs):
    logger.error(f"Discord API Error in {event}: {args} | {kwargs}")

# Run bot
bot.run(TOKEN)