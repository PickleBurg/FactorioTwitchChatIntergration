# config.py
from twitchAPI.type import AuthScope

APP_ID = "" #Bot ClientID
APP_SECRETS = "" #Bot Client Secret
USER_SCOPE = [AuthScope.CHAT_READ, AuthScope.CHAT_EDIT, AuthScope.CHANNEL_MANAGE_BROADCAST]
TARGET_CHANNEL = "" #Channel to connect to

RCON_HOST = "127.0.0.1" # Factorio RCON Host
RCON_PORT = 25575 # Factorio RCON Port
RCON_PASS = "" # Factorio RCON Password

# Default player name for item commands (make this configurable)
DEFAULT_PLAYER = "TerriblenessDonG"

# Item command configuration
IRON_PLATE_COUNT = 100
COPPER_PLATE_COUNT = 100

# Rate limiting (seconds between commands per user)
COMMAND_COOLDOWN = 30
