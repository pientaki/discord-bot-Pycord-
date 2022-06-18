#Copyright © 2021-2022 Sorrows[SOR] All Rights Reserved.
import discord
from discord.ext import commands, pages, tasks
from discord.commands import Option
from discord.ui import Button, View, Select
import aiohttp
import os
import math
import aiosqlite
import asyncio
from itertools import cycle

intents = discord.Intents.default()
intents.members = True
intents.message_content = True


bot = commands.Bot(command_prefix="*", intents=intents)
bot.multiplier = 1
status=cycle(["/cmdでコマンド一覧","うんち！","メンバーを監視中"])

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')


async def initialize():
    await bot.wait_until_ready()
    bot.db = await aiosqlite.connect("expData.db")
    await bot.db.execute("CREATE TABLE IF NOT EXISTS guildData (guild_id int, user_id int, exp int, PRIMARY KEY (guild_id, user_id))")

@bot.event
async def on_ready():
    print("Bot is ready!")
    change_status.start()
   
@tasks.loop(seconds=10)
async def change_status():
    await bot.change_presence(status=discord.Status.online,activity=discord.Game(next(status)))

@bot.slash_command(name="cmd", description="コマンド一覧を表示")
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
   f"**/splay ＜spotifyのurl＞ : **音楽をSpotifyで検索して再生\n"
   f"**/socplay ＜タイトル＞ : **音楽をSoundCloud経由で検索して再生\n"
   f"**/playstream ＜url＞ : **urlから音楽を再生\n"
   f"**/stop : **音声を停止\n"
   f"**/skip : **スキップ\n"    
   f"**/resume : **再生\n"
   f"**/pause : **一時停止\n"
   f"**/queue : **キュー覧を表示\n"
   f"**/pause : **一時停止\n"
   f"**/volume ＜音量＞ : **音量を変更\n"
   f"**/disconnect : **ボイスチャンネルから切断\n")

    convembed = discord.Embed(title="**:mag_right:  便利？コマンド**",color=discord.Color.blurple())
    convembed.description=(f"**/trans ＜翻訳したい言語＞ ＜内容＞ : **翻訳機能\n"
   f"**/language : **翻訳言語一覧\n"
   f"**/search ＜検索ワード＞ : **ネットで検索\n"
   f"**/vote ＜テーマ＞ ＜選択肢１＞ ＜選択肢２＞ : **投票を作成\n"
   f"**/covid : **大阪府の新型コロナウイルス新規感染者数を検索\n"
   f"**/imagesearch : **ネット上の画像を検索\n")

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
   f"**/stats ＜メンバー＞ : **ステータスを表示\n"
   f"**/ping : **botのpingを表示\n")

    gameembed = discord.Embed(title="**:video_game: ゲームコマンド**",color=discord.Color.blurple())
    gameembed.description=(f"**/akinator : **アキネイターをプレイ\n"
   f"**/minesweeper : **マインスイーパーをプレイ\n")

    funembed = discord.Embed(title="**💩 その他コマンド**",color=discord.Color.blurple())
    funembed.description=(f"**/meme : **ミームを投稿\n"
   f"**/hack : **ハッキングツール？\n"
   f"**/kodane : **褒美だ.......\n"
   f"**/kasuga : **春日俊彰をランダムで送信\n"
   f"**メンション ＜テキスト＞  : **AIとおしゃべり")
   
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

bot.sniped_messages = {}

@bot.event
async def on_message_delete(message):
    bot.sniped_messages[message.guild.id] = (message.content, message.author, message.channel.name, message.created_at)

    

@bot.slash_command(name="snipe", description="最新の削除されたメッセージを復元")
async def snipe(ctx: discord.ApplicationContext):
    try:
        contents, author, channel_name, time = bot.sniped_messages[ctx.guild.id]
        
    except:
        await ctx.respond("削除されたメッセージが見つかりません")
        return

    embed = discord.Embed(description=contents, color=discord.Color.purple(), timestamp=time)
    embed.set_author(name=f"{author.name}#{author.discriminator}", icon_url=author.avatar)
    embed.set_footer(text=f"#{channel_name}")

    await ctx.respond(embed=embed)


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

@bot.slash_command(name="stats", description="レベルのステータスを表示")
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

@bot.slash_command(name="lederboard", description="リーダーボードを表示")
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
