import logging
import os
from app.__version__ import __version__
from app.bot.commands import main


_log = logging.getLogger(__name__)
_log.info("Wellness Bot: %s", __version__)
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD_ID')
main()
