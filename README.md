# Rain.Wave Discord Bot
RainwaveDiscordBot is currently in testing, and should not be used!

Rain.Wave Discord Bot is a self hostable Discord Bot which allows live music from [rainwave.cc](https://rainwave.cc) to be played in voice channels.  It utilizes the [discord.py](https://github.com/Rapptz/discord.py) API wrapper and [Python Rainwave Client](https://github.com/williamjacksn/python-rainwave-client).

Join the [Rain.Wave Discord Bot]() discord server to try it out!

## Install

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

## Customization

The options found in your user_config/userconfig.yaml file can be modified to customize the functionality of the bot.  Just change the values of a given item to customize how the bot looks and behaves, then restart the container to see those changes.

The file will look like this:

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
