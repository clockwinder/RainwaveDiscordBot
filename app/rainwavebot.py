#Built in libraries
import time #Built in
import asyncio #Built in
import random #Built in
import os #Built in
import traceback #Built in
import logging #Built in
from datetime import datetime, timedelta, timezone #Built in

#Libraries to install
import aiocron
import discord
from discord.ext import commands
from discord.ext import tasks
import nacl #This import is not required, but provides `requirements.txt` clarity, and use of `pipreqs`.
from rainwaveclient import RainwaveClient #NOTE Command to upgrade the rainwaveclient api: pip install -U python-rainwave-client

#Local imports
import load_config.load_config

#Global Constants
MINIMUM_REFRESH_DELAY = 6

#Load Config
config = load_config.load_config.config(os.path.dirname(os.path.abspath(__file__)))
#config = config.config #Move the dict out of a class, saves characters.
#Format for fetching config settings is `config.config["botPrefix"]`

#Set Up logger
from logger import logger

#Discord Permissions
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

#Create Bot instance w/ settings
bot = commands.Bot(command_prefix=config.config["botPrefix"], 
    description=f"rainwave.cc bot, in development by Roach\nUse `{config.config["botPrefix"]}play` to get started", intents=intents)

class current:
    voiceChannel = None
    selectedStream = None
    playing = None
    message = None

class login:
    discordBotToken = os.getenv("DISCORD_TOKEN", default=config.config["discordBotToken"])
    rainwaveID = os.getenv("RAINWAVE_ID", default=config.config["rainwaveID"])
    rainwaveKey = os.getenv("RAINWAVE_KEY", default=config.config["rainwaveKey"])

def fetchMetaData():
    return current.selectedStream.schedule_current.songs[0]

def getChannelList():
    tempArray = []
    for entries in rainwaveClient.channels:
        tempArray.append(entries.key)
    return tempArray

def checkSyncThreadIsAlive():
    try:
        if current.selectedStream._sync_thread.is_alive() == False:
            current.selectedStream.start_sync()
            logger.debug("RW Sync Restarted")
    except Exception as returnedException:
        #print(f"checkSyncThreadIsAlive error: {returnedException}") #NOTE Not required here, but I want to keep it noted as an example.
        #traceback.print_exc() #NOTE Not required here, but I want to keep it noted as an example.
        current.selectedStream.start_sync()
        logger.debug("RW Sync Started")

async def postCurrentlyListening(ctx = None, stopping=False):
    checkSyncThreadIsAlive()
    newMetaData = fetchMetaData()
    if (current.playing is None
        or current.playing.id != newMetaData.id): #This function is only for logging
        current.playing = newMetaData
        logger.info(f"{current.playing} // {current.playing.id}")
    else:
        current.playing = newMetaData
    tempEmbed = nowPlayingEmbed(newMetaData)
    if stopping: #If stopping, send final update
        tempEmbed = nowPlayingEmbed(newMetaData, stopping=True)
        await current.message.edit(embed=tempEmbed.embed)
    elif ctx != None: #If passed context (done when a new message is wanted), create new message
        current.message = await ctx.send(file=tempEmbed.rainwaveLogo, embed=tempEmbed.embed)
    else: #Otherwise, edit old message
        await current.message.edit(embed=tempEmbed.embed)
        logger.debug(f'Currently Listening updated {current.playing.id}')

