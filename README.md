# FactorioTwitchChatIntergration

1. Generate client ID
For the bot, you may want to create a separate twitch account (alternatively you can just use your current twitch account). Note: you will need Two-Factor Authentication (2FA) enabled for this step.

Go to https://dev.twitch.tv/ and login with this twitch account. Then click Your Console->Register Your Application. Fill in the fields:

```name: FactorioChatBot```
```OAuth Redirect URLs: https://twitchapps.com/tokengen/```
```Category: Chat Bot```

2. Changing Factorio RCON settings to host the server locally
If you are hosting the game locally, instead of a dedicated server then follow these instruction. Otherwise if you already have a dedicated server, look up how to enable the RCON interface with a particular port and password.

On the main menu screen, hold Ctrl+Alt and then left click "Settings"
Now select the last item "The rest".
By local-rcon-socket, enter 0.0.0.0:25575
By local-rcon-password, enter my_password (or any secret password, the same one as in settings.txt)
Then click confirm, and go back to the main menu.
Click Multiplayer -> Host a save game
Select the game you want to host.
Click Play
