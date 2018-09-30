import addons.watch as watch


class OnHandling:
    def __init__(self, bot):
        self.bot = bot

    async def on_message(self, message):
        await watch.Watch.watchlogging(self, message)
        #await watch.Watch.channellogging(self, message)

    async def on_message_delete(self, message):
        await watch.Watch.deletelogging(self, message)
        #await watch.Watch.channellogging(self, message)

    async def on_message_edit(self, before, after):
        await watch.Watch.editlogging(self, before, after)
        #await watch.Watch.channellogging(self, message)


def setup(bot):
    bot.add_cog(OnHandling(bot))
