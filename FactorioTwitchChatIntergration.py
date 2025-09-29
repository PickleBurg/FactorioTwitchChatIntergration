from twitchAPI.chat import Chat, EventData, ChatMessage, ChatSub, ChatCommand
from twitchAPI.type import AuthScope, ChatEvent
from twitchAPI.eventsub.websocket import EventSubWebsocket
from twitchAPI.oauth import UserAuthenticator
from twitchAPI.twitch import Twitch
from Config import (APP_ID, APP_SECRETS, USER_SCOPE, TARGET_CHANNEL, 
                   RCON_HOST, RCON_PORT, RCON_PASS, DEFAULT_PLAYER,
                   IRON_PLATE_COUNT, COPPER_PLATE_COUNT, COMMAND_COOLDOWN)
import asyncio
import random
import logging
import html
import time
from collections import defaultdict
from factorio_rcon import AsyncRCONClient

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Rate limiting for commands (user_id -> last_command_time)
last_command_time = defaultdict(float)

# ------------------------------------------------------------------------------------------------------- #
# Factorio Twitch Chat Integration 
# ------------------------------------------------------------------------------------------------------- #

def is_command_on_cooldown(user_id: str) -> bool:
    """
    Check if a user is on cooldown for commands.
    
    Args:
        user_id: The user's ID
        
    Returns:
        True if user is on cooldown, False otherwise
    """
    current_time = time.time()
    last_time = last_command_time.get(user_id, 0)
    return (current_time - last_time) < COMMAND_COOLDOWN

def update_command_time(user_id: str) -> None:
    """Update the last command time for a user."""
    last_command_time[user_id] = time.time()

def get_cooldown_remaining(user_id: str) -> int:
    """Get remaining cooldown time in seconds for a user."""
    current_time = time.time()
    last_time = last_command_time.get(user_id, 0)
    remaining = COMMAND_COOLDOWN - (current_time - last_time)
    return max(0, int(remaining))

def sanitize_message(message: str) -> str:
    """Sanitize user input to prevent injection attacks."""
    if not message:
        return ""
    
    # HTML escape the message to prevent potential issues
    sanitized = html.escape(message)
    
    # Remove or escape problematic characters for Factorio commands
    sanitized = sanitized.replace('"', '\\"').replace('\\', '\\\\')
    
    # Limit message length
    return sanitized[:500] if len(sanitized) > 500 else sanitized

async def send_to_factorio(message: str, user: str = None) -> str:
    """
    Send a message or command to Factorio via RCON.
    
    Args:
        message: The message or command to send
        user: The username for chat messages (None for commands)
    
    Returns:
        The response from the Factorio server, or None if failed
    """
    if not message or (not user and not message.startswith("/")):
        logging.warning("Invalid message or user parameters")
        return None

    try:
        async with AsyncRCONClient(RCON_HOST, RCON_PORT, RCON_PASS) as rcon:
            if message.startswith("/"):
                # This is a command
                response = await rcon.send_command(message)
                logging.info(f"Sent command: {message[:50]}...")
            else:
                # This is a chat message
                sanitized_message = sanitize_message(message)
                sanitized_user = sanitize_message(user)
                
                chat_line = f'/silent-command game.print("[color=purple]{sanitized_user}[/color]: {sanitized_message}")'
                response = await rcon.send_command(chat_line)
                logging.info(f"Sent chat message from {user}")

            return response
            
    except Exception as e:
        logging.error(f"Failed to send message to Factorio: {e}")
        return None

# Register event handlers
def register_event_handlers(chat: Chat) -> None:
    """Register all event handlers and commands for the chat bot."""
    chat.register_event(ChatEvent.READY, on_ready)
    chat.register_event(ChatEvent.MESSAGE, on_message)

    chat.register_command("egg", egg_command)
    chat.register_command("IronPlates", iron_plates_command)
    chat.register_command("CopperPlates", copper_plates_command)

# Commands
async def egg_command(cmd: ChatCommand) -> None:
    """Handle the egg command."""
    await cmd.reply("EGGG!!!!")

async def give_items_to_player(player_name: str, item_name: str, count: int, sender: str) -> bool:
    """
    Give items to a player and thank the sender.
    
    Args:
        player_name: The Factorio player to give items to
        item_name: The item to give
        count: Number of items to give
        sender: The Twitch user who triggered the command
    
    Returns:
        True if successful, False otherwise
    """
    try:
        # Give items to player
        give_command = f'/sc game.players["{player_name}"].insert{{name="{item_name}", count={count}}}'
        result = await send_to_factorio(give_command)
        
        if result is not None:
            # Thank the sender in-game
            thank_message = f"Thanks {sender} for the {item_name.replace('-', ' ')}!"
            await send_to_factorio(thank_message, user="Server")
            return True
        else:
            logging.error(f"Failed to give {item_name} to {player_name}")
            return False
            
    except Exception as e:
        logging.error(f"Error giving items to player: {e}")
        return False

