import discord
import typing
import asyncio
import aiohttp
import random
from discord.commands import slash_command, Option
from discord.ext import commands
import giphy_client
from giphy_client.rest import ApiException

kasuga = ['https://prtimes.jp/i/2610/255/resize/d2610-255-984823-4.jpg','https://news.mynavi.jp/article/20190428-816092/images/001.jpg','https://bunshun.jp/mwimgs/d/d/-/img_dd73c56ad1cb77d2cc8908c19fd104eb147104.jpg','https://www.sanspo.com/resizer/09u0U--V-d-TOXyDEbfEHpJiLGw=/360x240/filters:focal(786x960:796x970)/cloudfront-ap-northeast-1.images.arcpublishing.com/sankei/DRLINAMP6VIUPOJXADQGMLGIMQ.jpg','https://dogatch.jp/prod/kanren_news/20211122/f439b447540b8e6ef14282295cc7908d.jpg','https://dogatch.jp/prod/kanren_news/20220125/5ca0aadeda68dd31800ede03a3469dd8.jpg','https://www.sanspo.com/resizer/a5ba_8VIl4H6a1dQiiQQNL0NpPI=/360x240/filters:focal(293x372:303x382)/cloudfront-ap-northeast-1.images.arcpublishing.com/sankei/4BALJANZJJKWTH55SESRDFPK2Y.jpg','https://c799eb2b0cad47596bf7b1e050e83426.cdnext.stream.ne.jp/img/article/000/253/272/bf0d8c1ab11b1bec0b7ccbca29d5ecf920190504125911274.jpg','https://storage.nana-music.com/picture/426706-8a045b57-aa2a-4799-b6eb-82786e79cb1d-large.png']
emails = ["Anderson","Ashwoon","Aikin","Bateman","Reira","5jo","Boyd","Soramame","Cast","skinnman0000"]
passwords = ["12345","975dhkhf","kji874hh8","iosf783hs","sludd378hdf","57oit9kd","ksl8973knf8d","k7hj4ek"]
quotes = ["ちんこ","うんち！","俺の名前はちんこ","ちんちん大好き","しねｎ","びんびん"]
randomWord = ["rainbow","red","blue","apple",]

