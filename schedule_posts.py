
import logging
import traceback
logging.getLogger().setLevel(logging.INFO)

from pprint import pprint
from handlers import *
from vk_api.bot_longpoll import VkBotEventType

from config import init_config
from context import context as ctx, init_context
init_config(env_vars=["WALL_TOKEN", "GROUP_ID", "MSG_TOKEN", "GROUP_ALBUM_ID"])
init_context()

logging.info("Bot started")


def process_command(msg):
    if len(msg.get("attachments")) > 0 and not msg["text"].startswith("//not"):
        process_attachments(msg)

for event in ctx.longpoll.listen():
    try:
        if event.type == VkBotEventType.MESSAGE_NEW:
            msg = event.object['message']
            process_command(msg)
    except Exception as e:
        logging.error(traceback.format_exc())
        

