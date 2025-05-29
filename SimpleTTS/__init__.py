from .simpletts import SimpleTTS

def setup(bot):
    bot.add_cog(SimpleTTS(bot))