def formatSecondsToMinutes(incomingSeconds):
    minutes = str(incomingSeconds // 60) #get minutes, .zfill requires a string
    seconds = str(incomingSeconds % 60) #get seconds
    return(f"{minutes.zfill(2)}:{seconds.zfill(2)}")

def setTimes():
    class times:
        currentAdjustedTime = datetime.now(timezone.utc) #This time is in UTC
        startTime = current.selectedStream.schedule_current.start_actual #This time is in UTC
        #endTime = current.selectedStream.schedule_current.end #This time is in UTC
        timeSinceStart = currentAdjustedTime - startTime
        #timeUntilEnd = endTime - currentAdjustedTime #Not currently needed
    return(times)

def generateProgressBar(metaData, stopping=False):
    times = setTimes()
    #The below checks for rainwave issues. If their system fails, the current track "plays" forever.
    if times.timeSinceStart.seconds > metaData.length: #Check int to int value
        timeSinceStartInSeconds = metaData.length #If time is too long, set max.
    else: #Else just do a seconds conversion.
        timeSinceStartInSeconds = times.timeSinceStart.seconds 
    if ((config.config["enableProgressBar"] == False
        and config.config["enableProgressTimes"] == False)
        or stopping == True):
        return(None)
    if config.config["enableProgressTimes"] == False:
        timer = ''
    else:
        timer = f"`[{formatSecondsToMinutes(timeSinceStartInSeconds)}/{formatSecondsToMinutes(metaData.length)}]`"
    progress = int(config.config["progressBarLength"] * (timeSinceStartInSeconds/metaData.length))
    if config.config["enableProgressBar"] == False:
        progressBar = ''
    elif config.config["progressBarStyle"] == 1: #Left to right "fill"
        progressBar = f"{config.config["progressBarCharacters"][0] * progress}{config.config["progressBarCharacters"][1] * (config.config["progressBarLength"] - progress)}"
    elif config.config["progressBarStyle"] == 2: #Left to right indicator
        progressBar = f"{config.config["progressBarCharacters"][0] * (progress - 1)}{config.config["progressBarCharacters"][1]}{config.config["progressBarCharacters"][0] * (config.config["progressBarLength"] - progress)}"
    #TODO See if we can prevent the flickering from the formatting of Style3
    #elif config.config["progressBarStyle"] == 3: #Left to right color fill
    #    progressBar = f"```ansi\n[2;34m{options.progressBarChars[0] * progress}[0m[2;37m{options.progressBarChars[0] * (config.config["progressBarLength"] - progress)}[0m{timer}\n```"
    if config.config["enableProgressBar"] == True and config.config["enableProgressTimes"] == True:
        spacer = ' '
    else:
        spacer = ''
    completeProgressBar = f"{progressBar}{spacer}{timer}"
    return(completeProgressBar)

def nowPlayingEmbed(metaData, stopping=False):
    class formatedEmbed:
        syncThreadStatus = current.selectedStream._sync_thread.is_alive()
        rainwaveLogo = discord.File("app/data/logo.png", filename="logo.png")
        if stopping:
            intro = 'Stopped playing'
        else:
            intro = 'Now playing on'
        embed = discord.Embed(title=f"{intro} Rainwave {metaData.album.channel.name} Radio", 
            url=current.selectedStream.url, 
            description=generateProgressBar(metaData, stopping), 
            color = discord.Colour.from_rgb(config.config["embedColor"][0],config.config["embedColor"][1],config.config["embedColor"][2]))
        if metaData.url:
            artistData = f"[{metaData.artist_string}]({metaData.url})"
        else:
            artistData = metaData.artist_string
        embed.add_field(name=f"{metaData.title} ", 
            value=f"From - [{metaData.album.name}]({current.selectedStream.schedule_current.song.album.url})\nBy - {artistData}", inline=False)
        embed.set_thumbnail(url=metaData.album.art)
        embed.set_footer(text=f"Sync thread is alive: {syncThreadStatus}", icon_url="attachment://logo.png")
    return formatedEmbed

async def validChannelCheck(ctx, checkVoiceChannel = False):
    response = True #Assume nothing is wrong
    if (config.config["restrictTextChannels"] #If disallowed channel
        and (ctx.message.channel.id not in config.config["allowedTextChannels"])):
        response = f"{bot.user.name} commands not allowed in {ctx.message.channel.name}"
    elif checkVoiceChannel == True: 
        try:
            authorsChannel = ctx.message.author.voice.channel.id #Creating this variable checks that they're in a channel at all.
            if (config.config["restrictVoiceChannels"] #If disallowed voice channel
                and (authorsChannel not in config.config["allowedVoiceChannels"])):
                response = f"{bot.user.name} music playback not allowed in {ctx.message.author.voice.channel.name}"
        except: #If user not in a visible voice channel
            response = 'You do not appear to be in a voice channel'
    if response != True: #Log error and turn response into a bool for return
        logger.debug(f"Valid Channel Check: {response}")
        await ctx.message.channel.send(f"{ctx.message.author.mention} {response}")
        response = False
    return response

async def stopUpdates(gracefully = False):
    if gracefully: #If called from the loop which it is ending, the loop must be ended gracefully instead of canceled.
        updatePlaying.stop()
    else:
        updatePlaying.cancel()
    await postCurrentlyListening(stopping=True)
    current.selectedStream.stop_sync()
    current.voiceChannel.stop()
    current.message = None

async def stopConnection():
    await current.voiceChannel.disconnect()
    await setDefaultActivity()

async def setDefaultActivity():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f" for `{config.config["botPrefix"]}play`"))

