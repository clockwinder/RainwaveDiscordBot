[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/clockwinder) <noscript><a href="https://liberapay.com/Clockwinder/donate"><img alt="Donate using Liberapay" src="https://liberapay.com/assets/widgets/donate.svg"></a></noscript>
# Rain.Wave Discord Bot
Rain.Wave Discord Bot is a self hostable Discord Bot which allows music from [rainwave.cc](https://rainwave.cc) streams to be played in voice channels.  It utilizes the [discord.py](https://github.com/Rapptz/discord.py) API wrapper and [Python Rainwave Client](https://github.com/williamjacksn/python-rainwave-client). The appearance of messages and functionality of the bot are configurable.

| ![example](https://github.com/user-attachments/assets/edece0ce-544e-4c69-a2f6-af736edaaae4) |
| --- |
| *Examples of Rain.Wave Discord Bot in operation with default appearance* |

Join the [Rain.Wave Discord Bot discord server](https://discord.gg/VBFuFTQfWN) to try it out!

[![Discord](https://img.shields.io/discord/1278432123455279195?logo=discord&label=Join%20the%20Rain.Wave%20Discord)](https://discord.gg/VBFuFTQfWN)

## Install
### Docker Compose Example:

> ⚠️ If you intend to run the container as a non-root user **AND** want persistent storage for your config file, you must manually create your `/path/to/local/dir` directory with read and write permissions for your intended user **before first run**.

```yaml
services:
  rainwavediscordbot:
    container_name: rainwavediscordbot
    image: ghcr.io/clockwinder/rainwavediscordbot:latest
    #user: 1000:100 #Optional, runs container as specified user
    environment:
      - DISCORD_TOKEN=F4K3T0K3N_ikb331nmGsvgHPGAv8jwFV3gKFs9eR.nF4lgje68ZdrEX9aSJ #Required, replace me
      - RAINWAVE_ID=12345 #Required, replace me
      - RAINWAVE_KEY=12345abcde #Required, replace me
      #- TZ=America/Los_Angeles #Optional, sets timezone for logging
      #- LOG_LEVEL=INFO #Optional, can be set to DEBUG, INFO, WARNING, ERROR, CRITICAL
    
    #The below two lines are optional, uncomment both to allow custom configuration files.
    #volumes:
      #- /path/to/local/dir:/rainwavediscordbot/app/user_config
```

<details>

<summary>How to get your DISCORD_TOKEN and invite your bot (click me)</summary>

1. Navigate to the Discord application page here: [https://discord.com/developers/applications](https://discord.com/developers/applications)
2. Click the "New Application" button:
3. Enter application name (this name is not the bots display name, that's adjustable in the config file), then accept the conditions and click "Create". I suggest `Rain.Wave`.
4. You'll be taken to the "General Information" tab for your application, here you can add an "APP ICON" and save. I suggest the [Rain.Wave logo](https://github.com/clockwinder/RainwaveDiscordBot/blob/main/app/data/logo.png).
5. Navigate to the "Installation" tab and set the "Install Link" dropdown to "None" and save.
6. Navigate to the "Bot" tab.
   1. Disable "Public Bot" (Rain.Wave bot is currently written as a single server bot)
   2. Under "Privileged Gateway Intents" enable: 
      * Presence Intent
      * Server Members Intent
      * Message Content Intent
   3. Save
   4. Click "Reset Token", and confirm, to get your bot token.  Copy your token and paste it in your compose as variable `DISCORD_TOKEN`.
7. Navigate to the OAuth2 tab.
   1. Under "OAuth2 URL Generator" tick the "bot" box.
   2. This opens the "Bot Permissions" options under which you'll select:
      - General Permissions
        * Change Nickname
        * View Channels
      - Text Permissions
        * Send Messages
        * Manage Messages
        * Embed Links
        * Read Message History
        * Add Reactions
      - Voice Permissions
        * Connect
        * Speak
    3. Copy the contents of "Generated URL" and navigate to it in your browser.  This should cause discord (in app or browser) to prompt you to invite the bot to a server. From the drop down choose the server in which you want the bot, and click continue, then click authorize.

</details>

<details>

<summary>How to get your RAINWAVE_ID and RAINWAVE_KEY (click me)</summary>

1. Login/create account at https://rainwave.cc/
2. Navigate to https://rainwave.cc/keys/
   * The `numeric user ID` is your docker `RAINWAVE_ID`
   * The `API Key` is your docker `RAINWAVE_KEY`

</details>

## Customization

The options found in your user_config/userconfig.yaml file can be modified to customize the functionality and appearance of the bot.  Just change the values of a given item, then restart the container to see those changes.


<details>

<summary>Here is a list of the customization options available in the userconfig.yaml file (click me)</summary>

```yaml
botChannels:
  #To restrict which voice channels the bot can use, set below to true.
  restrictVoiceChannels: False
  #If above is set to True, list allowed channel/s IDs in a list as shown below.
  allowedVoiceChannels: [123456789012345678, 987654321098765432]
  
  #To restrict which text channels the bot can receive commands on, set below to true.
  restrictTextChannels: False
  #If above is set to True, list allowed channel/s IDs in a list as shown below.
  allowedTextChannels: [112233445566778899, 998877665544332211]
  
  #If you want the bot to log items like login and error info in a channel, set below to True
  enableLogChannel: False
  #If above is set to True, list your logging channel ID below
  logChannel: 246813579024681357

options:
  #Change the name of your bot here
  botName: "Rain.Wave"

  #Change the prefix of your bot here
  botPrefix: "rw."

  #Enables display of song progress in a numerical style timer e.g. [01:05/01:21]
  enableProgressTimes: True
  
  #Enables display of song progress in a graphical manner e.g. ▰▰▰▱▱▱▱▱▱▱▱
  enableProgressBar: True
  
  #Allows selection of progress bar style between 1 and 2
  #1 is a left to right "fill" style progress bar e.g. ▰▰▰▱▱▱▱▱▱▱▱
  #2 is a moving indicator style progress bar e.g. ▱▱▱▰▱▱▱▱▱▱▱
  progressBarStyle: 1
  
  #Allows selection of progress bar character length
  progressBarLength: 14
  
  #Allows selection of characters which make up the progress bar
  #for style 1 ['▰','▱'] or ['▶','▷'] or ['█','░'] is suggested
  #for style 2 ['═','╪'] or ['—','⎔'] or ['▬',':radio_button:'] is suggested
  progressBarCharacters: ['▰','▱']

  #Allows selection of embed sidebar color as an (r, g, b) value.  
  #You can use https://it-tools.tech/color-converter to generate an rgb color value
  embedColor: [24, 135, 210]
  
  #Number of seconds between refresh of progress bar and timer, can be increased if user is being rate limited.
  #Minimum value can never be below 6.
  refreshDelay: 6
  
  #If set to `True`, bot will disconnect if no users are present in the bots voice channel.
  autoDisconnect: True

  #The below logging level is not used when running the bot via Docker.
  #Logging level, can be set to DEBUG, INFO, WARNING, ERROR, CRITICAL.  If INFO provides too much info, switch to WARNING
  logLevel: "INFO"
```
</details>
