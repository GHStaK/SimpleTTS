from .simpletts import SimpleTTS

async def setup(bot):
    await bot.add_cog(SimpleTTS(bot))