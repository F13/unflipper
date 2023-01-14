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


intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
client.run(os.environ.get('UNFLIPPER_TOKEN'))