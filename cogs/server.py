import discord
from discord import permissions
from discord.commands import slash_command, Option
from discord.ext import commands
import humanfriendly
import datetime

class Server(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Server Cog is now ready!")

    @slash_command(name="server", description="サーバー情報を表示")
    async def server(self, ctx: discord.ApplicationContext):
        owner=str(ctx.guild.owner)
        region = str(ctx.guild.region)
        guild_id = str(ctx.guild.id)
        memberCount = str(ctx.guild.member_count)
        icon = str(ctx.guild.icon)
        desc=ctx.guild.description
        no_voice_channels = len(ctx.guild.voice_channels)
        no_text_channels = len(ctx.guild.text_channels)
        emoji_string = ""
        for e in ctx.guild.emojis:
            if e.is_usable():
                emoji_string += str(e)
    
        embed = discord.Embed(
            title=ctx.guild.name + " サーバー情報",
            description=desc,
            color=discord.Color.blue()
        )
        embed.set_thumbnail(url=icon)
        embed.add_field(name="ID", value=guild_id, inline=True)
        embed.add_field(name="地域", value=region, inline=True)
        embed.add_field(name="オーナー", value=owner, inline=False)
        embed.add_field(name="メンバー数", value=memberCount, inline=True)
        embed.add_field(name="カスタム絵文字", value=emoji_string or "登録なし", inline=False)
        embed.add_field(name="# ボイスチャンネル", value=no_voice_channels)
        embed.add_field(name="# テキストチャンネル", value=no_text_channels)

        await ctx.respond(embed=embed)

        members=[]
        async for member in ctx.guild.fetch_members(limit=150) :
            mememed = discord.Embed(title="メンバー", color=discord.Color.from_rgb(62, 138, 111))
            mememed.add_field(name="ステータス", value='名前 : {}\t 状態 : {}\n 参加日時 {}'.format(member.display_name,str(member.status),str(member.joined_at)))
            await ctx.send(embed=mememed)


    @slash_command(name="user-info", description="ユーザー情報を表示")
    async def user_info(self, inter, member: Option(discord.Member,'メンバーを選択')):

        emb = discord.Embed(color=discord.Color.blurple())
        emb.title = str(member)
        emb.description = (
        f"**作成日時:** `{member.created_at}`\n"
        f"**ID:** `{member.id}`"
        ) 
        emb.set_thumbnail(url=member.avatar)
        await inter.respond(embed=emb)

    @slash_command(name="kick", description="メンバーをキックします(使用注意)")
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx: discord.ApplicationContext, member: Option(discord.Member,'メンバーを選択'), reason: Option(str, 'キックする理由')):
        await member.kick(reason=reason)
        embed=discord.Embed(title="KICK", color=discord.Color.from_rgb(255, 0, 0))
        embed.add_field(name="メンバー", value=f"{member.mention}", inline=False)
        embed.add_field(name="理由", value=f"{reason}", inline=False)
        await ctx.respond(embed=embed)

    @slash_command(name="ban", description="メンバーをbanします(使用注意)")
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx: discord.ApplicationContext, member: Option(discord.Member,'メンバーを選択'), reason: Option(str, 'banする理由')):
        await member.ban(delete_message_days=7, reason=reason)
        embed=discord.Embed(title="BAN", color=discord.Color.from_rgb(255, 0, 0))
        embed.add_field(name="メンバー", value=f"{member.mention}", inline=False)
        embed.add_field(name="理由", value=f"{reason}", inline=False)
        await ctx.respond(embed=embed)

    @slash_command(name="timeout", description="メンバーをタイムアウトします")
    async def timeout(self, ctx: discord.ApplicationContext, member: Option(discord.Member,'メンバーを選択'), time: Option(str, 'タイムアウトする時間'), *, reason: Option(str, 'タイムアウトする理由')):
        time = humanfriendly.parse_timespan(time)
        await member.timeout(until = discord.utils.utcnow() + datetime.timedelta(seconds=time), reason=reason)
        embed=discord.Embed(title="TIMEOUT", color=discord.Color.from_rgb(255, 0, 0))
        embed.add_field(name="メンバー", value=f"{member.mention}", inline=False)
        embed.add_field(name="期間", value=f"{time}", inline=False)
        embed.add_field(name="理由", value=f"{reason}", inline=False)
        await ctx.respond(embed=embed)
        await member.send(f"あなたは `{ctx.guild}` でタイムアウトされました\n"
        f"理由: `{reason}`\n" f"期間: `{time}`")

    @slash_command(name="removetimeout", description="メンバーのタイムアウトを解除します")
    async def remove_timeout(self, ctx: discord.ApplicationContext, member: Option(discord.Member,'メンバーを選択'), *, reason=None):
        await member.timeout(until=None, reason=reason)
        embed=discord.Embed(title="TIMEOUT解除", color=discord.Color.from_rgb(255, 0, 0))
        embed.add_field(name="メンバー", value=f"{member.mention}", inline=False)
        embed.add_field(name="理由", value=f"{reason}", inline=False)
        await ctx.respond(embed=embed)
        await member.send(f"あなたの `{ctx.guild}` でのタイムアウトは解除されました\n"
        f"理由: `{reason}`")


    @slash_command(name="mute", description="メンバーをミュート")
    async def mute(self, ctx: discord.ApplicationContext, member: Option(discord.Member,'メンバーを選択'), *, reason: Option(str, 'muteする理由'), role: Option(discord.Role, "ロールがある場合は取り除くロール名を入れて下さい。", required=False)):
        guild = ctx.guild
        mutedRole = discord.utils.get(guild.roles, name = "ミュート中")

        if not mutedRole:
            await ctx.respond("ロールを作成中")
            mutedRole = await guild.create_role(name = "ミュート中")

            for channel in guild.channels:
                await channel.set_permissions(mutedRole, speak=False, send_messages=False, read_message_history=True, read_messages=False)

        await member.add_roles(mutedRole, reason=reason)
        embed = discord.Embed(title="ミュート",color=discord.Color.from_rgb(255, 0, 0))
        embed.description =(f"{member.mention} は {ctx.guild} でミュートされました\n"
        f"理由: {reason}")
        await ctx.respond(embed=embed)
        await member.send(f"あなたは `{ctx.guild}` でミュートされました\n"
        f"理由: `{reason}`")

        if role == None:
            return
        else:
            await member.remove_roles(role)

                

    @slash_command(name="unmute", description="ミュート解除するコマンド")
    async def unmute(self, ctx: discord.ApplicationContext, member: Option(discord.Member,'メンバーを選択')):
        mutedRole = discord.utils.get(ctx.guild.roles, name="ミュート中")

        await member.remove_roles(mutedRole)
        embed = discord.Embed(title="ミュート解除",color=discord.Color.blurple())
        embed.description = (f"{member.mention} のミュートが解除されました")
        await ctx.respond(embed=embed)
        await member.send(f"**あなたの `{ctx.guild.name}` でのミュートは解除されました**")
        

    @slash_command(name="clear", description="送信したメッセージを消去します")
    async def clear(self, ctx: discord.ApplicationContext, amount: Option(str, '削除したい件数')):
        await ctx.channel.purge(limit=int(amount))
        await ctx.respond("メッセージが削除されました")


    @slash_command(name="ping", description="botのping値を測定します")
    async def ping(self, ctx: discord.ApplicationContext):
        raw_ping = self.bot.latency
        ping = round(raw_ping * 1000)
        embed = discord.Embed(title="Ping",color=discord.Color.blurple())
        embed.description = (f"BotのPing値は**{ping}**msです")
        await ctx.respond(embed=embed)


def setup(bot):
    bot.add_cog(Server(bot))
