from selenium import webdriver 
import discord
from discord.commands import slash_command, Option
from discord.ext import commands
import time


class Covid(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("covid Cog is now ready!")

    @slash_command(name="covid", description="大阪府の新型コロナウイルス新規感染者数を表示")
    async def covid(self, ctx: discord.ApplicationContext):
        
        await ctx.respond(
        view=discord.ui.View(
            discord.ui.Button(
                label="情報元サイト", url="https://www.watch.impress.co.jp/extra/covid19/?pref=27"
            )
        ),
    )
        async with ctx.typing():
            options = webdriver.ChromeOptions()
            options.add_argument('--headless')
            options.add_argument('--disable-gpu')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--remote-debugging-port=9222')
            options.add_experimental_option('excludeSwitches', ['enable-logging'])


            browser = webdriver.Chrome(options=options)
            browser.set_window_size(950, 800)
           
            browser.get('https://www.watch.impress.co.jp/extra/covid19/?pref=27') 
            data = browser.find_elements_by_class_name("extra-wrap")
            text = data[0].text
            time.sleep(5)
            browser.quit()

            embed=discord.Embed(title="大阪府新型コロナウイルス感染者数", color=discord.Color.from_rgb(255, 0, 0))
            embed.description=(text)
            await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Covid(bot))
