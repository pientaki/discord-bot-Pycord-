from random import choices
import discord
from discord.ext import commands
from json import dumps
import requests
import json
from discord.commands import slash_command, Option

from janome.tokenizer import Tokenizer 
import random

class MarkovChain:
    def analyze(self, text):        
        t = Tokenizer()
        toks = list(t.tokenize(text))
        matrix = self.create_matrix(toks) 
        return self.markov(matrix)  

    def create_matrix(self, toks):
        mat = []
        i = 0

        while i < len(toks) - 2:
            t1 = toks[i]
            t2 = toks[i + 1]
            t3 = toks[i + 2]
            mat.append((t1, t2, t3))
            i += 1

        return mat

    def markov(self, mat):
        toks = self.find_start_toks(mat) 
        if toks is None:
            return None

        s = self.toks_to_text(toks)
        before_selected = None

        while True:
            candidates = self.grep_candidates(mat, toks)
            if not len(candidates):  
                if s[-1] != '。':
                    s += '。'
                return s

            selected = self.random_choice(before_selected, candidates)
            s += self.toks_to_text(selected) 
            if selected[1].surface == '。':  
                break

            before_selected = selected
            toks = selected

        return s

    def random_choice(self, before_selected, candidates):
        while True:
            selected = random.choice(candidates)
            if before_selected is None:
                break
            if before_selected[0].surface != selected[0].surface or \
               before_selected[1].surface != selected[1].surface:
                break
        return selected

    def grep_candidates(self, mat, toks):
        candidate = []

        for row in mat:
            if row[0].surface == toks[1].surface:
                candidate.append(row[1:])

        return candidate

    def find_start_toks(self, mat):
        if not len(mat):
            return None

        return mat[0][:2]

    def toks_to_text(self, toks):
        s = ''
        for tok in toks:
            s += tok.surface
        return s

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
            payload = {"api_key":"API KEY","agent_id":"AGENT ID","utterance": rewords,"uid":"UID"}
            url = 'https://api-mebo.dev/api'
            r = requests.post(url=url, headers=headers, data=json.dumps(payload))
            text = r.text
            data = json.loads(text)
            await message.channel.send('{}'.format(data['bestResponse']['utterance']))

    @slash_command(name="markov", description="マルコフ連鎖で文章を生成します")
    async def mkv(self, ctx: discord.ApplicationContext, text: Option(str, "もととなるテキスト(二文以上)")):
        m = MarkovChain()
        result = m.analyze(text)

        await ctx.respond(result)


def setup(bot):
    bot.add_cog(Ai(bot))
