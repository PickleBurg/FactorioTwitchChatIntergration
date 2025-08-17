# Factorio Twitch Chat Bot Setup

## 1. Generate Client ID
1. Go to [Twitch Developers](https://dev.twitch.tv/) and log in with your Twitch account.  
2. Navigate to **Your Console → Register Your Application**.  
3. Fill in the fields:
   - **Name:** `FactorioChatBot`
   - **OAuth Redirect URLs:** `https://twitchapps.com/tokengen/`
   - **Category:** `Chat Bot`
4. Copy the **Client ID** and paste it into `config.py`.
5. Copy the **Client Secret** and paste it into `config.py`.

---

## 2. Change Factorio RCON Settings (Local Hosting)
If you are hosting the game locally (not a dedicated server), follow these steps:

1. On the **main menu screen**, hold **Ctrl + Alt** and left-click **Settings**.  
2. Select the last item: **The rest**.  
3. Update the following:
   - `local-rcon-socket`: `127.0.0.1:25575` (or your RCON detaisl from a hosted service provider)
   - `local-rcon-password`: `my_password` (or any secret password; must match `settings.txt`)  
4. Click **Confirm**, then return to the main menu.  
5. Go to **Multiplayer → Host a save game**.  
6. Select the save you want to host and click **Play**.

---

## 3. Configure `config.cfg`
1. Open `config.py`.  
2. Fill in the following sections:

```
APP_ID = ""        ; Bot ClientID
APP_SECRETS = ""         ; #Bot Client Secret
TARGET_CHANNEL = ""                 ;  #Channel to connect to

RCON_HOST = 0.0.0.0                ; # Factorio RCON Host
RCON_PORT = 25575                  ; # Factorio RCON Port
RCONPASS = my_password        ; # Factorio RCON Password
```


