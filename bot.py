from discord.ext.commands import Context
from discord import FFmpegPCMAudio, VoiceChannel
from discord.ext import commands
from youtube_dl import YoutubeDL
import asyncio

bot = commands.Bot(command_prefix='$')
playlist = list()

def get_data2(url):
    song_info : dict
    ydl_options = {}

    with YoutubeDL(ydl_options) as ydl:
        song_info = ydl.extract_info(url, download=False)

    return song_info 

@bot.command()
async def test(ctx: Context):
    await ctx.send(ctx.message.content)

@bot.command()
async def helps(ctx: Context):
    resp = '''
    test - echo command
    play url - play right now
    pause - pause
    add url - add to queue
    delete num - delte track from queue
    playq - play queue
    '''
    await ctx.send(resp)

@bot.command()
async def play(ctx: Context,arg):
    url = get_data2(arg)['formats'][0]['url']
    channel : VoiceChannel
    vc = ctx.voice_client
    channel = ctx.author.voice.channel
    if vc:
        if vc.is_playing():
            vc.stop()
        await vc.move_to(channel)
    else:
        vc = await channel.connect()
    data = FFmpegPCMAudio(url)
    if not data:
        await asyncio.sleep(2)
    vc.play(data)
    

@bot.command()
async def pause(ctx: Context):
    vc = ctx.voice_client
    if vc:
        if vc.is_playing():
            vc.pause()

@bot.command()
async def resume(ctx: Context):
    vc = ctx.voice_client
    if vc:
        if vc.is_paused():
            vc.resume()

@bot.command()
async def playq(ctx):
    channel : VoiceChannel
    vc = ctx.voice_client
    channel = ctx.author.voice.channel
    if vc:
        if vc.is_playing():
            vc.stop()
        await vc.move_to(channel)
    else:
        vc = await channel.connect()
    if playlist:
        while len(playlist)>0:
            print(1)
            track = playlist.pop(0)
            data = FFmpegPCMAudio(track[1])
            await vc.play(data)
            await asyncio.sleep(track[2])           
                   
@bot.command()
async def add(ctx: Context, *, arg):
    print(arg)
    a = arg.split()
    print(a)
    for elem in a:
        el = get_data2(elem)
        playlist.append((el['title'],el['formats'][0]['url'],el['duration']))

@bot.command()
async def showq(ctx: Context):
    resp = ''
    for i in range(len(playlist)):
        resp= resp+str(i+1)+' '+playlist[i][0]+'\n'
    if not resp:
        resp = 'Empty'
    await ctx.send(resp)

@bot.command()
async def delete(ctx:Context, arg):
    playlist.pop(int(arg)-1)
    await ctx.send('Deleted')

@bot.command()
async def stop(ctx:Context, arg):
    vc = ctx.voice_client
    if vc.is_playing():
        vc.stop()

@bot.command()
async def disconnect(ctx:Context):
    vc = ctx.voice_client
    if vc.is_connected():
        await vc.disconnect() 

bot.run('ODk5MzY5ODE0NDQ1OTE2MjAw.YWxxaQ.ywwfEvg1NF03qEyihhvUsWZWAaA')