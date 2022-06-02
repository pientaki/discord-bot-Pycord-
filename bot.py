#Copyright © 2021-2022 Sorrows[SOR] All Rights Reserved.
import discord
from discord.ext import commands, tasks
from discord.commands import Option
from discord.ui import Button, View, Select
import aiohttp
import math
import aiosqlite
from itertools import cycle
import asyncio
from sympy import true
import wavelink
import numpy
import traceback
from wavelink.ext import spotify
from search import Google
from covidtest import Covid
from funny import Neta
from server import Server
from game import Game
from covi2 import Covid2
from weather import Weather

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix="*", intents=intents)
bot.multiplier = 1
test_ids=[902562000855502909]
status=cycle(["/cmdでコマンド一覧","早漏で候","メンバーを監視中"])

bot.add_cog(Server(bot))
bot.add_cog(Google(bot))
bot.add_cog(Covid(bot))
bot.add_cog(Neta(bot))
bot.add_cog(Game(bot))
bot.add_cog(Covid2(bot))
bot.add_cog(Weather(bot))

async def initialize():
    await bot.wait_until_ready()
    bot.db = await aiosqlite.connect("expData.db")
    await bot.db.execute("CREATE TABLE IF NOT EXISTS guildData (guild_id int, user_id int, exp int, PRIMARY KEY (guild_id, user_id))")

@bot.event
async def on_ready():
    print("Bot is ready!")
    change_status.start()
    bot.loop.create_task(create_nodes())
    
    
async def create_nodes():
    await bot.wait_until_ready()
    await wavelink.NodePool.create_node(bot=bot, host="lavalink.oops.wtf", port="443", password="www.freelavalink.ga",https=True, spotify_client=spotify.SpotifyClient(client_id="d52f6a05b7ac4ea1b953eadbd2b6ba45", client_secret="e43ff5d74bcd4eb28e55e5976b7b282e"))
    

@tasks.loop(seconds=10)
async def change_status():
    await bot.change_presence(status=discord.Status.online,activity=discord.Game(next(status)))


@bot.slash_command(name="cmd", description="コマンド一覧を表示", guild_ids=test_ids)
async def help_select(ctx: discord.ApplicationContext):
    helpembed = discord.Embed(title="Sorrows Official Bot",color=discord.Color.blurple())
    helpembed.set_thumbnail(url=bot.user.avatar.url)
    helpembed.add_field(name="導入サーバー数", value=len(bot.guilds))
    helpembed.add_field(name="メンバー数", value=len(bot.users))
    helpembed.add_field(name="Ping", value=f"{bot.latency*1000:.2f}ms")
    select = Select(options=[discord.SelectOption(label="音楽コマンド", description="音楽聞く時のコマンド一覧", emoji="🎧"), discord.SelectOption(label="サーバーコマンド", description="サーバーコマンド一覧", emoji="💻"),
    discord.SelectOption(label="便利コマンド", description="そんな便利でもないコマンド一覧", emoji="🔎"), discord.SelectOption(label="ゲームコマンド", description="ゲームコマンド一覧", emoji="🎮"), discord.SelectOption(label="その他コマンド", description="しょーもないコマンド一覧", emoji="💩")])
    
    musicembed = discord.Embed(title="**:headphones: 音楽コマンド**",color=discord.Color.blurple())
    musicembed.description=(f"**/join : **ボイスチャンネルに参加\n"
   f"**/play ＜タイトル＞ : **音楽をYouTube経由で検索して再生\n"
   f"**/socplay ＜タイトル＞ : **音楽をSoundCloud経由で検索して再生\n"
   f"**/stop : **音声を停止\n"
   f"**/resume : **再生\n"
   f"**/pause : **一時停止\n"
   f"**/volume ＜音量＞ : **音量を変更\n"
   f"**/disconnect : **ボイスチャンネルから切断\n")

    convembed = discord.Embed(title="**:mag_right:  便利コマンド**",color=discord.Color.blurple())
    convembed.description=(f"**/trans ＜翻訳したい言語＞ ＜内容＞ : **翻訳機能\n"
   f"**/language : **翻訳言語一覧\n"
   f"**/googlesearch ＜検索ワード＞ : **googleで検索(上位5件分)\n"
   f"**/vote ＜テーマ＞ ＜選択肢１＞ ＜選択肢２＞ : **投票を作成\n"
   f"**/covid : **大阪府の新型コロナウイルス新規感染者数を検索\n")

    serverembed = discord.Embed(title="**:computer: サーバーコマンド**",color=discord.Color.blurple())
    serverembed.description=(f"**/kick ＜メンバー＞ : **メンバーをキック\n"
   f"**/ban ＜メンバー＞ : **メンバーをban\n"
   f"**/clear ＜消去数＞ : **メッセージを削除\n"
   f"**/mute ＜メンバー＞ : **メンバーをミュート\n"
   f"**/unmute ＜メンバー＞ : **ミュート解除\n"
   f"**/user-info ＜メンバー＞ : **メンバー情報\n"
   f"**/timeout ＜メンバー＞ : **メンバーをタイムアウト\n"
   f"**/removetimeout ＜メンバー＞ : **タイムアウト解除\n"
   f"**/activity ＜アクティビティー＞ : **botの～をプレイ中の部分を変更\n"
   f"**/lederboard : **リーダーボードを表示\n"
   f"**/stats ＜メンバー＞ : **ステータスを表示\n")

    gameembed = discord.Embed(title="**:video_game: ゲームコマンド**",color=discord.Color.blurple())
    gameembed.description=(f"**/akinator : **アキネイターをプレイ\n"
   f"**/minesweeper : **マインスイーパーをプレイ\n")

    funembed = discord.Embed(title="**💩 funコマンド**",color=discord.Color.blurple())
    funembed.description=("**/meme : **ミームを投稿\n"
   "**/hack : **謎\n"
   "**/kodane : **褒美だ.......\n")
   
    async def my_callback(interaction):
        if select.values[0] == "音楽コマンド":
            await interaction.response.edit_message(embed=musicembed)
        elif select.values[0] == "サーバーコマンド":
            await interaction.response.edit_message(embed=serverembed)
        elif select.values[0] == "便利コマンド":
            await interaction.response.edit_message(embed=convembed)
        elif select.values[0] == "ゲームコマンド":
            await interaction.response.edit_message(embed=gameembed)
        elif select.values[0] == "その他コマンド":
            await interaction.response.edit_message(embed=funembed)
    
    select.callback = my_callback
    view = View()
    view.add_item(select)
    await ctx.respond(embed=helpembed, view=view)


