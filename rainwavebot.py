import discord
import time
import asyncio
import random
import os
import aiocron
#import logging
from discord.ext import commands
from discord.ext import tasks
from datetime import datetime
from data.config import botChannels
from private.private import token
from private.private import rwID
from private.private import rwKey
from rainwaveclient import RainwaveClient 
#Command to upgrade the rainwaveclient api: pip install -U python-rainwave-client

#logging.basicConfig(level=logging.DEBUG)

ffmpegLocation = "ffmpeg-2021-11-22/bin/ffmpeg.exe"

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

rainwaveClient = RainwaveClient()
rainwaveClient.user_id = rwID
rainwaveClient.key = rwKey

#print(rainwaveClient)

bot = commands.Bot(command_prefix='rw.', description="rainwave.cc bot, in development by Roach", intents=intents)

class current:
    voiceChannel = None
    selectedStream = None
    playing = None
    message = None

def fetchMetaData():
    return current.selectedStream.schedule_current.songs[0]

def getChannelList():
    tempArray = []
    for entries in rainwaveClient.channels:
        tempArray.append(entries.key)
    return tempArray

async def postCurrentlyListening(ctx = None, stopping=False):
#Try statement was here and still prevents is alive issue
    try: 
        current.selectedStream._sync_thread.is_alive()
        newMetaData = fetchMetaData()
        if stopping:
            tempEmbed = nowPlayingEmbed(newMetaData, stopping=True)
            await current.message.edit(embed=tempEmbed.embed)
        elif (current.playing is None
            or current.playing.id != newMetaData.id):
            tempEmbed = nowPlayingEmbed(newMetaData)
            if ctx != None:
                current.message = await ctx.send(file=tempEmbed.rainwaveLogo, embed=tempEmbed.embed)
            else:
                await current.message.edit(embed=tempEmbed.embed)
            current.playing = newMetaData
            print('')
            print(f"{current.playing} // {current.playing.id}", end ="")
        else:
            print('.', end ="")
    except:
        print("Not Syncing")

def nowPlayingEmbed(metaData, stopping=False):
    class formatedEmbed:
        syncThreadStatus = current.selectedStream._sync_thread.is_alive()
        rainwaveLogo = discord.File("data/logo.png", filename="logo.png")
        if stopping:
            intro = 'Stopped playing'
        else:
            intro = 'Now playing on'
        embed = discord.Embed(title=f"{intro} Rainwave " + metaData.album.channel.name + " Radio", url=current.selectedStream.url, description=f"Progress bar here - {metaData.length} seconds")
        if metaData.url:
            artistData = f"[{metaData.artist_string}]({metaData.url})"
        else:
            artistData = metaData.artist_string
        embed.add_field(name=f"{metaData.title} ", value=f"From - [{metaData.album.name}]({current.selectedStream.schedule_current.song.album.url})\nBy - {artistData}", inline=False)
        embed.set_thumbnail(url=metaData.album.art)
        embed.set_footer(text=f"Sync thread is alive: {syncThreadStatus}", icon_url="attachment://logo.png")
    return formatedEmbed

def validChannelCheck(ctx):
    try:
        if (botChannels.restrictVoiceChannels and ctx.message.author.voice.channel.id not in botChannels.allowedVoiceChannels):
            response = 'Music playback not allowed in this voice channel'
        elif (botChannels.restrictTextChannels and ctx.message.channel.id not in botChannels.allowedTextChannels):
            response = 'Bot commands not allowed in this text channel'
        else:
            response = True
    except:
        response = 'User does not appear to be in a voice channel'
    return response

async def stopUpdates():
    updatePlaying.stop()
    await postCurrentlyListening(stopping=True)
    current.selectedStream.stop_sync()
    current.voiceChannel.stop()
    current.message = None

async def stopConnection():
    await current.voiceChannel.disconnect()
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=" for commands"))

@tasks.loop(seconds = 5)
async def updatePlaying():
    await postCurrentlyListening()
    
@bot.event
async def on_ready():
    now = datetime.now()
    current_day = now.strftime("%d/%m/%y")
    current_time = now.strftime("%H:%M:%S")
    print('We have logged in as {0.user}'.format(bot) + ' at ' + current_time + ' on ' + current_day)
    logChannel = bot.get_channel(855136017233608744)
    await logChannel.send('I have logged on as `{0.user}` at `'.format(bot) + current_time + '` on `' + current_day + '`')
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=" for commands"))

@bot.command(aliases=['p'])
async def play(ctx, station = 'help'):
    """`rw.play <channel name>` to start radio"""
    isValidChannel = validChannelCheck(ctx)
    if isValidChannel == True:
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
                current.voiceChannel.play(discord.FFmpegPCMAudio(executable=ffmpegLocation, source=current.selectedStream.mp3_stream))
                current.selectedStream.start_sync() #print(selectedStream.client.call('sync', {'resync': 'true', 'sid': selectedStream.id}).keys())
                await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name=f"{fetchMetaData().album.channel.name} Radio"))
                await postCurrentlyListening(ctx)
                updatePlaying.start()  
        elif (station.lower() == 'help' or 'list'):
            await ctx.send(f"available channels: {channelList}")
        else:
            await ctx.send("Station not found, use `rw.help` for more info")
            print(station)
    else:
        await ctx.message.channel.send(isValidChannel)
        print(isValidChannel)
    

@bot.command(aliases=['leave','s']) ##, 'stop'
async def stop(ctx):
    """Stops radio"""
    await stopUpdates()
    await stopConnection()

@bot.command(aliases=['wo'])
async def whatson(ctx, station = None):
    """New message with playback info"""
    await ctx.send(embed=nowPlayingEmbed(fetchMetaData()))  

@bot.command()
async def test(ctx):
    nowPlayingMessage = await ctx.send("1")
    time.sleep(3)
    await nowPlayingMessage.edit(content="2")
    time.sleep(3)
    await nowPlayingMessage.edit(content="3")
    time.sleep(3)
    await nowPlayingMessage.edit(content="4")

@bot.command()
async def check(ctx):
    await ctx.send(len(ctx.message.author.voice.channel.members))

@bot.command()
async def ping(ctx):
    """Displays the bot's ping"""
    print (f'Pong! {round(bot.latency * 1000)}ms')
    await ctx.send(f'Pong! {round(bot.latency * 1000)}ms')

bot.run(token)