class Neta(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Funny Cog is now ready!")

    @slash_command(name="meme", description="💩ミームが投稿されるコマンド💩")
    async def meme(self, ctx: discord.ApplicationContext):
       embed = discord.Embed(title="Meme", description="💩", color=discord.Color.from_rgb(255, 208, 0))
       async with aiohttp.ClientSession() as cs:
           async with cs.get('https://www.reddit.com/r/dankmemes/new.json?sort=hot') as r:
               res = await r.json()
               embed.set_image(url=res['data']['children'][random.randint(0, 25)]['data']['url'])
               await ctx.respond(embed=embed)

          
        
    @slash_command(name="kasuga", description="💩💩💩みんな大好き春日俊彰💩💩💩")
    async def ping(self, ctx: discord.ApplicationContext):
        await ctx.respond(random.choice(kasuga))                                                          
            
        
                                               

    @slash_command(name="hack", description="ハッキング？")
    async def hack(self, ctx: discord.ApplicationContext, *,  member: discord.Member):
        await ctx.respond(f"Hacking {member.mention} now...")
        await asyncio.sleep(1)

        await ctx.edit(content = f"Finding discord login...(2fa bypassed)")
        await asyncio.sleep(2)

        await ctx.edit(content = f"""Found:
    Email: '{member.name}{random.choice(emails)}@gmail.com'
    Password: '{random.choice(passwords)}'""")
        await asyncio.sleep(2)

        await ctx.edit(content = f"Fetching dms with closest friends (if you got any init)")
        await asyncio.sleep(2)

        await ctx.edit(content = f"""**Last DMs** '{random.choice(quotes)}' """)
        await asyncio.sleep(2)

        await ctx.edit(content = f"Finding most common word...")
        await asyncio.sleep(2)

        await ctx.edit(content = f"""mostCommon '{random.choice(randomWord)}' """)
        await asyncio.sleep(2)

        await ctx.edit(content = f"Injecting the big boy virus into the discriminator #{member.discriminator}")
        await asyncio.sleep(2)

        await ctx.edit(content = f"""Virus injected. nitro stolen""")
        await asyncio.sleep(2)

        await ctx.edit(content = f"""Setting up LINE account...""")
        await asyncio.sleep(2)

        await ctx.edit(content = f"""Hacking LINE account...""")
        await asyncio.sleep(2)

        await ctx.edit(content = f"""Fining IP address...""")
        await asyncio.sleep(2)

        await ctx.edit(content = f"""**IP address**: 127.0.0.1:8080...""")
        await asyncio.sleep(2)

        await ctx.edit(content = f"""Stealing data from the scary Government...""")
        await asyncio.sleep(2)

        await ctx.edit(content = f"""Reporting account to discord for breaking TOS...""")
        await asyncio.sleep(2)

        await ctx.edit(content = f"""Hacking your google history...""")
        await asyncio.sleep(2)

        await ctx.edit(content = f"""Finished hacking {member.mention} Thankyou!""")
        await asyncio.sleep(2)

        await member.edit(nick="繧上◆縺励?縺ｪ縺ｾ縺医?縺｡繧薙■繧薙〒縺")
        await asyncio.sleep(1)

        await member.send("https://fairworkcenter.org/wp-content/uploads/2018/04/hacked-skull.jpg")
        await asyncio.sleep(2)
        msg = await member.send("外部に情報を流出されたくなければ＄10000をあと10秒で振り込め")
        await asyncio.sleep(1)
        await msg.edit("外部に情報を流出されたくなければ＄10000をあと**9**秒で振り込め")
        await asyncio.sleep(1)
        await msg.edit("外部に情報を流出されたくなければ＄10000をあと**8**秒で振り込め")
        await asyncio.sleep(1)
        await msg.edit("外部に情報を流出されたくなければ＄10000をあと**7**秒で振り込め")
        await asyncio.sleep(1)
        await msg.edit("外部に情報を流出されたくなければ＄10000をあと**6**秒で振り込め")
        await asyncio.sleep(1)
        await msg.edit("外部に情報を流出されたくなければ＄10000をあと**5**秒で振り込め")
        await asyncio.sleep(1)
        await msg.edit("外部に情報を流出されたくなければ＄10000をあと**4**秒で振り込め")
        await asyncio.sleep(1)
        await msg.edit("外部に情報を流出されたくなければ＄10000をあと**3**秒で振り込め")
        await asyncio.sleep(1)
        await msg.edit("外部に情報を流出されたくなければ＄10000をあと**2**秒で振り込め")
        await asyncio.sleep(1)
        await msg.edit("外部に情報を流出されたくなければ＄10000をあと**1**秒で振り込め")
        await asyncio.sleep(1)

        await member.send("期限終了")

        await asyncio.sleep(2)

        msg2 = await member.send("**download/** #                                                            /")
        await asyncio.sleep(1)
        await msg2.edit("**downloading/** ####                                                               /")    
        await msg2.edit("**downloading/** ######                                                             /")
        await asyncio.sleep(1)  
        await msg2.edit("**downloading/** #########                                                          /")
        await msg2.edit("**downloading/** ##############                                                     /")
        await msg2.edit("**downloading/** ################################                                   /")
        await asyncio.sleep(1)
        await msg2.edit("**downloading/** ###################################################################/")
        await asyncio.sleep(2)
        await msg2.edit("completed")

        await member.send("繧上◆縺励?縺ｪ縺ｾ縺医?縺｡繧薙■繧薙〒縺")
        await member.send("繧上◆縺励?縺ｪ")
        await member.send("縺翫▽")
        await member.send("縺翫＞縺翫＞縺翫＞縺翫＞縺?♀")
        await member.send("髯ｳ蟄宣匍蟄")
        await member.send("縺?縺｡繧薙〒縺")
        await member.send("医?縺｡繧薙〒縺")
        await member.send("髮鷹ｭ壻ｹ")
        await member.send("縺顔夢繧後∴縺医∴縺医∴")
        await member.send("縺翫＞縺翫＞縺翫＞縺翫＞縺翫＞縺翫＞?茨ｽ?ｽ具ｽ?ｽ難ｽ鯉ｽ?ｽ具ｽ難ｽ")

    
    @slash_command(name="gif", description="gifを送信します。")
    async def gif(self, ctx: discord.ApplicationContext, *, text: Option(str, '送信したいgifのテーマ')):

        api_key="APIキー"
        api_instance = giphy_client.DefaultApi()

        try:
            api_response = api_instance.gifs_search_get(api_key, text, limit=5)
            lst = list(api_response.data)
            giff = random.choice(lst)

            await ctx.respond(giff.embed_url)

        except ApiException as e:
            await ctx.respond(e)

def setup(bot):
    bot.add_cog(Neta(bot))