class PlayButton(Button):
    def __init__(self, label):
        super().__init__(label=label, style=discord.ButtonStyle.green)

    async def callback(self, interaction):
        node = wavelink.NodePool.get_node()
        player = node.get_player(interaction.guild)

        if player is None:
            return await interaction.response.send_message("botがボイスチャンネルに接続していません", ephemeral=True)
            
        if player.is_paused():
            await player.resume()
            mbed = discord.Embed(title="再生中", color=discord.Color.from_rgb(255, 255, 255))
            return await interaction.response.send_message(embed=mbed, ephemeral=True)
        else:
            return await interaction.response.send_message("音楽は一時停止されていません", ephemeral=True)
        
class PauseButton(Button):
    def __init__(self, label):
        super().__init__(label=label, style=discord.ButtonStyle.blurple)

    async def callback(self, interaction):
        node = wavelink.NodePool.get_node()
        player = node.get_player(interaction.guild)

        if player is None:
            return await interaction.response.send_message("botがボイスチャンネルに接続していません", ephemeral=True)
        
        if not player.is_paused():
            if player.is_playing():
                await player.pause()
                mbed = discord.Embed(title="一時停止中", color=discord.Color.from_rgb(255, 255, 255))
                return await interaction.response.send_message(embed=mbed, ephemeral=True)
            else:
                return await interaction.response.send_message("現在音楽は流れていません", ephemeral=True)
        else:
            return await interaction.response.send_message("既に一時停止中です", ephemeral=True)

class StopButton(Button):
    def __init__(self, label):
        super().__init__(label=label, style=discord.ButtonStyle.blurple)

    async def callback(self, interaction):
        node = wavelink.NodePool.get_node()
        player = node.get_player(interaction.guild)

        if player is None:
            return await interaction.response.send_message("botがボイスチャンネルに接続していません", ephemeral=True)
        
        if player.is_playing:
            player.queue.clear()
            await player.stop()
            mbed = discord.Embed(title="停止", color=discord.Color.from_rgb(255, 255, 255))
            return await interaction.response.send_message(embed=mbed, ephemeral=True)
        else:
            return await interaction.response.send_message("現在音楽は流れていません", ephemeral=True)

