import discord
from redbot.core import commands
from gtts import gTTS
import os
import asyncio

class SimpleTTS(commands.Cog):
    """간단한 한글 TTS를 음성채널에 송출"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def tts(self, ctx, *, text: str):
        """TTS로 음성채널에서 <텍스트> 읽기"""
        if ctx.author.voice is None or ctx.author.voice.channel is None:
            await ctx.send("음성채널에 먼저 들어가 있어야 해요.")
            return

        channel = ctx.author.voice.channel
        voice_client = ctx.voice_client

        if voice_client is None or not voice_client.is_connected():
            voice_client = await channel.connect()
        elif voice_client.channel != channel:
            await voice_client.move_to(channel)

        # gTTS로 mp3 생성
        tts = gTTS(text=text, lang='ko')
        filename = "/tmp/tts_output.mp3"
        tts.save(filename)

        # 음성 재생
        audio_source = discord.FFmpegPCMAudio(filename)
        if not voice_client.is_playing():
            voice_client.play(audio_source)
            await ctx.send(f"🔊 `{text}` (을)를 읽는 중!")
        else:
            await ctx.send("이미 음성이 재생 중입니다. 잠시 후 다시 시도해 주세요.")

        # 재생 끝날 때까지 대기 후 파일 삭제
        while voice_client.is_playing():
            await asyncio.sleep(1)
        if os.path.exists(filename):
            os.remove(filename)

def setup(bot):
    bot.add_cog(SimpleTTS(bot))