def loadOpus():
    opusStatus = "Failed"
    if discord.opus.is_loaded() == False:
        try:
            discord.opus.load_opus(config.config["opusLocation"])
            opusStatus = "Initialized"
        except Exception as returnedException:
            logger.warn(f"Opus loading error error: {returnedException}")
    else:
        opusStatus = "Pre-Loaded"
    return(opusStatus)

def checkUserPresence():
    userPresent = False
    for members in current.voiceChannel.channel.members:
        if members.id != bot.user.id:
            userPresent = True
            break
    return(userPresent)

@tasks.loop(seconds = config.config["refreshDelay"]) #TODO Determine if 6 is actually safe, and if we can go lower
async def updatePlaying():
    usersPresent = checkUserPresence()
    if ((usersPresent == False)
         and (config.config["autoDisconnect"] == True)):
        logger.info("All alone, disconnecting")
        await stopUpdates(gracefully = True)
        await stopConnection()
    else:
        await postCurrentlyListening()
    
@bot.event
async def on_ready():
    now = datetime.now()
    current_day = now.strftime("%d/%m/%y")
    current_time = now.strftime("%H:%M:%S")
    opusStatus = loadOpus()
    await bot.user.edit(username=config.config["botName"])
    loginReport = f'Logged into Discord as `{bot.user} (ID: {bot.user.id})` and Rainwave as `(ID: {rainwaveClient.user_id})` at `{current_time}` on `{current_day}`'
    logger.info(loginReport)
    logger.debug(f"Opus: {opusStatus}")
    if config.config["enableLogChannel"]:
        await bot.get_channel(config.config["logChannel"]).send(loginReport)
    await setDefaultActivity()

@bot.command(aliases=['p'])
async def play(ctx, station = 'help'):
    """Starts radio playback"""
    if await validChannelCheck(ctx, checkVoiceChannel = True):
        channelList = getChannelList()
        if station.lower() in channelList:
            stationNumber = channelList.index(station.lower())
            userChannel = ctx.message.author.voice.channel
            newSelectedStream = rainwaveClient.channels[stationNumber]
            try:
                current.voiceChannel = await userChannel.connect() #connect to channel
            except:
                if current.selectedStream != newSelectedStream: #If already connected and new stream is selected, restart stream
                    await stopUpdates()
            current.selectedStream = newSelectedStream
            if current.voiceChannel.is_playing():
                await ctx.send(f"Already playing {fetchMetaData().album.channel.name} Radio")
            else:
                probedAudioStream = await discord.FFmpegOpusAudio.from_probe(current.selectedStream.ogg_stream)
                current.voiceChannel.play(probedAudioStream)
                await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name=f"{fetchMetaData().album.channel.name} Radio"))
                await postCurrentlyListening(ctx)
                updatePlaying.start()  
        elif (station.lower() == ('help' or 'list')):
            await ctx.send(f"To start playback use `{config.config["botPrefix"]}play` followed by one of the available channels: {channelList}"
                            f"\nExample: `{config.config["botPrefix"]}play {channelList[0]}`")
        else:
            await ctx.send(f"Station not found, use `{config.config["botPrefix"]}play help` for more info")

@bot.command(aliases=['leave','s']) ##, 'stop'
async def stop(ctx):
    """Stops radio playback"""
    try:
        if current.voiceChannel.is_playing():
            if (await validChannelCheck(ctx)):
                await stopUpdates()
                await stopConnection()
    except:
        logger.info("invalid stop command")

@bot.command(aliases=['np','whatson','wo','queue','q'])
async def nowplaying(ctx, station = None):
    """New message with playback info"""
    try:
        if current.voiceChannel.is_playing():
            if (await validChannelCheck(ctx)):
                await postCurrentlyListening(stopping=True)
                await postCurrentlyListening(ctx)
    except:
        logger.info("invalid nowplaying command")

#@bot.command()
#async def test(ctx): #Used for testing
#    logger.info('test')

@bot.command()
async def ping(ctx):
    """Displays the bot's ping"""
    logger.info(f'Pong! {round(bot.latency * 1000)}ms')
    await ctx.send(f'Pong! {round(bot.latency * 1000)}ms')

#Set up rainwave client
rainwaveClient = RainwaveClient()
rainwaveClient.user_id = login.rainwaveID
rainwaveClient.key = login.rainwaveKey

if config.config["refreshDelay"] < MINIMUM_REFRESH_DELAY:
    config.config["refreshDelay"] = MINIMUM_REFRESH_DELAY
    logger.warning(f"WARN refreshDelay overridden to: {MINIMUM_REFRESH_DELAY}")
bot.run(login.discordBotToken) #Start Bot