class SkipButton(Button):
    def __init__(self, label):
        super().__init__(label=label, style=discord.ButtonStyle.blurple)

    async def callback(self, interaction):
        node = wavelink.NodePool.get_node()
        player = node.get_player(interaction.guild)

        if player is None:
            return await interaction.response.send_message("botがボイスチャンネルに接続していません", ephemeral=True)
        
        if player.is_playing and not player.queue.is_empty:
            await player.stop()
            mbed = discord.Embed(title="スキップ", color=discord.Color.from_rgb(255, 255, 255))
            return await interaction.response.send_message(embed=mbed, ephemeral=True)
        elif player.queue.is_empty:
            return await interaction.response.send_message("キューに曲はありません")
        else:
            return await interaction.response.send_message("現在音楽は流れていません", ephemeral=True)

class DisconButton(Button):
    def __init__(self, label):
        super().__init__(label=label, style=discord.ButtonStyle.red)

    async def callback(self, interaction):
        node = wavelink.NodePool.get_node()
        player = node.get_player(interaction.guild)

        if player is None:
            return await interaction.response.send_message("botがボイスチャンネルに接続していません", ephemeral=True)
    
        await player.disconnect()
        mbed = discord.Embed(title="ボイスチャンネルから退出", color=discord.Color.from_rgb(255, 255, 255))
        await interaction.response.send_message(embed=mbed)

@bot.event
async def on_wavelink_node_ready(node: wavelink.Node):
    print(f"Node <{node.identifier}> is now Ready!")


        
@bot.slash_command(name="play", description="YouTubeの音楽を再生", guild_ids=test_ids)
async def play(ctx: discord.ApplicationContext, *, search: Option(str, '曲名を入力')):
    search = await wavelink.YouTubeTrack.search(query=search, return_first=True)
    button = PlayButton("再生")
    button2 = PauseButton("一時停止")
    button3 = StopButton("停止")
    button4 = SkipButton("スキップ")
    button5 = DisconButton("退出")

    if not ctx.voice_client:
        vc: wavelink.Player = await ctx.author.voice.channel.connect(cls=wavelink.Player)
        embed=discord.Embed(title=f"ボイスチャンネル {ctx.author.voice.channel.name} に接続", color=discord.Color.from_rgb(255, 255, 255))
        await ctx.respond(embed=embed)
    else:
        vc: wavelink.Player = ctx.voice_client
        vc.chanctx = ctx.channel

    if vc.queue.is_empty and not vc.is_playing():

        await vc.play(search)

        mbed = discord.Embed(title="再生中", color=discord.Color.from_rgb(255, 255, 255))
        mbed.add_field(name="タイトル", value=search.title)
        mbed.add_field(name="再生時間", value=round(search.duration / 60, 2))
        mbed.add_field(name="ボリューム", value=vc.volume) 
        mbed.set_image(url=search.thumb)

        view = View()
        view.add_item(button)
        view.add_item(button2)
        view.add_item(button3)
        view.add_item(button4)
        view.add_item(button5)
        await ctx.respond(embed=mbed, view=view)
    else:
        await vc.queue.put_wait(search)
        await ctx.respond(f'`{search}` をキューに追加しました')

@bot.event
async def on_wavelink_track_end(player: wavelink.Player, track , reason):
    button = PlayButton("再生")
    button2 = PauseButton("一時停止")
    button3 = StopButton("停止")
    button4 = SkipButton("スキップ")
    button5 = DisconButton("退出")

    if not player.queue.is_empty:
            ctx = player.chanctx
            new_song = player.queue.get()
            
            await player.play(new_song)
            view = View() 
            view.add_item(button)
            view.add_item(button2)
            view.add_item(button3)
            view.add_item(button4)
            view.add_item(button5)

            embed = discord.Embed(title="再生中", color=discord.Color.from_rgb(255, 255, 255))
            embed.add_field(name="タイトル", value=new_song.title)
            embed.add_field(name="再生時間", value=round(new_song.duration / 60, 2))
            embed.add_field(name="ボリューム", value=player.volume) 
            embed.set_image(url=new_song.thumb) 
            await ctx.send(embed=embed, view=view)

    

