import discord
import os
import requests
from discord.ext import tasks
from urllib.parse import urlparse
from random import choice
import logging
import re
# from time import time
from keep_alive import keep_alive

client = discord.Client()
channel_name = 'all-links-and-media'
# delay = lambda t1, t2: f'Execution time = {t2 - t1}'


@client.event
async def on_message(message):
    msg = message.content
    # t1 = time()
    if "$ping" in msg.lower():
        await message.channel.send(
            f'**Pong!** Latency: {round(client.latency * 1000)}ms')
        # t2 = time()
        # print(f'ping pong - {delay(t1, t2)}')

    if (not isinstance(message.channel, discord.TextChannel)):
        return

    if message.author == client.user or message.channel.name == channel_name:
        return

    # t1 = time()
    channel = guild_channels[message.guild].get(channel_name)
    # t2 = time()
    # print(f'\n\n----------------------\nchannel fetch - {delay(t1, t2)}')

    if channel == None:
        return

    attachments = message.attachments
    # embeds = message.embeds
    # print(f'Embeds : {len(embeds)}')
    # print(f'Attachments : {len(attachments)}')

    # t1 = time()
    url_regex = 'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
    if re.search(url_regex, msg):
        await channel.send(msg)
        # t2 = time()
        # print(f'send embed - {delay(t1, t2)}')

    # t1 = time()
    if len(attachments) > 0:
        for i in attachments:
            a = urlparse(str(i))
            filename = os.path.basename(a.path)
            r = requests.get(i)
            with open(filename, 'wb') as f:
                f.write(r.content)
            f.close()
            await channel.send(file=discord.File(filename))
            # t2 = time()
            # print(f'send file - {delay(t1, t2)}')
            os.remove(filename)


status = [
    'music!', 'party till sundown!🥳', 'lazy-ass!', 'rabbit-holes!',
    'snoopy-boopy!', 'with cats - Meowww!'
]


@tasks.loop(seconds=10)
async def change_status():
    await client.change_presence(activity=discord.Game(name=choice(status)))


@client.event
async def on_ready():
    change_status.start()
    # autopingpong.start()
    logging.info('BOT RESTARTED')

    global guild_channels

    channels = [
        dict(zip((channel.name for channel in guild.channels), guild.channels))
        for guild in client.guilds
    ]
    guild_channels = dict(zip(client.guilds, channels))
    logging.info('GUILDS AND CHANNELS DICTIONARY GENERATED.')


@client.event
async def on_guild_join(guild):
    guild_channels[guild] = dict(
        zip((channel.name for channel in guild.channels), guild.channels))
    logging.info(f'NEW GUILD {guild.name} JOINED.')
    logging.info('GUILDS AND CHANNELS DICTIONARY UPDATED.')

    channel = guild.channels[2]
    bot_ch = guild_channels[guild].get(channel_name)
    await channel.send(
        f"Hi, I'm a bot! I forward all links and media shared in this server to a dedicated channel {bot_ch.mention if bot_ch else '**all-links-and-media**'}! Please make sure that this server has a channel called {bot_ch.mention if bot_ch else '**all-links-and-media**'}."
    )


@client.event
async def on_guild_remove(guild):
    guild_channels.pop(guild)
    logging.info(f'GUILD {guild.name} LEFT.')
    logging.info('GUILDS AND CHANNELS DICTIONARY UPDATED.')


@client.event
async def on_guild_update(before, guild):
    guild_channels.pop(before)
    guild_channels[guild] = dict(
        zip((channel.name for channel in guild.channels), guild.channels))
    logging.info(f'GUILD {before.name} WAS MODIFIED.')
    logging.info('GUILDS AND CHANNELS DICTIONARY UPDATED.')


@client.event
async def on_guild_channel_create(channel):
    guild = channel.guild
    guild_channels[guild] = dict(
        zip((channel.name for channel in guild.channels), guild.channels))
    logging.info(f'NEW CHANNEL ADDED IN {guild.name}.')
    logging.info('GUILDS AND CHANNELS DICTIONARY UPDATED.')


@client.event
async def on_guild_channel_delete(channel):
    guild = channel.guild
    guild_channels[guild] = dict(
        zip((channel.name for channel in guild.channels), guild.channels))
    logging.info(f'CHANNEL {channel.name} REMOVED FROM {guild.name}.')
    logging.info('GUILDS AND CHANNELS DICTIONARY UPDATED.')


@client.event
async def on_guild_channel_update(before, channel):
    guild = channel.guild
    guild_channels[guild] = dict(
        zip((channel.name for channel in guild.channels), guild.channels))
    logging.info(f'CHANNEL {before.name} UPDATED IN {guild.name}')
    logging.info('GUILDS AND CHANNELS DICTIONARY UPDATED.')


# @tasks.loop(minutes=5)
# async def autopingpong():
#     id = 937157186851848192
#     channel = client.get_channel(id)
#     await channel.send('$ping')

keep_alive()
client.run(os.getenv('TOKEN'))
