import asyncio
import discord
import datetime
from googletrans import Translator
from discord.commands import slash_command, Option
from discord.ui import Button, View
from discord.ext import commands
import googletrans
from googlesearch import search
from urllib import parse
from googleapiclient.discovery import build
import random
import wikipedia
from selenium import webdriver

translator = Translator()
api_key = "APY KEY"

class Google(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
       
    @commands.Cog.listener()
    async def on_ready(self):
        print("Search Cog is now ready!")

    @slash_command(name="translate", description="翻訳機能")
    async def trans(self, ctx: discord.ApplicationContext, lang_to: Option(str, '翻訳したい言語を入力(ex. en,ja,hi...)'), text: Option(str, '翻訳したいテキスト')):
        lang_to = lang_to.lower()
        if lang_to not in googletrans.LANGUAGES and lang_to not in googletrans.LANGCODES:
            raise commands.BadArgument("language error!")
            
        translator = googletrans.Translator()
        text_translated = translator.translate(text, dest=lang_to).text
        await ctx.respond(text_translated)
   
    @slash_command(name="language", description="翻訳言語一覧")
    async def language(self,ctx: discord.ApplicationContext):
        embed = discord.Embed(title="翻訳言語一覧",color=discord.Color.blurple())
        embed.description=(f"**Japanese :** ja \n"f"**English :** en \n"f"**Hindi :** hi\n\n"f"**:united_nations: その他**\n" "https://py-googletrans.readthedocs.io/en/latest/")
        await ctx.respond(embed=embed)

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if reaction.count == 1:
            if str(reaction.emoji) == "🇮🇳":
                translator = Translator()
                country = translator.detect(text=reaction.message.content)
                trans_en = translator.translate(text=reaction.message.content,  src=country.lang, dest='hi')
                await reaction.message.channel.send(trans_en.text)

            if str(reaction.emoji) == "🇯🇵":
                translator = Translator()
                country = translator.detect(text=reaction.message.content)
                trans_en = translator.translate(text=reaction.message.content,  src=country.lang, dest='ja')
                await reaction.message.channel.send(trans_en.text)

            if str(reaction.emoji) == "🇺🇸":
                translator = Translator()
                country = translator.detect(text=reaction.message.content)
                trans_en = translator.translate(text=reaction.message.content,  src=country.lang, dest='en')
                await reaction.message.channel.send(trans_en.text)
          
    @slash_command(name="vote", description="投票機能")
    async def poll(self, ctx: discord.ApplicationContext,  topic: Option(str, '投票テーマ'), choice1: Option(str, '選択肢１'), choice2: Option(str, '選択肢２'), time: Option(int, "投票期間（秒）")):
        await ctx.respond("**投票開始**")
        t_delta = datetime.timedelta(hours=9)
        JST = datetime.timezone(t_delta, 'JST')
        embed = discord.Embed(title = topic, description = f":one: {choice1}\n\n:two: {choice2}", color = ctx.author.color, timestamp = datetime.datetime.now(JST))
        embed.set_footer(text = f"投票作成者 : {ctx.author.name}")
        embed.set_thumbnail(url = ctx.author.avatar)
        message = await ctx.send(embed = embed)
        await message.add_reaction("1️⃣")
        await message.add_reaction("2️⃣")
        await asyncio.sleep(time)

        newmessage = await ctx.channel.fetch_message(message.id)
        onechoice = await newmessage.reactions[0].users().flatten()
        secchoice = await newmessage.reactions[1].users().flatten()

        result = "TIE"
        if len(onechoice)>len(secchoice):
            result = choice1
        elif len(secchoice)>len(onechoice):
            result = choice2
        embed = discord.Embed(title = topic, description = f"結果 : {result}", color = ctx.author.color, timestamp = datetime.datetime.now(JST))
        embed.set_footer(text = f"{choice1} || {choice2}")

        await newmessage.edit(embed = embed)

    @slash_command(name="googlesearch", description="Googleで検索(上位5件分)")
    async def gsearch(self, ctx: discord.ApplicationContext, word: Option(str, '検索ワード')):
        kensaku = word
        for url in search(kensaku, lang="jp",num_results = 5):
            await ctx.respond(url)

    @slash_command(name="search", description="インターネットの検索結果のリンクを生成")
    async def search(self, ctx: discord.ApplicationContext, *, word: Option(str, '検索ワード')):
        param = parse.urlencode({"q": word})
        await ctx.respond(
            f" `{word}` についての検索結果は以下の通りです。",
            view=discord.ui.View(
                discord.ui.Button(
                    label="Google", url=f"https://www.google.com/search?{param}"
                ),
                discord.ui.Button(
                    label="Bing", url=f"https://www.bing.com/search?{param}"
                ),
                discord.ui.Button(
                    label="DuckDuckGo", url=f"https://www.duckduckgo.com/?{param}"
                ),
            ),
        )

    @slash_command(name="imagesearch", description="画像を検索")
    async def showpic(self, ctx: discord.ApplicationContext, *, search: Option(str, '検索したい画像名')):
        t_delta = datetime.timedelta(hours=9)
        JST = datetime.timezone(t_delta, 'JST')
        ran = random.randint(0, 9)
        resource = build("customsearch", "v1", developerKey=api_key).cse()
        result = resource.list(
            q=f"{search}", cx="KEY", searchType="image"
        ).execute()
        url = result["items"][ran]["link"]
        embed = discord.Embed(title=f" `{search}` の画像", timestamp=datetime.datetime.now(JST))
        embed.set_image(url=url)
        embed.set_footer(text=f"{ctx.author.name}のリクエスト")
        await ctx.respond(embed=embed)

    @slash_command(name="wiki", description="wikipediaで検索")
    async def wiki(self, ctx: discord.ApplicationContext, word: Option(str, "検索ワード")):
        wikipedia.set_lang("ja")
        try:
            embed = discord.Embed(title=f"{word}")
            embed.add_field(name="概要", value=wikipedia.summary(word))
            embed.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/thumb/b/b3/Wikipedia-logo-v2-en.svg/1784px-Wikipedia-logo-v2-en.svg.png")
            await ctx.respond(embed=embed)

        except wikipedia.exceptions.DisambiguationError as e:
            embed = discord.Embed(title="検索失敗", description="下の候補から選んで下さい")
            embed.add_field(name="候補", value=e)
            embed.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/thumb/b/b3/Wikipedia-logo-v2-en.svg/1784px-Wikipedia-logo-v2-en.svg.png")
            await ctx.respond(embed=embed)

    @slash_command(name="screenshot", description="ネット上のページのスクリーンショットを撮影")
    async def ss(self, ctx: discord.ApplicationContext, urlorword: Option(str, "URLか検索したいページの名前")):

        await ctx.response.defer()

        try:

            options = webdriver.ChromeOptions()
            options.add_argument('--headless')
            options.add_argument('--disable-gpu')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--remote-debugging-port=9222')
            options.add_experimental_option('excludeSwitches', ['enable-logging'])
            browser = webdriver.Chrome(options=options)
            browser.set_window_size(950, 800)

            if not 'http' in str(urlorword):
                kensaku = urlorword
                for url in search(kensaku, lang="jp",num_results = 1):
                    browser.get(url)
                    browser.get_screenshot_as_file('screenshot.png')

                    file = discord.File('screenshot.png', filename='image.png')
                    embed = discord.Embed(title=f"{url}")
                    embed.set_image(url='attachment://image.png')
                    await ctx.followup.send(file=file, embed=embed)
                    browser.quit()

            else:
                browser.get(urlorword)
                browser.get_screenshot_as_file('screenshot.png')

                file = discord.File('screenshot.png', filename='image.png')

                
                embed = discord.Embed(title=f"{urlorword}")
                embed.set_image(url='attachment://image.png')
                await ctx.followup.send(file=file, embed=embed)
                browser.quit()

        except Exception as e:
            await ctx.followup.send(e)    

def setup(bot):
    bot.add_cog(Google(bot))
