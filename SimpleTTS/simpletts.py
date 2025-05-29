from redbot.core import commands
import discord
from gtts import gTTS
import os
import asyncio

class SimpleTTS(commands.Cog):
    """간단한 TTS를 음성채널에 송출"""

    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(
        name="tts",
        description="TTS로 음성채널에서 입력된 텍스트를 읽어줍니다."
    )
    async def tts(self, ctx: commands.Context, *, text: str):
        """TTS로 음성채널에서 <텍스트> 읽기 (프리픽스/슬래시 모두 지원)"""
        # 음성채널 체크
        if ctx.author.voice is None or ctx.author.voice.channel is None:
            await ctx.reply("❌ 음성채널에 먼저 들어가 있어야 해요.", ephemeral=True)
            return

        channel = ctx.author.voice.channel
        # 봇이 이미 음성채널에 있으면 가져오기
        voice_client = ctx.voice_client
        if voice_client is None or not voice_client.is_connected():
            voice_client = await channel.connect()
        elif voice_client.channel != channel:
            await voice_client.move_to(channel)

        # TTS mp3 생성
        tts = gTTS(text=text, lang='ko')
        filename = "/tmp/tts_output.mp3"
        tts.save(filename)

        # ffmpeg로 음성 재생
        audio_source = discord.FFmpegPCMAudio(filename)
        if not voice_client.is_playing():
            voice_client.play(audio_source)
            await ctx.reply(f"🔊 `{text}` 읽는 중!", ephemeral=True)
        else:
            await ctx.reply("이미 음성이 재생 중입니다. 잠시 후 다시 시도해 주세요.", ephemeral=True)

        # 재생 끝날 때까지 대기 후 파일 삭제
        while voice_client.is_playing():
            await asyncio.sleep(1)
        if os.path.exists(filename):
            os.remove(filename)

    # 선택: 봇이 음성채널에서 나가는 명령(옵션)
    @commands.hybrid_command(
        name="leavevc",
        description="봇을 음성채널에서 내보냅니다."
    )
    async def leavevc(self, ctx: commands.Context):
        if ctx.voice_client:
            await ctx.voice_client.disconnect()
            await ctx.reply("음성채널에서 퇴장했어요.", ephemeral=True)
        else:
            await ctx.reply("봇이 현재 음성채널에 있지 않아요.", ephemeral=True)
