import discord
from discord.ext import commands, tasks
import os
import asyncio
import subprocess
from dotenv import load_dotenv
from PIL import ImageGrab
import io

# Load environment variables
load_dotenv()

# Bot setup
intents = discord.Intents.default()
# Enable message content intent for commands (requires privileged intent)
# If you don't enable this in Discord Developer Portal, comment out the next line
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Configuration from environment variables
SCREENSHOT_PATH = os.getenv('SCREENSHOT_PATH', 'shared_folder\\screenshot.png')
CHANNEL_NAME = os.getenv('CHANNEL_NAME', 'battle-nations')
CHECK_INTERVAL = int(os.getenv('CHECK_INTERVAL', '10'))  # seconds
PYTHON_PATH = os.getenv('PYTHON_PATH', '.venv\\Scripts\\python.exe')
SCRIPT_NAME = os.getenv('SCRIPT_NAME', 'autobn.py')

# Store the last message ID to delete it later
last_message_id = None

# Store the running autobn.py process
autobn_process = None

# Image counter
image_counter = 0

@bot.event
async def on_ready():
    print(f'{bot.user} has logged in!')
    screenshot_checker.start()

@tasks.loop(seconds=CHECK_INTERVAL)
async def screenshot_checker():
    """Check for screenshot and send it if found"""
    global last_message_id, image_counter
    
    # Check if screenshot exists
    if not os.path.exists(SCREENSHOT_PATH):
        return
    
    # Find the channel
    channel = discord.utils.get(bot.get_all_channels(), name=CHANNEL_NAME)
    if not channel:
        print(f"Channel '{CHANNEL_NAME}' not found!")
        return
    
    try:
        # Delete previous message if it exists
        if last_message_id:
            try:
                old_message = await channel.fetch_message(last_message_id)
                await old_message.delete()
                print("Deleted previous screenshot message")
            except discord.NotFound:
                print("Previous message not found (may have been deleted)")
            except discord.Forbidden:
                print("No permission to delete previous message")
            except Exception as e:
                print(f"Error deleting previous message: {e}")
        
        # Send new screenshot
        with open(SCREENSHOT_PATH, 'rb') as f:
            file = discord.File(f, filename="screenshot.png")
            # Increment the image counter
            image_counter += 1
            # Include counter in the message
            message = await channel.send(f"📸 Screenshot #{image_counter}", file=file)
            last_message_id = message.id
            print(f"Screenshot #{image_counter} sent to #{CHANNEL_NAME}")
        
        # Delete local file
        os.remove(SCREENSHOT_PATH)
        print("Local screenshot deleted")
        
    except FileNotFoundError:
        print("Screenshot file was removed before sending")
    except discord.Forbidden:
        print("No permission to send messages in the channel")
    except Exception as e:
        print(f"Error sending screenshot: {e}")

@screenshot_checker.before_loop
async def before_screenshot_checker():
    """Wait until bot is ready before starting the loop"""
    await bot.wait_until_ready()

@bot.command(name='status')
async def status_command(ctx):
    """Check bot status and last screenshot info"""
    screenshot_exists = os.path.exists(SCREENSHOT_PATH)
    
    # Check if autobn.py is running
    autobn_running = autobn_process and autobn_process.poll() is None
    
    status_msg = (
        f"🤖 Bot is running\n"
        f"📁 Screenshot exists: {screenshot_exists}\n"
        f"🐍 {SCRIPT_NAME} running: {autobn_running}\n"
        f"📊 Images sent: {image_counter}"
    )
    
    if autobn_running:
        status_msg += f" (PID: {autobn_process.pid})"
    
    if last_message_id:
        status_msg += f"\n📸 Last message ID: {last_message_id}"
    
    await ctx.send(status_msg)

@bot.command(name='screenshot')
async def screenshot_command(ctx):
    """Take a screenshot of all monitors and send to Discord"""
    global image_counter
    
    try:
        await ctx.send("📸 Taking screenshot...")
        
        # Capture entire screen including all monitors
        screenshot = ImageGrab.grab(all_screens=True)
        
        # Convert to bytes for Discord
        img_bytes = io.BytesIO()
        screenshot.save(img_bytes, format='PNG')
        img_bytes.seek(0)
        
        # Increment counter for manual screenshots too
        image_counter += 1
        
        # Send to Discord with counter
        file = discord.File(img_bytes, filename="full_screenshot.png")
        await ctx.send(f"📸 Screenshot #{image_counter} captured:", file=file)
        
        print(f"Manual screenshot #{image_counter} taken and sent")
        
    except Exception as e:
        await ctx.send(f"❌ Error taking screenshot: {e}")
        print(f"Error taking screenshot: {e}")

@bot.command(name='counter')
async def counter_command(ctx):
    """Show the current image counter value"""
    await ctx.send(f"📊 Images sent: {image_counter}")
    print(f"Counter command used. Current count: {image_counter}")

@bot.command(name='resetcounter')
async def reset_counter_command(ctx):
    """Reset the image counter to zero"""
    global image_counter
    old_count = image_counter
    image_counter = 0
    await ctx.send(f"🔄 Image counter reset from {old_count} to 0")
    print(f"Counter reset from {old_count} to 0")

