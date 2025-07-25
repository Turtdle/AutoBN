import discord
from discord.ext import commands, tasks
import os
import asyncio
import subprocess
from dotenv import load_dotenv
from PIL import ImageGrab
import io
import threading
import queue

# Load environment variables
load_dotenv()

# Bot setup
intents = discord.Intents.default()
# Enable message content intent for commands (requires privileged intent)
# If you don't enable this in Discord Developer Portal, comment out the next line
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Configuration from environment variables
SCREENSHOT_PATH = os.getenv("SCREENSHOT_PATH", "shared_folder\\screenshot.png")
CHANNEL_NAME = os.getenv("CHANNEL_NAME", "battle-nations")
CHECK_INTERVAL = int(os.getenv("CHECK_INTERVAL", "10"))  # seconds
PYTHON_PATH = os.getenv("PYTHON_PATH", ".venv\\Scripts\\python.exe")
SCRIPT_NAME = os.getenv("SCRIPT_NAME", "autobn.py")

# Store the last message ID to delete it later
last_message_id = None

# Store the running autobn.py process
autobn_process = None

# Image counter
image_counter = 0

# Console message tracking
last_console_message = "No console output yet"
console_message_id = None
console_output_queue = queue.Queue()


def read_process_output(process, output_queue):
    """Read process output in a separate thread using a different approach"""
    try:
        output_queue.put("Console monitor started - waiting for output...")

        while process.poll() is None:  # While process is still running
            try:
                # Try to read a line with a short timeout
                line = process.stdout.readline()
                if line:
                    clean_line = line.strip()
                    if clean_line:
                        output_queue.put(clean_line)
                else:
                    # If no line available, sleep briefly
                    import time

                    time.sleep(0.1)
            except Exception as e:
                output_queue.put(f"Read error: {e}")
                break

        # Process ended, try to read any remaining output
        try:
            remaining = process.stdout.read()
            if remaining:
                for line in remaining.split("\n"):
                    clean_line = line.strip()
                    if clean_line:
                        output_queue.put(clean_line)
        except:
            pass

        output_queue.put("Process ended")

    except Exception as e:
        output_queue.put(f"Thread error: {e}")


@bot.event
async def on_ready():
    print(f"{bot.user} has logged in!")
    screenshot_checker.start()
    console_monitor.start()


@tasks.loop(seconds=2)  # Check console output every 2 seconds
async def console_monitor():
    """Monitor console output and update Discord message"""
    global last_console_message, console_message_id

    # Only monitor if autobn is running
    if not autobn_process or autobn_process.poll() is not None:
        return

    # Check for new console messages
    new_messages = []
    while not console_output_queue.empty():
        try:
            message = console_output_queue.get_nowait()
            new_messages.append(message)
        except queue.Empty:
            break

    # If we have new messages, update the display
    if new_messages:
        # Use the most recent message
        last_console_message = new_messages[-1]

        # Find the channel
        channel = discord.utils.get(bot.get_all_channels(), name=CHANNEL_NAME)
        if not channel:
            return

        try:
            console_display = f"🖥️ **Console Output:**\n```\n{last_console_message}\n```"

            if console_message_id:
                # Edit existing message
                try:
                    console_msg = await channel.fetch_message(console_message_id)
                    await console_msg.edit(content=console_display)
                except discord.NotFound:
                    # Message was deleted, create new one
                    console_msg = await channel.send(console_display)
                    console_message_id = console_msg.id
                except Exception as e:
                    print(f"Error editing console message: {e}")
            else:
                # Create new message
                console_msg = await channel.send(console_display)
                console_message_id = console_msg.id

        except Exception as e:
            print(f"Error updating console message: {e}")


@console_monitor.before_loop
async def before_console_monitor():
    """Wait until bot is ready before starting the loop"""
    await bot.wait_until_ready()


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
        with open(SCREENSHOT_PATH, "rb") as f:
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


@bot.command(name="status")
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

    if console_message_id:
        status_msg += f"\n🖥️ Console message ID: {console_message_id}"

    status_msg += f"\n🖥️ Last console: {last_console_message}"

    await ctx.send(status_msg)


@bot.command(name="console")
async def console_command(ctx):
    """Show the current console message"""
    await ctx.send(f"🖥️ **Current Console Output:**\n```\n{last_console_message}\n```")


