# Example configuration file
# Copy this file to Config.py and fill in your values

from twitchAPI.type import AuthScope

# Twitch Bot Configuration
APP_ID = "your_twitch_app_client_id_here"  # Bot ClientID from https://dev.twitch.tv/
APP_SECRETS = "your_twitch_app_client_secret_here"  # Bot Client Secret
USER_SCOPE = [AuthScope.CHAT_READ, AuthScope.CHAT_EDIT, AuthScope.CHANNEL_MANAGE_BROADCAST]
TARGET_CHANNEL = "your_twitch_channel_name"  # Channel to connect to (without #)

# Factorio RCON Configuration
RCON_HOST = "127.0.0.1"  # Factorio RCON Host (localhost if running on same machine)
RCON_PORT = 25575  # Factorio RCON Port (default is 25575)
RCON_PASS = "your_factorio_rcon_password"  # Factorio RCON Password (set in Factorio settings)

# Game Configuration
DEFAULT_PLAYER = "YourFactorioPlayerName"  # Player who will receive items from commands

# Item Command Configuration
IRON_PLATE_COUNT = 100  # Number of iron plates to give per command
COPPER_PLATE_COUNT = 100  # Number of copper plates to give per command