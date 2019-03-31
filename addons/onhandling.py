import addons.watch as watch
import addons.alerts as alerts


class OnHandling:
    def __init__(self, bot):
        self.bot = bot

    async def on_message(self, message):
        await watch.Watch.watchlogging(self, message)
        if await alerts.Alerts.on_mention_check(self) and await alerts.Alerts.mentioned(self, message):
            await alerts.Alerts.mention_alert(self, message)
        #await watch.Watch.channellogging(self, message)

    async def on_message_delete(self, message):
        await watch.Watch.deletelogging(self, message)
        #await watch.Watch.channellogging(self, message)

    async def on_message_edit(self, before, after):
        await watch.Watch.editlogging(self, before, after)
        #await watch.Watch.channellogging(self, message)

    async def on_member_join(self, member):
        if await alerts.Alerts.on_join_check(self):
            await alerts.Alerts.join_alert(self, member)


def setup(bot):
    bot.add_cog(OnHandling(bot))