#@bot.slash_command(name="join", description="コマンド一覧を表示", guild_ids=test_ids)
#async def join_command(ctx: discord.ApplicationContext, channel: Option(discord.VoiceChannel, 'ボイスチャンネルを選択')):
    #if channel is None:
        #channel = ctx.author.voice.channel
        
    #node = wavelink.NodePool.get_node()
    #player = node.get_player(ctx.guild)

    #if player is not None:
        #if player.is_connected():
            #return await ctx.respond("botが既にボイスチャンネルに接続しています")
        
    #await channel.connect(cls=wavelink.Player)
    #mbed=discord.Embed(title=f"ボイスチャンネル {channel.name} に接続", color=discord.Color.from_rgb(255, 255, 255))
    #await ctx.respond(embed=mbed)

@bot.slash_command(name="disconnect", description="ボイスチャンネルから退出", guild_ids=test_ids)
async def leave_command(ctx: discord.ApplicationContext):
    node = wavelink.NodePool.get_node()
    player = node.get_player(ctx.guild)

    if player is None:
        return await ctx.send("botがボイスチャンネルに接続していません")
    
    await player.disconnect()
    mbed = discord.Embed(title="ボイスチャンネルから退出", color=discord.Color.from_rgb(255, 255, 255))
    await ctx.respond(embed=mbed)

@bot.slash_command(name="stop", description="停止", guild_ids=test_ids)
async def stop_command(ctx: discord.ApplicationContext):
    node = wavelink.NodePool.get_node()
    player = node.get_player(ctx.guild)
      
    if player is None:
        return await ctx.respond("botがボイスチャンネルに接続していません")

        
    if player.is_playing:
        player.queue.clear()
        await player.stop()
        mbed = discord.Embed(title="停止", color=discord.Color.from_rgb(255, 255, 255))
        return await ctx.respond(embed=mbed)
    else:
        return await ctx.respond("現在音楽は流れていません")

@bot.slash_command(name="skip", description="スキップ", guild_ids=test_ids)
async def skip_command(ctx: discord.ApplicationContext):
    node = wavelink.NodePool.get_node()
    player = node.get_player(ctx.guild)
      
    if player is None:
        return await ctx.respond("botがボイスチャンネルに接続していません")

        
    if player.is_playing:
        await player.stop()
        mbed = discord.Embed(title="スキップ", color=discord.Color.from_rgb(255, 255, 255))
        return await ctx.respond(embed=mbed)
    else:
        return await ctx.respond("現在音楽は流れていません")

@bot.slash_command(name="pause", description="一時停止", guild_ids=test_ids)
async def pause_command(ctx: discord.ApplicationContext):
    node = wavelink.NodePool.get_node()
    player = node.get_player(ctx.guild)

    if player is None:
        return await ctx.respond("botがボイスチャンネルに接続していません")
        
    if not player.is_paused():
        if player.is_playing():
            await player.pause()
            mbed = discord.Embed(title="一時停止中", color=discord.Color.from_rgb(255, 255, 255))
            return await ctx.respond(embed=mbed)
        else:
            return await ctx.respond("現在音楽は流れていません")
    else:
        return await ctx.respond("既に一時停止中です")

@bot.slash_command(name="resume", description="再生", guild_ids=test_ids)
async def resume_command(ctx: discord.ApplicationContext):
    node = wavelink.NodePool.get_node()
    player = node.get_player(ctx.guild)

    if player is None:
        return await ctx.respond("botがボイスチャンネルに接続していません")
        
    if player.is_paused():
        await player.resume()
        mbed = discord.Embed(title="再生中", color=discord.Color.from_rgb(255, 255, 255))
        return await ctx.respond(embed=mbed)
    else:
        return await ctx.respond("音楽は一時停止されていません")

@bot.slash_command(name="volume", description="ボリュームを変更", guild_ids=test_ids)
async def volume_command(ctx: discord.ApplicationContext, to: Option(int, '変更したい数値')):
    if to > 100:
        return await ctx.respond("ボリュームは0~100の間で変更できます")
    elif to < 1:
        return await ctx.respond("ボリュームは0~100の間で変更できます")
        

    node = wavelink.NodePool.get_node()
    player = node.get_player(ctx.guild)

    await player.set_volume(to)
    mbed = discord.Embed(title=f"ボリュームが {to} に変更されました", color=discord.Color.from_rgb(255, 255, 255))
    await ctx.respond(embed=mbed)

