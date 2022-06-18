import discord
from discord.ext import commands
import requests
from discord.commands import slash_command, Option


api_key = "APIキー"
base_url = "http://api.openweathermap.org/data/2.5/weather?"

class Weather(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(name="weawther", description="天気を表示")
    async def weatherinfo(self, ctx: discord.ApplicationContext, city: Option(str, "場所を指定") ):
        city_name = city
        complete_url = base_url + "appid=" + api_key + "&q=" + city_name + "&lang="+ "ja"
        response = requests.get(complete_url)
        x = response.json()

        if x["cod"] != "404":
            async with ctx.typing():
                y = x["main"]
                current_temperature = y["temp"]
                current_temperature_celsiuis = str(round(current_temperature - 273.15))
                current_pressure = y["pressure"]
                current_humidity = y["humidity"]
                z = x["weather"]
                weather_description = z[0]["description"]
                icon = z[0]["icon"]
                w = x["wind"]
                wind_speed = w["speed"]
                wind_direction = w["deg"]
                c = x["clouds"]
                cloud_description = c["all"]
                embed = discord.Embed(title=f"{city_name}の天気",
                                color=ctx.guild.me.top_role.color)
                embed.add_field(name="詳細", value=f"**{weather_description}**", inline=False)
                embed.add_field(name="気温(C)", value=f"**{current_temperature_celsiuis}°C**")
                embed.add_field(name="湿度(%)", value=f"**{current_humidity}%**")
                embed.add_field(name="気圧(hPa)", value=f"**{current_pressure}hPa**")
                embed.add_field(name="風速", value=f"**{wind_speed}m/s**")
                embed.add_field(name="風向き", value=f"**{wind_direction}**")
                embed.add_field(name="曇り率", value=f"**{cloud_description}%**", inline=False)
                embed.set_thumbnail(url=f"http://openweathermap.org/img/wn/{icon}@2x.png")
                embed.set_footer(text=f"{ctx.author.name}のリクエスト")


                await ctx.respond(embed=embed)
        
        else:
            await ctx.respond("場所が見つかりません")

def setup(bot):
    bot.add_cog(Weather(bot))
