from twitchAPI.chat import Chat,EventData,ChatMessage,ChatSub,ChatCommand
from twitchAPI.type import AuthScope,ChatEvent
from twitchAPI.eventsub.websocket import EventSubWebsocket
from twitchAPI.oauth import UserAuthenticator
from twitchAPI.twitch import Twitch
from Config import APP_ID, APP_SECRETS, USER_SCOPE, TARGET_CHANNEL, RCONPASSWORD, RCON_HOST, RCON_PORT, RCON_PASS
import asyncio
import random
from factorio_rcon import AsyncRCONClient

# ------------------------------------------------------------------------------------------------------- #
# Factorio Twitch Chat Integration 
# ------------------------------------------------------------------------------------------------------- #
async def send_to_factorio(message, user=None):
    async with AsyncRCONClient(RCON_HOST, RCON_PORT, RCON_PASS) as rcon:

        if user == None:
            return

        if message.startswith("/"):
            response = await rcon.send_command(message)
        else:
            # Format message with username in purple
            chat_line = f'/silent-command game.print("[color=purple]{user}[/color]: {message}")'
            response = await rcon.send_command(chat_line)

        return response

#register event handlers
def register_Event_Handlers(chat):
    
    chat.register_event(ChatEvent.READY, on_ready)
    chat.register_event(ChatEvent.MESSAGE, on_message)

    chat.register_command("egg",egg_command )
    chat.register_command("IronPlates",IronPlates_command )
    chat.register_command("CopperPlates",CopperPlates_command )

# Commands
async def egg_command(cmd: ChatCommand):
    await cmd.reply("EGGG!!!!")

async def IronPlates_command(cmd: ChatCommand):
    sender_name = cmd.user.display_name

    await cmd.reply("Sending Iron plates!")
    await send_to_factorio('/sc game.players["TerriblenessDonG"].insert{name="iron-plate", count=100}')
    #TODO: Add ingmae text to thank the sender

async def CopperPlates_command(cmd: ChatCommand):
    await cmd.reply("Sending Copper plates!")
    await send_to_factorio('/sc game.players["TerriblenessDonG"].insert{name="copper-plate", count=100}')

# Channel points



# Listen to chat messages
async def on_message(msg: ChatMessage):
    if msg.text.startswith("!"):
        await send_to_factorio(msg.text)
    else:
        # send the message with username in purple
        await send_to_factorio(msg.text, user=msg.user.display_name)







# ------------------------------------------------------------------------------------------------------- #
# Bot Setup 
# ------------------------------------------------------------------------------------------------------- #

# Bot Setup function
async def run_bot():

    # Authenticate application
    bot = await Twitch(APP_ID, APP_SECRETS)
    auth = UserAuthenticator(bot, USER_SCOPE)
    token, refresh_token = await auth.authenticate()
    await bot.set_user_authentication(token, USER_SCOPE, refresh_token)

    # Create chat instance
    chat = await Chat(bot)

    #register event handlers
    register_Event_Handlers(chat)

    # Start chatbot
    chat.start()

    try:
        input("Press Enter to stop the bot...\n")
    finally:
        chat.stop()
        await bot.close()

#Bot connected correctly
async def on_ready(ready_event: EventData):
    #Connect to TARGET_CHANNEL
    await ready_event.chat.join_room(TARGET_CHANNEL)

    # Print Ready Message
    print(f'Bot is ready and connected to {TARGET_CHANNEL}!')

asyncio.run(run_bot())