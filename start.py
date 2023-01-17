#!/usr/bin/env python3

import discord
import os

class Unflipper(discord.Client):
    BASIC_TABLE = "┻━┻"
    AUTOFLIP_MSG = "(╯°□°)╯︵ " + BASIC_TABLE

    async def on_message(self, message):
        # we do not want the bot to reply to itself
        if message.author.id == self.user.id:
            return

        if self.AUTOFLIP_MSG in message.content:
            if message.author.id == 224697402383138817:
                await message.reply("Fuck you.", mention_author=True)
            else:
                await self.unflip(message)

        elif self.BASIC_TABLE in message.content:
            if message.author.id == 224697402383138817:
                await message.reply("Fuck you.", mention_author=True)
            reply_content = "Do...do I unflip it? O.o"
            reply = await message.reply(reply_content)
            await reply.add_reaction("✅")
            await reply.add_reaction("❌")

    async def on_raw_reaction_add(self, reactionEvent):
        if reactionEvent.member == self.user:
            return
        channel = client.get_channel(reactionEvent.channel_id)
        message = await channel.fetch_message(reactionEvent.message_id)
        if message.author != self.user:
            return

        # Build a doctored list of reactions to act on
        reactions = []
        for r in message.reactions:
            # Only look at reactions we prompted
            if r.me:
                # Ignore reactions from the flipper
                users = [x async for x in r.users()]
                if reactionEvent.member in users:
                    r.count -= 1
                reactions.append(r)

        # Valid messages should have 2 selectable reactions.
        if len(reactions) != 2:
            return

        # First person (who isn't the flipper) to react gets to decide
        if any(r.count >= 2 for r in reactions):
            for reaction in reactions:
                if reaction.emoji == "✅" and reaction.count >= 2:
                    await self.unflip(message.reference.resolved)
                # Remove our own reactions, so we stop acting on this message
                await reaction.remove(self.user)

    async def unflip(self, message):
        flips = message.content.count("┻━┻")
        reply_content = "┬─┬ノ( º \_ ºノ)   " * flips
        await message.reply(reply_content.strip(), mention_author=True)

intents = discord.Intents.default()
intents.message_content = True
intents.reactions = True

client = Unflipper(intents=intents)
client.run(os.environ.get('UNFLIPPER_TOKEN'))