@bot.slash_command(name="queue", description="キューを確認", guild_ids=test_ids)
async def queuecheck(ctx: discord.ApplicationContext):
    vc: wavelink.Player = ctx.voice_client
    if vc.queue.is_empty:
        return await ctx.respond("キューに曲はありません")
    embed = discord.Embed(title="キュー", color=discord.Color.from_rgb(255, 255, 255))
    queue = vc.queue.copy()
    songCount = 0
    for song in queue:
        songCount += 1
        embed.add_field(name=f"No.{str(songCount)}", value=f"`{song}`")
    await ctx.respond(embed=embed)

@bot.slash_command(name="socplay", description="SoundCloudの音楽を再生", guild_ids=test_ids)
async def splay(ctx: discord.ApplicationContext, *, search: Option(str, '曲名を入力')):
    track = await wavelink.SoundCloudTrack.search(query=search, return_first=True)
    button = PlayButton("再生")
    button2 = PauseButton("一時停止")
    button3 = StopButton("停止")
    button4 = DisconButton("退出")

    if not ctx.voice_client:
        vc: wavelink.Player = await ctx.author.voice.channel.connect(cls=wavelink.Player)
    else:
        vc: wavelink.Player = ctx.voice_client
        
    await vc.play(track)

    mbed = discord.Embed(title=f"再生中: {track}", color=discord.Color.from_rgb(255, 255, 255))
    view = View()
    view.add_item(button)
    view.add_item(button2)
    view.add_item(button3)
    view.add_item(button4)
    await ctx.respond(embed=mbed, view=view)
   
@bot.slash_command(name="splay", description="Spotifyの音楽を再生", guild_ids=test_ids)
async def spoplay(ctx: discord.ApplicationContext, *, search: Option(str, 'spotifyのurl')):
    button = PlayButton("再生")
    button2 = PauseButton("一時停止")
    button3 = StopButton("停止")
    button4 = DisconButton("退出")

    if not ctx.voice_client:
        vc: wavelink.Player = await ctx.author.voice.channel.connect(cls=wavelink.Player)
    else:
        vc: wavelink.Player = ctx.voice_client
        vc.chanctx = ctx.channel

    if vc.queue.is_empty and not vc.is_playing():
            try:
                
                track = await spotify.SpotifyTrack.search(query=search, return_first=True)

                await vc.play(track)
                mbed = discord.Embed(title=f"再生中: {track.title}", color=discord.Color.from_rgb(255, 255, 255))
                view = View()
                view.add_item(button)
                view.add_item(button2)
                view.add_item(button3)
                view.add_item(button4)
                await ctx.respond(embed=mbed, view=view)
            except Exception as e:
                await ctx.respond(e)
    else:
        try:
            await vc.queue.put_wait(track)
            await ctx.send(f'Added `{track}` to the queue...')
        except Exception as e:
            await ctx.respond(e)

@bot.slash_command(name="playstream", description="urlから音楽を再生", guild_ids=test_ids)
async def playstream(ctx: discord.ApplicationContext, url: str):
    button = PlayButton("再生")
    button2 = PauseButton("一時停止")
    button3 = StopButton("停止")
    button4 = DisconButton("退出")
        
    if not ctx.voice_client:
        vc: wavelink.Player = await ctx.author.voice.channel.connect(cls=wavelink.Player)
    else:
        vc: wavelink.Player = ctx.voice_client
    track = await vc.node.get_tracks(query=url, cls=wavelink.LocalTrack)
    
    if vc.queue.is_empty and not vc.is_playing():
        try:
            track = await vc.node.get_tracks(query=url, cls=wavelink.LocalTrack)

            await vc.play(track[0])
            mbed = discord.Embed(title=f"再生中: {url}", color=discord.Color.from_rgb(255, 255, 255))
            view = View()
            view.add_item(button)
            view.add_item(button2)
            view.add_item(button3)
            view.add_item(button4)
            await ctx.respond(embed=mbed, view=view)
        except Exception as e:
            await ctx.send(e)
        
   
        

   
@bot.slash_command(name="kodane", description="褒美だ.......", guild_ids=test_ids)
async def kplay(ctx: discord.ApplicationContext):
    search = "褒美だ。我の素材をくれてやる【GB素材】"
    track = await wavelink.YouTubeTrack.search(query=search, return_first=True)

    if not ctx.voice_client:
        vc: wavelink.Player = await ctx.author.voice.channel.connect(cls=wavelink.Player)
    else:
        vc: wavelink.Player = ctx.voice_client
        
    await vc.play(track)
    await ctx.respond("褒美だ、我の子種をくれてやる。")
    await ctx.respond("https://pbs.twimg.com/media/FK_tTvmaAAAYzMp.jpg")

