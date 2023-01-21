import discord
import logging

class Unflipper(discord.Client):
    def __init__(self, log_level=None, **kwargs):
        self.BASIC_TABLE = "┻━┻"
        self.AUTOFLIP_MSG = "(╯°□°)╯︵ " + self.BASIC_TABLE

        self.logger = logging.getLogger("discord.client.unflipper")
        if not log_level:
            log_level = logging.INFO
        self.logger.setLevel(log_level)

        intents = discord.Intents.default()
        intents.message_content = True
        intents.reactions = True
        
        super().__init__(intents=intents, **kwargs)

    async def on_message(self, message):
        # we do not want the bot to reply to itself
        if message.author.id == self.user.id:
            return

        if self.BASIC_TABLE in message.content:
            if message.author.id == 224697402383138817:
                await message.reply("Fuck you.", mention_author=True)
            elif self.AUTOFLIP_MSG in message.content:
                await self.unflip(message)
            else:
                reply_content = "Do...do I unflip it? O.o"
                reply = await message.reply(reply_content)
                await reply.add_reaction("✅")
                await reply.add_reaction("❌")

    async def on_raw_reaction_add(self, reactionEvent):
        message = await self.get_channel(reactionEvent.channel_id).fetch_message(reactionEvent.message_id)
        emoji = str(reactionEvent.emoji)

        # Ignore reactions from the bot and the flipper
        if reactionEvent.user_id in [self.user.id, message.reference.resolved.author.id]:
            self.logger.debug("Ignoring reaction \"{}\" on message {} due to reactor ({})".format(
                emoji, message.id, reactionEvent.member.name))
            return

        # Ignore reactions that we did not prompt
        reaction = discord.utils.get(message.reactions, emoji=emoji)
        if not reaction or not reaction.me:
            self.logger.debug("Ignoring reaction \"{}\" on message {} because it was unprompted".format(
                emoji, message.id))
            return

        if emoji == "✅":
            self.logger.debug("Unflipping message {} from {} due to reaction from {}".format(
                message.reference.resolved.id, message.reference.resolved.author.name, reactionEvent.member.name))
            await self.unflip(message.reference.resolved)
        elif emoji == "❌":
            self.logger.debug("Ignoring message {} from {} due to reaction from {}".format(
                message.reference.resolved.id, message.reference.resolved.author.name, reactionEvent.member.name))
        else:
            self.logger.warn("Fallback! Ignoring reaction \"{}\" on message {}, even though it was prompted".format(emoji, message.id))
            return

        for r in message.reactions:
            await r.remove(self.user)

    async def unflip(self, message):
        flips = message.content.count("┻━┻")
        reply_content = "┬─┬ノ( º \_ ºノ)   " * flips
        await message.reply(reply_content.strip(), mention_author=True)
