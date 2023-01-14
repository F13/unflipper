FROM gorialis/discord.py

COPY . /app

ENTRYPOINT /app/start.sh