@bot.event  
async def on_message(message):
    if not message.author.bot:
        cursor = await bot.db.execute("INSERT OR IGNORE INTO guildData (guild_id, user_id, exp) VALUES (?,?,?)", (message.guild.id, message.author.id, 1)) 

        if cursor.rowcount == 0:
            await bot.db.execute("UPDATE guildData SET exp = exp + 1 WHERE guild_id = ? AND user_id = ?", (message.guild.id, message.author.id))
            cur = await bot.db.execute("SELECT exp FROM guildData WHERE guild_id = ? AND user_id = ?", (message.guild.id, message.author.id))
            data = await cur.fetchone()
            exp = data[0]
            lvl = math.sqrt(exp) / bot.multiplier
                      
        
            if lvl.is_integer():
                await message.channel.send(f"{message.author.mention} おめでとう！ レベル {int(lvl)}に到達")

        await bot.db.commit()

    await bot.process_commands(message)

@bot.slash_command(name="stats", description="レベルのステータスを表示", guild_ids=test_ids)
async def stats(ctx: discord.ApplicationContext, member: Option(discord.Member,'メンバーを選択')):
    if member is None: member = ctx.author

    async with bot.db.execute("SELECT exp FROM guildData WHERE guild_id = ? AND user_id = ?", (ctx.guild.id, member.id)) as cursor:
        data = await cursor.fetchone()
        exp = data[0]

    async with bot.db.execute("SELECT exp FROM guildData WHERE guild_id = ?", (ctx.guild.id,)) as cursor:
        rank = 1
        async for value in cursor:
            if exp < value[0]:
                rank += 1

    lvl = int(math.sqrt(exp)//bot.multiplier)

    current_lvl_exp = (bot.multiplier*(lvl))**2
    next_lvl_exp = (bot.multiplier*((lvl+1)))**2

    lvl_percentage = ((exp-current_lvl_exp) / (next_lvl_exp-current_lvl_exp)) * 100

    embed = discord.Embed(title=f"{member.name}のステータス", colour=discord.Colour.gold())
    embed.add_field(name="レベル", value=str(lvl))
    embed.add_field(name="Exp", value=f"{exp}/{next_lvl_exp}")
    embed.add_field(name="ランク", value=f"{rank}/{ctx.guild.member_count}")
    embed.add_field(name="レベル進行度", value=f"{round(lvl_percentage, 2)}%")

    await ctx.respond(embed=embed)

@bot.slash_command(name="lederboard", description="リーダーボードを表示", guild_ids=test_ids)
async def leaderboard(ctx: discord.ApplicationContext):
    await ctx.respond("...") 
    buttons = {}
    for i in range(1, 6):
        buttons[f"{i}\N{COMBINING ENCLOSING KEYCAP}"] = i 

    previous_page = 0
    current = 1
    index = 1
    entries_per_page = 10

    embed = discord.Embed(title=f"リーダーボード Page {current}", description="", colour=discord.Colour.gold())
    msg = await ctx.send(embed=embed)

    for button in buttons:
        await msg.add_reaction(button)

    while True:
        if current != previous_page:
            embed.title = f"リーダーボード Page {current}"
            embed.description = ""

            async with bot.db.execute(f"SELECT user_id, exp FROM guildData WHERE guild_id = ? ORDER BY exp DESC LIMIT ? OFFSET ? ", (ctx.guild.id, entries_per_page, entries_per_page*(current-1),)) as cursor:
                index = entries_per_page*(current-1)

                async for entry in cursor:
                    index += 1
                    member_id, exp = entry
                    member = ctx.guild.get_member(member_id)
                    embed.description += f"{index}) {member.mention} : {exp}\n"

                await msg.edit(embed=embed)

        try:
            reaction, user = await bot.wait_for("reaction_add", check=lambda reaction, user: user == ctx.author and reaction.emoji in buttons, timeout=60.0)

        except asyncio.TimeoutError:
            return await msg.clear_reactions()

        else:
            previous_page = current
            await msg.remove_reaction(reaction.emoji, ctx.author)
            current = buttons[reaction.emoji]


bot.loop.create_task(initialize())
bot.run(トークン)
asyncio.run(bot.db.close())