@bot.command(name='stop')
async def stop_command(ctx):
    """Create a stop.txt file, monitor process shutdown, and reset counter"""
    global autobn_process, image_counter
    
    try:
        # Check if process is even running
        if not autobn_process or autobn_process.poll() is not None:
            await ctx.send("❌ autobn.py is not running!")
            return
        
        # Create empty stop.txt file in the same directory as the screenshot path
        screenshot_dir = os.path.dirname(SCREENSHOT_PATH)
        if not screenshot_dir:  # If no directory specified, use current directory
            stop_file_path = "stop.txt"
        else:
            stop_file_path = os.path.join(screenshot_dir, "stop.txt")
        
        # Create empty file
        with open(stop_file_path, 'w') as f:
            pass  # Creates an empty file
        
        await ctx.send(f"✅ Created stop.txt at: `{stop_file_path}`\n⏳ Monitoring shutdown...")
        print(f"Stop file created: {stop_file_path}")
        
        # Monitor the process shutdown
        check_count = 0
        while autobn_process and autobn_process.poll() is None:
            await asyncio.sleep(2)  # Wait 2 seconds
            check_count += 1
            
            # Send status every few checks to avoid spam
            if check_count % 3 == 0:  # Every 6 seconds (3 * 2 seconds)
                await ctx.send(f"⏳ Still waiting for {SCRIPT_NAME} to stop... ({check_count * 2}s)")
            
            # Safety timeout after 60 seconds
            if check_count >= 500:  # 30 * 2 = 60 seconds
                await ctx.send(f"⚠️ {SCRIPT_NAME} didn't stop after 1000 seconds. Use `!kill` to force stop.")
                return
        
        # Process has stopped
        autobn_process = None
        
        # Store old counter value for message
        old_count = image_counter
        
        # Reset counter when process stops
        image_counter = 0
        
        await ctx.send(f"✅ {SCRIPT_NAME} has stopped successfully! ({check_count * 2}s)\n🔄 Image counter reset from {old_count} to 0")
        print(f"{SCRIPT_NAME} stopped after {check_count * 2} seconds")
        print(f"Counter reset from {old_count} to 0")
        
    except Exception as e:
        await ctx.send(f"❌ Error during stop process: {e}")
        print(f"Error during stop process: {e}")

@bot.command(name='start')
async def start_command(ctx):
    """Start autobn.py using virtual environment Python"""
    global autobn_process
    
    try:
        # Check if process is already running
        if autobn_process and autobn_process.poll() is None:
            await ctx.send("❌ autobn.py is already running!")
            return
        
        # Check if files exist
        if not os.path.exists(PYTHON_PATH):
            await ctx.send(f"❌ Virtual environment Python not found at: `{PYTHON_PATH}`")
            return
            
        if not os.path.exists(SCRIPT_NAME):
            await ctx.send(f"❌ Script not found: `{SCRIPT_NAME}`")
            return
        
        # Start the process (hidden, no window)
        autobn_process = subprocess.Popen(
            [PYTHON_PATH, SCRIPT_NAME],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            creationflags=subprocess.CREATE_NO_WINDOW  # Runs hidden without window
        )
        
        await ctx.send(f"✅ Started {SCRIPT_NAME} (PID: {autobn_process.pid})")
        print(f"Started {SCRIPT_NAME} with PID: {autobn_process.pid}")
        
    except Exception as e:
        await ctx.send(f"❌ Error starting {SCRIPT_NAME}: {e}")
        print(f"Error starting {SCRIPT_NAME}: {e}")

@bot.command(name='kill')
async def kill_command(ctx):
    """Stop the running autobn.py process"""
    global autobn_process
    
    try:
        if not autobn_process or autobn_process.poll() is not None:
            await ctx.send(f"❌ {SCRIPT_NAME} is not running!")
            return
        
        # Terminate the process
        autobn_process.terminate()
        
        # Wait a moment for graceful shutdown
        try:
            autobn_process.wait(timeout=5)
            await ctx.send(f"✅ {SCRIPT_NAME} stopped gracefully")
        except subprocess.TimeoutExpired:
            # Force kill if it doesn't stop gracefully
            autobn_process.kill()
            await ctx.send(f"⚠️ {SCRIPT_NAME} force-killed (didn't stop gracefully)")
        
        autobn_process = None
        print(f"{SCRIPT_NAME} process stopped")
        
    except Exception as e:
        await ctx.send(f"❌ Error stopping {SCRIPT_NAME}: {e}")
        print(f"Error stopping {SCRIPT_NAME}: {e}")

# Error handling
@bot.event
async def on_error(event, *args, **kwargs):
    print(f"An error occurred in {event}")

# Run the bot
if __name__ == "__main__":
    # Get token from environment variable
    TOKEN = os.getenv('DISCORD_TOKEN')
    
    if not TOKEN:
        print("Error: DISCORD_TOKEN not found in environment variables!")
        print("Please create a .env file with your bot token.")
        print("See the .env.example file for reference.")
    else:
        bot.run(TOKEN)