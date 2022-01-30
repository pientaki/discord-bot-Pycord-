#Copyright © 2021-2022 Sorrows[SOR] All Rights Reserved.
import os
import keep_alive
import discord
from discord.ext import commands
from dislash import slash_commands, Option, OptionType
from discord.utils import get
from discord import FFmpegPCMAudio
from youtube_dl import YoutubeDL

client = commands.Bot(command_prefix = '/')

slash = slash_commands.SlashClient(client)


test_guilds = [サーバーID] #ボットを導入するサーバーのID

@client.event  
async def on_ready():
    print('Bot online')



@slash.command(name='join',description = 'voicechannelに接続',guild_ids = test_guilds)
async def join(ctx):
  
  vc = ctx.author.voice.channel
  print('#voicechannelに接続')
  await vc.connect()
  await ctx.send('ボイスチャンネルに参加')

@slash.command(name='play',description = '音楽を再生',guild_ids = test_guilds,options=[Option('url', 'urlを入れてください', OptionType.STRING,required=True)])
async def play(ctx, url):
    YDL_OPTIONS = {'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address':'0.0.0.0'}
    FFMPEG_OPTIONS = {
        'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    voice = get(client.voice_clients, guild=ctx.guild)

    if not voice.is_playing():
        with YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(url,download=False)
        URL = info['url']
        voice.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
        voice.is_playing()
        await ctx.send('再生中')

    else:
        await ctx.send("すでに曲が流れています。別の曲を流したい場合はstopコマンドを打ち、その後urlを入力してください。")
        return


@slash.command(name='resume',description = '再生します',guild_ids = test_guilds)
async def resume(ctx):
    voice = get(client.voice_clients, guild=ctx.guild)

    if not voice.is_playing():
        voice.resume()
        await ctx.send('再生')

@slash.command(name='pause',description = '一時停止します',guild_ids = test_guilds)
async def pause(ctx):
    voice = get(client.voice_clients, guild=ctx.guild)

    if voice.is_playing():
        voice.pause()
        await ctx.send('一時停止中')

@slash.command(name='stop',description = '完全に停止します',guild_ids = test_guilds)
async def stop(ctx):
    voice = get(client.voice_clients, guild=ctx.guild)

    if voice.is_playing():
        voice.stop()
        await ctx.send('停止しています....')

@slash.command(name='disconnect',description = 'ボイスチャンネルから退出します',guild_ids = test_guilds)
async def disconnect(ctx):
    voice = get(client.voice_clients, guild=ctx.guild)
    await voice.disconnect()
    await ctx.send('ばいばい')

@slash.command(name='sourcecode',description = 'ソースコードを閲覧できます',guild_ids = test_guilds)
async def volume(ctx):
    await ctx.send('ソースコードのURL')

@slash.command(name='clear',description = '送信したメッセージを過去5件分消去します',guild_ids = test_guilds)
async def clear(ctx, amount=5):
    await ctx.channel.purge(limit=amount)
    await ctx.send("メッセージが削除されました")

@slash.command(
    guild_ids=test_guilds,
    name="user-info",
    description="ユーザー情報を表示します",
    options=[
        Option("user", "ユーザー名を入れて下さい", OptionType.USER,required=True),
    ]
)
async def user_info(inter, user=None):
    
    user = user or inter.author

    emb = discord.Embed(color=discord.Color.blurple())
    emb.title = str(user)
    emb.description = (
        f"**作成日時:** `{user.created_at}`\n"
        f"**ID:** `{user.id}`"
    )
    emb.set_thumbnail(url=user.avatar_url)
    await inter.respond(embed=emb)

@slash.command(name='update',description = 'botのアップデート情報を確認できます',guild_ids = test_guilds)
async def update(ctx):
 emb = discord.Embed(color=0xff0000)
 emb.title = 'Bot update info'
 emb.description = (
   f"**スラッシュコマンドに対応\n"
 )
 emb.set_thumbnail(url="https://kakijun.jp/shotaigifkm/tm_E697A9.gif")
 await ctx.send(embed=emb)

@slash.command(name='cmd',description = 'コマンド一覧を表示します',guild_ids = test_guilds)
async def cmd(ctx):
 emb = discord.Embed(color=0x00ff00)
 emb.title = 'コマンド一覧'
 emb.description = (
   f"**/join:**ボイスチャンネルに参加\n"
   f"**/play url:**youtubeの動画を再生\n"
   f"**/stop:**音声を停止\n"
   f"**/resume:**再生\n"
   f"**/pause:**一時停止\n"
   f"**/disconnect:**ボイスチャンネルから切断\n"
   f"**/user_info:**ユーザー情報を閲覧\n"
   f"**/update:**botのアップデート情報を確認\n"
   f"**/cmd:**コマンド一覧"
 )
 emb.set_thumbnail(url="https://images-ext-2.discordapp.net/external/q7M1UfefAPO3nhUXOj3vOARNLjNFavT-h5MPOhu5J6k/https/upload.wikimedia.org/wikipedia/en/thumb/9/9a/Trollface_non-free.png/220px-Trollface_non-free.png")
 await ctx.send(embed=emb)        
    

keep_alive.keep_alive()
client.run(os.getenv('TOKEN'))#botのトークン
