import vk_api
from vk_api.bot_longpoll import VkBotLongPoll
from config import config
import logging

class Context:
    wall_vk_session: vk_api.VkApi = None
    wall_vk = None
    wall_upload: vk_api.VkUpload = None
    msg_vk_session: vk_api.VkApi = None
    msg_vk = None
    longpoll: VkBotLongPoll = None
    msg_upload: vk_api.VkUpload = None

context = Context()
logging.info("Context created")


def init_context():
    context.wall_vk_session = vk_api.VkApi(token=config.WALL_TOKEN)
    context.wall_vk = context.wall_vk_session.get_api()
    context.wall_upload = vk_api.VkUpload(context.wall_vk_session)

    context.msg_vk_session = vk_api.VkApi(token=config.MSG_TOKEN)
    context.msg_vk = context.msg_vk_session.get_api()
    context.longpoll = VkBotLongPoll(context.msg_vk_session, group_id=config.GROUP_ID)
    context.msg_upload = vk_api.VkUpload(context.msg_vk_session)
    logging.info("Context initialized")