async def iron_plates_command(cmd: ChatCommand) -> None:
    """Handle the iron plates command with rate limiting."""
    user_id = cmd.user.id
    sender_name = cmd.user.display_name
    
    if is_command_on_cooldown(user_id):
        remaining = get_cooldown_remaining(user_id)
        await cmd.reply(f"Please wait {remaining} seconds before using another command!")
        return
    
    await cmd.reply("Sending Iron plates!")
    
    success = await give_items_to_player(DEFAULT_PLAYER, "iron-plate", IRON_PLATE_COUNT, sender_name)
    if success:
        update_command_time(user_id)
    else:
        await cmd.reply("Sorry, there was an error sending the items!")

async def copper_plates_command(cmd: ChatCommand) -> None:
    """Handle the copper plates command with rate limiting."""
    user_id = cmd.user.id
    sender_name = cmd.user.display_name
    
    if is_command_on_cooldown(user_id):
        remaining = get_cooldown_remaining(user_id)
        await cmd.reply(f"Please wait {remaining} seconds before using another command!")
        return
    
    await cmd.reply("Sending Copper plates!")
    
    success = await give_items_to_player(DEFAULT_PLAYER, "copper-plate", COPPER_PLATE_COUNT, sender_name)
    if success:
        update_command_time(user_id)
    else:
        await cmd.reply("Sorry, there was an error sending the items!")

# Channel points
# TODO: Add channel point reward handlers here

# Listen to chat messages
async def on_message(msg: ChatMessage) -> None:
    """Handle incoming chat messages."""
    try:
        if not msg.text:
            return
            
        if msg.text.startswith("!"):
            # This is treated as a command - be careful with validation
            command = msg.text.strip()
            if len(command) > 1:  # Make sure it's not just "!"
                logging.info(f"Processing command from {msg.user.display_name}: {command}")
                await send_to_factorio(command)
        else:
            # Send regular chat message
            await send_to_factorio(msg.text, user=msg.user.display_name)
            
    except Exception as e:
        logging.error(f"Error processing message: {e}")







# ------------------------------------------------------------------------------------------------------- #
# Bot Setup 
# ------------------------------------------------------------------------------------------------------- #

def validate_configuration() -> bool:
    """Validate that all required configuration values are set."""
    required_configs = {
        'APP_ID': APP_ID,
        'APP_SECRETS': APP_SECRETS,
        'TARGET_CHANNEL': TARGET_CHANNEL,
        'RCON_PASS': RCON_PASS
    }
    
    missing = [name for name, value in required_configs.items() if not value]
    
    if missing:
        logging.error(f"Missing required configuration values: {', '.join(missing)}")
        return False
    
    logging.info("Configuration validation passed")
    return True

async def run_bot() -> None:
    """Main bot setup and execution function."""
    if not validate_configuration():
        logging.error("Configuration validation failed. Please check your Config.py file.")
        return

    try:
        # Authenticate application
        logging.info("Starting bot authentication...")
        bot = await Twitch(APP_ID, APP_SECRETS)
        auth = UserAuthenticator(bot, USER_SCOPE)
        token, refresh_token = await auth.authenticate()
        await bot.set_user_authentication(token, USER_SCOPE, refresh_token)

        # Create chat instance
        chat = await Chat(bot)

        # Register event handlers
        register_event_handlers(chat)

        # Start chatbot
        logging.info("Starting chat bot...")
        chat.start()

        try:
            input("Press Enter to stop the bot...\n")
        finally:
            logging.info("Shutting down bot...")
            chat.stop()
            await bot.close()
            logging.info("Bot stopped successfully")
            
    except Exception as e:
        logging.error(f"Error running bot: {e}")
        raise

async def on_ready(ready_event: EventData) -> None:
    """Handle bot ready event."""
    try:
        # Connect to TARGET_CHANNEL
        await ready_event.chat.join_room(TARGET_CHANNEL)
        
        # Print Ready Message
        logging.info(f'Bot is ready and connected to {TARGET_CHANNEL}!')
        print(f'Bot is ready and connected to {TARGET_CHANNEL}!')
        
    except Exception as e:
        logging.error(f"Error in on_ready: {e}")

if __name__ == "__main__":
    asyncio.run(run_bot())