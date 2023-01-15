#!/usr/bin/env python3

import discord
import os

class MyClient(discord.Client):
    async def on_message(self, message):
        # we do not want the bot to reply to itself
        if message.author.id == self.user.id:
            return

        flips = message.content.count("(╯°□°)╯︵ ┻━┻")

        if flips > 0:
            if message.author.id == 224697402383138817:
                reply_content = "Fuck you."
            else:
                reply_content = "┬─┬ノ( º \_ ºノ)   " * flips
            await message.reply(reply_content.strip(), mention_author=True)

        elif message.content.count("┻━┻") > 0:
            reply_content = "Do...do I unflip it? O.o"
            reply = await message.reply(reply_content)
            await reply.add_reaction("✅")
            await reply.add_reaction("❌")

    async def on_raw_reaction_add(self, reactionEvent):
        if reactionEvent.member == self.user:
            return
        channel = client.get_channel(reactionEvent.channel_id)
        message = await channel.fetch_message(reactionEvent.message_id)

        if any(x.count >= 2 for x in message.reactions if x.me):
            for reaction in [x for x in message.reactions if x.me]:
                if reaction.emoji == "✅" and reaction.count >= 2:
                    flips = message.reference.resolved.content.count("┻━┻")
                    reply_content = "┬─┬ノ( º \_ ºノ)   " * flips
                    await message.reference.resolved.reply(reply_content.strip(), mention_author=True)
                await reaction.remove(self.user)

intents = discord.Intents.default()
intents.message_content = True
intents.reactions = True

client = MyClient(intents=intents)
client.run(os.environ.get('UNFLIPPER_TOKEN'))