@bot.command(name="testconsole")
async def test_console_command(ctx):
    """Test console output by running a simple Python command"""
    global autobn_process, last_console_message, console_message_id

    try:
        # Stop existing process if running
        if autobn_process and autobn_process.poll() is None:
            await ctx.send("⚠️ Stopping existing process first...")
            autobn_process.terminate()
            try:
                autobn_process.wait(timeout=3)
            except subprocess.TimeoutExpired:
                autobn_process.kill()

        # Reset console tracking
        last_console_message = "Testing console output..."
        console_message_id = None

        # Clear the queue
        while not console_output_queue.empty():
            try:
                console_output_queue.get_nowait()
            except queue.Empty:
                break

        # Run a simple test command that should produce output
        test_script = """
import time
import sys

# Force unbuffered output
sys.stdout.reconfigure(line_buffering=True)
sys.stderr.reconfigure(line_buffering=True)

print("Test message 1", flush=True)
sys.stdout.flush()
print("Test message 2", flush=True) 
sys.stdout.flush()
time.sleep(2)
print("Test message 3", flush=True)
sys.stdout.flush()
time.sleep(2)
print("Final test message", flush=True)
sys.stdout.flush()
"""

        # Write test script to temp file
        with open("test_console.py", "w") as f:
            f.write(test_script)

        # Start the test process with additional environment variables
        env = os.environ.copy()
        env["PYTHONUNBUFFERED"] = "1"  # Force Python to be unbuffered

        autobn_process = subprocess.Popen(
            [PYTHON_PATH, "test_console.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=0,  # Unbuffered
            universal_newlines=True,
            env=env,  # Use the modified environment
            creationflags=subprocess.CREATE_NO_WINDOW,
        )

        # Start the output reading thread
        output_thread = threading.Thread(
            target=read_process_output,
            args=(autobn_process, console_output_queue),
            daemon=True,
        )
        output_thread.start()

        await ctx.send(f"✅ Started test console script (PID: {autobn_process.pid})")
        await ctx.send(
            "📝 Watch for console updates! Test will run for about 6 seconds."
        )

    except Exception as e:
        await ctx.send(f"❌ Error running test: {e}")
        print(f"Error running test: {e}")


@bot.command(name="debug")
async def debug_command(ctx):
    """Debug console monitoring status"""
    queue_size = console_output_queue.qsize()
    process_running = autobn_process and autobn_process.poll() is None

    debug_info = f"""🔍 **Debug Info:**
Process running: {process_running}
Queue size: {queue_size}
Console message ID: {console_message_id}
Last console: `{last_console_message}`"""

    if autobn_process:
        debug_info += f"\nProcess PID: {autobn_process.pid}"
        debug_info += f"\nProcess poll: {autobn_process.poll()}"

    await ctx.send(debug_info)


@bot.command(name="testsubprocess")
async def test_subprocess_command(ctx):
    """Test console output using subprocess.run instead of Popen"""
    global autobn_process, last_console_message, console_message_id

    try:
        await ctx.send("🧪 Testing subprocess.run method...")

        # Test with subprocess.run first
        test_script = """
import time
print("Test message 1")
print("Test message 2") 
time.sleep(1)
print("Test message 3")
time.sleep(1)
print("Final test message")
"""

        # Write test script to temp file
        with open("test_subprocess.py", "w") as f:
            f.write(test_script)

        # Use subprocess.run to capture all output at once
        result = subprocess.run(
            [PYTHON_PATH, "test_subprocess.py"],
            capture_output=True,
            text=True,
            env={**os.environ, "PYTHONUNBUFFERED": "1"},
        )

        await ctx.send(f"📝 **subprocess.run output:**\n```\n{result.stdout}\n```")

        if result.stderr:
            await ctx.send(f"❌ **Errors:**\n```\n{result.stderr}\n```")

        await ctx.send(f"✅ Return code: {result.returncode}")

    except Exception as e:
        await ctx.send(f"❌ Error running subprocess test: {e}")
        print(f"Error running subprocess test: {e}")


@bot.command(name="testlog")
async def test_log_command(ctx):
    """Test autobn.py output by running it briefly and capturing what it prints"""
    try:
        await ctx.send("🔍 Testing autobn.py output (will run for 10 seconds)...")

        # Check if autobn.py exists
        if not os.path.exists(SCRIPT_NAME):
            await ctx.send(f"❌ {SCRIPT_NAME} not found!")
            return

        # Run autobn.py for a short time to see what it outputs
        process = subprocess.Popen(
            [PYTHON_PATH, SCRIPT_NAME],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            env={**os.environ, "PYTHONUNBUFFERED": "1"},
            creationflags=subprocess.CREATE_NO_WINDOW,
        )

        # Wait 10 seconds then terminate
        await asyncio.sleep(10)

        process.terminate()
        try:
            output, _ = process.communicate(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()
            output, _ = process.communicate()

        if output.strip():
            await ctx.send(
                f"📝 **autobn.py output (first 10 seconds):**\n```\n{output[:1900]}\n```"
            )
        else:
            await ctx.send("❌ No output captured from autobn.py in 10 seconds")
            await ctx.send(
                "💡 autobn.py might not print to console, or only prints when certain events happen"
            )

    except Exception as e:
        await ctx.send(f"❌ Error testing autobn.py: {e}")
        print(f"Error testing autobn.py: {e}")


@bot.command(name="screenshot")
async def screenshot_command(ctx):
    """Take a screenshot of all monitors and send to Discord"""
    global image_counter

    try:
        await ctx.send("📸 Taking screenshot...")

        # Capture entire screen including all monitors
        screenshot = ImageGrab.grab(all_screens=True)

        # Convert to bytes for Discord
        img_bytes = io.BytesIO()
        screenshot.save(img_bytes, format="PNG")
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


@bot.command(name="counter")
async def counter_command(ctx):
    """Show the current image counter value"""
    await ctx.send(f"📊 Images sent: {image_counter}")
    print(f"Counter command used. Current count: {image_counter}")


@bot.command(name="resetcounter")
async def reset_counter_command(ctx):
    """Reset the image counter to zero"""
    global image_counter
    old_count = image_counter
    image_counter = 0
    await ctx.send(f"🔄 Image counter reset from {old_count} to 0")
    print(f"Counter reset from {old_count} to 0")


@bot.command(name="stop")
async def stop_command(ctx):
    """Create a stop.txt file, monitor process shutdown, and reset counter"""
    global autobn_process, image_counter, console_message_id, last_console_message

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
        with open(stop_file_path, "w") as f:
            pass  # Creates an empty file

        await ctx.send(
            f"✅ Created stop.txt at: `{stop_file_path}`\n⏳ Monitoring shutdown..."
        )
        print(f"Stop file created: {stop_file_path}")

        # Monitor the process shutdown
        check_count = 0
        while autobn_process and autobn_process.poll() is None:
            await asyncio.sleep(2)  # Wait 2 seconds
            check_count += 1

            # Send status every few checks to avoid spam
            if check_count % 3 == 0:  # Every 6 seconds (3 * 2 seconds)
                await ctx.send(
                    f"⏳ Still waiting for {SCRIPT_NAME} to stop... ({check_count * 2}s)"
                )

            # Safety timeout after 60 seconds
            if check_count >= 500:  # 30 * 2 = 60 seconds
                await ctx.send(
                    f"⚠️ {SCRIPT_NAME} didn't stop after 1000 seconds. Use `!kill` to force stop."
                )
                return

        # Process has stopped
        autobn_process = None

        # Store old counter value for message
        old_count = image_counter

        # Reset counter when process stops
        image_counter = 0

        # Reset console tracking
        console_message_id = None
        last_console_message = "No console output yet"

        await ctx.send(
            f"✅ {SCRIPT_NAME} has stopped successfully! ({check_count * 2}s)\n🔄 Image counter reset from {old_count} to 0"
        )
        print(f"{SCRIPT_NAME} stopped after {check_count * 2} seconds")
        print(f"Counter reset from {old_count} to 0")

    except Exception as e:
        await ctx.send(f"❌ Error during stop process: {e}")
        print(f"Error during stop process: {e}")


@bot.command(name="start")
async def start_command(ctx):
    """Start autobn.py using virtual environment Python"""
    global autobn_process, last_console_message, console_message_id

    try:
        # Check if process is already running
        if autobn_process and autobn_process.poll() is None:
            await ctx.send("❌ autobn.py is already running!")
            return

        # Check if files exist
        if not os.path.exists(PYTHON_PATH):
            await ctx.send(
                f"❌ Virtual environment Python not found at: `{PYTHON_PATH}`"
            )
            return

        if not os.path.exists(SCRIPT_NAME):
            await ctx.send(f"❌ Script not found: `{SCRIPT_NAME}`")
            return

        # Reset console tracking
        last_console_message = "Starting autobn.py..."
        console_message_id = None

        # Clear the queue
        while not console_output_queue.empty():
            try:
                console_output_queue.get_nowait()
            except queue.Empty:
                break

        # Start the process (hidden, no window) with unbuffered environment
        env = os.environ.copy()
        env["PYTHONUNBUFFERED"] = "1"  # Force Python to be unbuffered

        autobn_process = subprocess.Popen(
            [PYTHON_PATH, SCRIPT_NAME],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,  # Redirect stderr to stdout
            text=True,
            bufsize=0,  # Unbuffered
            universal_newlines=True,
            env=env,  # Use the modified environment
            creationflags=subprocess.CREATE_NO_WINDOW,  # Runs hidden without window
        )

        # Start the output reading thread
        output_thread = threading.Thread(
            target=read_process_output,
            args=(autobn_process, console_output_queue),
            daemon=True,
        )
        output_thread.start()

        await ctx.send(f"✅ Started {SCRIPT_NAME} (PID: {autobn_process.pid})")
        print(f"Started {SCRIPT_NAME} with PID: {autobn_process.pid}")

    except Exception as e:
        await ctx.send(f"❌ Error starting {SCRIPT_NAME}: {e}")
        print(f"Error starting {SCRIPT_NAME}: {e}")


@bot.command(name="kill")
async def kill_command(ctx):
    """Stop the running autobn.py process"""
    global autobn_process, console_message_id, last_console_message

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

        # Reset console tracking
        console_message_id = None
        last_console_message = "No console output yet"

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
    TOKEN = os.getenv("DISCORD_TOKEN")

    if not TOKEN:
        print("Error: DISCORD_TOKEN not found in environment variables!")
        print("Please create a .env file with your bot token.")
        print("See the .env.example file for reference.")
    else:
        bot.run(TOKEN)
