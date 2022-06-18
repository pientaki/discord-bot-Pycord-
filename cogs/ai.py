import discord
from discord.ext import commands
import requests
import json


class Ai(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("AI Cog is now ready!")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.attachments:
            pass
        elif self.bot.user in message.mentions:       
            words = message.content
            rewords = words[22:]
            headers = {"Content-Type": "application/json"}
            payload = {"api_key":"あなたのAPIキー","agent_id":"あなたのエージェントのID","utterance": rewords,"uid":"あなたのID"}
            url = 'https://api-mebo.dev/api'
            r = requests.post(url=url, headers=headers, data=json.dumps(payload))
            text = r.text
            data = json.loads(text)
            await message.channel.send('{}'.format(data['bestResponse']['utterance']))

def setup(bot):
    bot.add_cog(Ai(bot))
