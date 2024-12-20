# RainwaveDiscordBot
RainwaveDiscordBot is currently in testing, and should not be used!

Docker Compose Example:
```yaml
services:
  rainwavediscordbot:
    container_name: rainwavediscordbot
    image: dockerhub?
    #user: 1000:100 #Optional
    environment:
      - DISCORD_TOKEN=F4K3T0K3N_ikb331nmGsvgHPGAv8jwFV3gKFs9eR.nF4lgje68ZdrEX9aSJ
      - RAINWAVE_ID=12345
      - RAINWAVE_KEY=12345abcde
      #- TZ=America/Los_Angeles #Optional
      #- LOG_LEVEL=INFO #Optional, can be set to DEBUG, INFO, WARNING, ERROR, CRITICAL
    #volumes:
      #- "/path/to/local/dir:/rainwavediscordbot/app/user_config" #Optional, to use this line, also uncomment `#volumes:`
```

<details>

<summary>How to get your Discord Bot Token and invite your bot (click me)</summary>

[This discordpy guide](https://discordpy.readthedocs.io/en/stable/discord.html#discord-intro) covers creating a bot, getting the token for `DISCORD_TOKEN`, and inviting the bot to your discord server.

The below bot permissions should cover current bot abilities. 

![image](https://github.com/user-attachments/assets/48d5c0ac-8b60-4577-85e9-3d67eb2e737f)


</details>

<details>

<summary>How to get your Rainwave ID and Key (click me)</summary>

Login/create account at https://rainwave.cc/

Navigate to https://rainwave.cc/keys/

The `numeric user ID` is your docker `RAINWAVE_ID`

The `API Key` is your docker `RAINWAVE_KEY`

</details>
