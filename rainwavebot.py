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
from private.private import token
from private.private import rwID
from private.private import rwKey
from rainwaveclient import RainwaveClient 
#Command to upgrade the rainwaveclient api: pip install -U python-rainwave-client

#logging.basicConfig(level=logging.DEBUG)

ffmpegLocation = "ffmpeg-2021-11-22/bin/ffmpeg.exe"
dataLocation = "data/"

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

async def postCurrentlyListening():
    try:
        if current.selectedStream._sync_thread.is_alive():
            newMetaData = fetchMetaData()
            if (current.playing is None
                or current.playing.id != newMetaData.id):
                await bot.get_channel(882671679938109530).send(embed=nowPlayingEmbed(newMetaData))
                current.playing = newMetaData
                print('')
                print(f"{current.playing} // {current.playing.id}", end ="")
            else:
                print('.', end ="")
    except:
        print("waiting on thread start")
            
def nowPlayingEmbed(metaData):
    syncThreadStatus = current.selectedStream._sync_thread.is_alive()
    embed = discord.Embed(title="Now playing on Rainwave " + metaData.album.channel.name + " Radio", url=current.selectedStream.url, description=f"Progress bar here - {metaData.length} seconds")
    if metaData.url:
        artistData = f"[{metaData.artist_string}]({metaData.url})"
    else:
        artistData = metaData.artist_string
    
    embed.add_field(name=f"{metaData.title} ", value=f"From - [{metaData.album.name}]({current.selectedStream.schedule_current.song.album.url})\nBy - {artistData}", inline=False)
    embed.set_thumbnail(url=metaData.album.art)
    embed.set_footer(text=f"Sync thread is alive: {syncThreadStatus}", icon_url="https://cookiemountain.org/pictures/rainwavelogoorangecropped.png")
    return embed

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
    channelList = getChannelList()   
    if station.lower() in channelList:
        stationNumber = channelList.index(station.lower())
        userChannel = ctx.message.author.voice.channel
        newSelectedStream = rainwaveClient.channels[stationNumber]
        try:
            current.voiceChannel = await userChannel.connect()
        except:
            if current.selectedStream != newSelectedStream:
                current.voiceChannel.stop()
                current.selectedStream.stop_sync()
        current.selectedStream = newSelectedStream
        if current.voiceChannel.is_playing():
            await ctx.send(f"Already playing {fetchMetaData().album.channel.name} Radio")
        else:
            current.voiceChannel.play(discord.FFmpegPCMAudio(executable=ffmpegLocation, source=current.selectedStream.mp3_stream)) #If you need to define executable location, add executable=ffmpegLocation,
            current.selectedStream.start_sync() #print(selectedStream.client.call('sync', {'resync': 'true', 'sid': selectedStream.id}).keys())
            await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name=f"{fetchMetaData().album.channel.name} Radio"))
            updatePlaying.start()
        
    elif (station.lower() == 'help' or 'list'):
        await ctx.send(f"available channels: {channelList}")
    else:
        await ctx.send("Station not found, use `rw.help` for more info")
        print(station)

@bot.command(aliases=['leave','s']) ##, 'stop'
async def stop(ctx):
    """Stops radio"""
    updatePlaying.stop()
    current.selectedStream.stop_sync()
    current.voiceChannel.stop()
    await current.voiceChannel.disconnect()
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=" for commands"))

@bot.command(aliases=['wo'])
async def whatson(ctx, station = None):
    """New message with playback info"""
    await ctx.send(embed=nowPlayingEmbed(fetchMetaData()))  

@bot.command()
async def test(ctx):
    print(fetchMetaData())

@bot.command()
async def check(ctx):
    await ctx.send(len(ctx.message.author.voice.channel.members))

@bot.command()
async def ping(ctx):
    """Displays the bot's ping"""
    print (f'Pong! {round(bot.latency * 1000)}ms')
    await ctx.send(f'Pong! {round(bot.latency * 1000)}ms')

bot.run(token)
