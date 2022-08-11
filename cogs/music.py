import discord
import wavelink
from wavelink.ext import spotify
from discord.ext import commands
from discord.commands import slash_command, Option, SlashCommandGroup



class Buttons(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(style=discord.ButtonStyle.blurple, emoji="⏯️", row=0)
    async def playpause_button(self, button: discord.ui.Button, interaction: discord.Interaction):
        node = wavelink.NodePool.get_node()
        player = node.get_player(interaction.guild)

        if player is None:
            return await interaction.response.send_message("botがボイスチャンネルに接続していません", ephemeral=True)
        
        if player.is_paused():
            await player.resume()
            mbed1 = discord.Embed(title="再生中", color=discord.Color.from_rgb(255, 255, 255))
            return await interaction.response.send_message(embed=mbed1, ephemeral=True)
        elif player.is_playing():
            await player.pause()
            mbed = discord.Embed(title="一時停止", color=discord.Color.from_rgb(255, 255, 255))
            return await interaction.response.send_message(embed=mbed, ephemeral=True)
        else:
            return await interaction.response.send_message("現在音楽は流れていません", ephemeral=True)

    @discord.ui.button(style=discord.ButtonStyle.blurple, emoji="⏹️", row=0)
    async def stop_button(self, button: discord.ui.Button, interaction: discord.Interaction):
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

    @discord.ui.button(style=discord.ButtonStyle.blurple, emoji="⏭️", row=0)
    async def skip_button(self, button: discord.ui.Button, interaction: discord.Interaction):
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

    @discord.ui.button(style=discord.ButtonStyle.red, emoji="🔚", row=0)
    async def dc_button(self, button: discord.ui.Button, interaction: discord.Interaction):
        node = wavelink.NodePool.get_node()
        player = node.get_player(interaction.guild)

        if player is None:
            return await interaction.response.send_message("botがボイスチャンネルに接続していません", ephemeral=True)
    
        await player.disconnect()
        mbed = discord.Embed(title="ボイスチャンネルから退出", color=discord.Color.from_rgb(255, 255, 255))
        await interaction.response.send_message(embed=mbed)



#class PlayButton(Button):
    #def __init__(self, label):
        #super().__init__(label=label, style=discord.ButtonStyle.green)

    #async def callback(self, interaction):
        #node = wavelink.NodePool.get_node()
        #player = node.get_player(interaction.guild)

        #if player is None:
            #return await interaction.response.send_message("botがボイスチャンネルに接続していません", ephemeral=True)
            
        #if player.is_paused():
            #await player.resume()
            #mbed = discord.Embed(title="再生中", color=discord.Color.from_rgb(255, 255, 255))
            #return await interaction.response.send_message(embed=mbed, ephemeral=True)
        #else:
            #return await interaction.response.send_message("音楽は一時停止されていません", ephemeral=True)
        



class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        bot.loop.create_task(self.create_nodes())
    
    async def create_nodes(self):
        await self.bot.wait_until_ready()
        await wavelink.NodePool.create_node(bot=self.bot, host="lavalink.tomatotomato3.repl.co", port="443", password="sorrows",https=True, spotify_client=spotify.SpotifyClient(client_id="d52f6a05b7ac4ea1b953eadbd2b6ba45", client_secret="e43ff5d74bcd4eb28e55e5976b7b282e"))
    
    @commands.Cog.listener()
    async def on_ready(self):
        print("Music Cog is now ready!")

    @commands.Cog.listener()
    async def on_wavelink_node_ready(self, node: wavelink.Node):
        print(f"Node <{node.identifier}> is now Ready!")

    music = SlashCommandGroup("music", "音楽コマンド")
            
    @music.command(name="play", description="YouTubeの音楽を再生")
    async def play(self, ctx: discord.ApplicationContext, *, search: Option(str, '曲名を入力')):

        await ctx.response.defer()
        search = await wavelink.YouTubeTrack.search(query=search, return_first=True)

        if not ctx.voice_client:
            vc: wavelink.Player = await ctx.author.voice.channel.connect(cls=wavelink.Player)
            embed=discord.Embed(title=f"ボイスチャンネル {ctx.author.voice.channel.name} に接続", color=discord.Color.from_rgb(255, 255, 255))
            await ctx.followup.send(embed=embed)
        else:
            vc: wavelink.Player = ctx.voice_client
            vc.chanctx = ctx.channel

        if vc.queue.is_empty and not vc.is_playing():

            await vc.play(search)

            mbed = discord.Embed(title="再生中", color=discord.Color.from_rgb(255, 255, 255))
            mbed.add_field(name="タイトル", value=search.title)
            mbed.add_field(name="再生時間", value=round(search.duration / 60, 2))
            mbed.add_field(name="ボリューム", value=vc.volume)
            mbed.add_field(name="チャンネル", value=search.author) 
            mbed.set_image(url=search.thumb)

            view = Buttons()
            await ctx.followup.send(embed=mbed, view=view)
        else:
            await vc.queue.put_wait(search)
            await ctx.followup.send(f'`{search}` をキューに追加しました')
        

    @commands.Cog.listener()
    async def on_wavelink_track_end(self, player: wavelink.Player, track , reason):

        if not player.queue.is_empty:
            ctx = player.chanctx
            new_song = player.queue.get()
            
            await player.play(new_song)
            view = Buttons()

            embed = discord.Embed(title="再生中", color=discord.Color.from_rgb(255, 255, 255))
            embed.add_field(name="タイトル", value=new_song.title)
            embed.add_field(name="再生時間", value=round(new_song.duration / 60, 2))
            embed.add_field(name="ボリューム", value=player.volume)
            embed.add_field(name="チャンネル", value=new_song.author) 
            embed.set_image(url=new_song.thumb) 
            await ctx.send(embed=embed, view=view)
        
    #slash_command(name="join", description="コマンド一覧を表示")
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

    @music.command(name="disconnect", description="ボイスチャンネルから退出")
    async def leave_command(self, ctx: discord.ApplicationContext):
        node = wavelink.NodePool.get_node()
        player = node.get_player(ctx.guild)

        if player is None:
            return await ctx.send("botがボイスチャンネルに接続していません")
        
        await player.disconnect()
        mbed = discord.Embed(title="ボイスチャンネルから退出", color=discord.Color.from_rgb(255, 255, 255))
        await ctx.respond(embed=mbed)

      
    
    @music.command(name="stop", description="停止")
    async def stop_command(self, ctx: discord.ApplicationContext):
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

    @music.command(name="skip", description="スキップ")
    async def skip_command(self, ctx: discord.ApplicationContext):
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

    @music.command(name="pause", description="一時停止")
    async def pause_command(self, ctx: discord.ApplicationContext):
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

    @music.command(name="resume", description="再生")
    async def resume_command(self, ctx: discord.ApplicationContext):
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

    @music.command(name="volume", description="ボリュームを変更")
    async def volume_command(self, ctx: discord.ApplicationContext, volume: Option(int, '変更したい数値')):
        vol=volume / 100
        if vol > 5:
            return await ctx.respond("ボリュームは0~500の間で変更できます")
        elif vol < 0.001 :
            return await ctx.respond("ボリュームは0~500の間で変更できます")
            
        node = wavelink.NodePool.get_node()
        player = node.get_player(ctx.guild)

        if player is None:
            return await ctx.respond("botがボイスチャンネルに接続していません")
        else:
            await player.set_volume(vol)
            mbed = discord.Embed(title=f"ボリュームが {volume} に変更されました", color=discord.Color.from_rgb(255, 255, 255))
            await ctx.respond(embed=mbed)
    
    @music.command(name="queue", description="キューを確認")
    async def queuecheck(self, ctx: discord.ApplicationContext):
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

    @music.command(name="socplay", description="SoundCloudの音楽を再生")
    async def splay(self, ctx: discord.ApplicationContext, *, search: Option(str, '曲名を入力')):

        await ctx.response.defer()
        
        if not ctx.voice_client:
            vc: wavelink.Player = await ctx.author.voice.channel.connect(cls=wavelink.Player)
        else:
            vc: wavelink.Player = ctx.voice_client
            

        if vc.queue.is_empty and not vc.is_playing():
                try:
                    track = await wavelink.SoundCloudTrack.search(query=search, return_first=True)
                    await vc.play(track)

                    mbed = discord.Embed(title=f"再生中", color=discord.Color.from_rgb(255, 255, 255))
                    mbed.add_field(name="タイトル", value=track.title)
                    mbed.add_field(name="再生時間", value=round(track.duration / 60, 2))
                    mbed.add_field(name="ボリューム", value=vc.volume) 
                    mbed.add_field(name="著作者", value=track.author)
                    mbed.set_image(url="https://logos-world.net/wp-content/uploads/2020/10/SoundCloud-Logo.png")

                    view = Buttons()
                    await ctx.followup.send(embed=mbed, view=view)
                except Exception as e:
                    await ctx.followup.send(e)
        else:
            await ctx.respond("現時点ではこの再生形式はキュー機能に対応していません（近日対応予定）")
    
    @music.command(name="splay", description="Spotifyの音楽を再生")
    async def spoplay(self, ctx: discord.ApplicationContext, *, search: Option(str, 'spotifyのurl')):

        await ctx.response.defer()

        if not ctx.voice_client:
            vc: wavelink.Player = await ctx.author.voice.channel.connect(cls=wavelink.Player)
        else:
            vc: wavelink.Player = ctx.voice_client
            vc.chanctx = ctx.channel

        if vc.queue.is_empty and not vc.is_playing():
                try:
                    
                    track = await spotify.SpotifyTrack.search(query=search, return_first=True)

                    await vc.play(track)
                    mbed = discord.Embed(title="再生中", color=discord.Color.from_rgb(255, 255, 255))
                    mbed.add_field(name="タイトル", value=track.title)
                    mbed.add_field(name="再生時間", value=round(track.duration / 60, 2))
                    mbed.add_field(name="ボリューム", value=vc.volume)
                    mbed.add_field(name="著作者", value=track.author) 
                    mbed.set_image(url="https://storage.googleapis.com/spotifynewsroom-jp.appspot.com/1/2020/12/Spotify_Logo_CMYK_Green.png")

                    view = Buttons()
                    
                    await ctx.followup.send(embed=mbed, view=view)
                except Exception as e:
                    await ctx.followup.send(e)
        else:
            await ctx.respond("現時点ではspotifyはキュー機能に対応していません（近日対応予定）")
            
    @music.command(name="playstream", description="urlから音楽を再生")
    async def playstream(self, ctx: discord.ApplicationContext, url: str):

        await ctx.response.defer()
            
        if not ctx.voice_client:
            vc: wavelink.Player = await ctx.author.voice.channel.connect(cls=wavelink.Player)
        else:
            vc: wavelink.Player = ctx.voice_client
        track = await vc.node.get_tracks(query=url, cls=wavelink.LocalTrack)
        
        if vc.queue.is_empty and not vc.is_playing():
            try:
                track = await vc.node.get_tracks(query=url, cls=wavelink.LocalTrack)

                await vc.play(track[0])
                mbed = discord.Embed(title="再生中", color=discord.Color.from_rgb(255, 255, 255))
                mbed.add_field(name="url", value=url)
                mbed.add_field(name="ボリューム", value=vc.volume) 
                mbed.set_image(url="https://wavelink.readthedocs.io/en/1.0/_static/logo.png")

                view = Buttons()

                await ctx.followup.send(embed=mbed, view=view)
            except Exception as e:
                await ctx.followup.send(e)

        else:
            await ctx.respond("現時点ではこの再生形式はキュー機能に対応していません（近日対応予定）")
            
        
    @slash_command(name="kodane", description="褒美だ.......")
    async def kplay(self, ctx: discord.ApplicationContext):
        search = "褒美だ。我の素材をくれてやる【GB素材】"
        track = await wavelink.YouTubeTrack.search(query=search, return_first=True)

        if not ctx.voice_client:
            vc: wavelink.Player = await ctx.author.voice.channel.connect(cls=wavelink.Player)
        else:
            vc: wavelink.Player = ctx.voice_client
            
        await vc.play(track)
        await ctx.respond("褒美だ、我の子種をくれてやる。")
        await ctx.respond("https://pbs.twimg.com/media/FK_tTvmaAAAYzMp.jpg")

    @music.command(name="bassboost", description="低音をブーストします")
    async def filterbass(self, ctx: discord.ApplicationContext):
        vc: wavelink.Player = ctx.voice_client

        if vc is None:
            return await ctx.send("Not in voice channel")
        bands = [
            (0, -0.075), (1, 0.125), (2, 0.125), (3, 0.1), (4, 0.1),
            (5, .05), (6, 0.075), (7, 0.0), (8, 0.0), (9, 0.0),
            (10, 0.0), (11, 0.0), (12, 0.125), (13, 0.15), (14, 0.05)
        ]
        await vc.set_filter(wavelink.Filter(equalizer=wavelink.Equalizer(name="MyOwnFilter",bands=bands)), seek=True)
        await ctx.respond("ブースト開始")

    @music.command(name="boostremove", description="ブースト解除")
    async def filterrmv(self, ctx: discord.ApplicationContext):
        vc: wavelink.Player = ctx.voice_client
        await vc.set_filter(wavelink.Filter(equalizer=wavelink.Equalizer.flat()),seek=True)
        await ctx.respond("ブースト解除")


def setup(bot):
    bot.add_cog(Music(bot))
