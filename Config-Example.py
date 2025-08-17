# config.py
from twitchAPI.type import AuthScope

# Rename this file to Config.py and fill in the values below. Refer to README.md for more information.

APP_ID = "" #Bot ClientID
APP_SECRETS = ""#Bot Client Secret
USER_SCOPE = [AuthScope.CHAT_READ, AuthScope.CHAT_EDIT, AuthScope.CHANNEL_MANAGE_BROADCAST]
TARGET_CHANNEL = "" #Channel to connect to

RCON_HOST = "127.0.0.1" # Factorio RCON Host
RCON_PORT = 25575 # Factorio RCON Port
RCONPASS = "" # Factorio RCON Password
