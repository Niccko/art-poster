import logging
from context import context as ctx
import booru_parser
import random
import vk_api
from utils import download_image
import os
from config import config

def process_booru(cmd):
    raise NotImplementedError
    query, page, limit = msg['text'][2:].rsplit(' ', 2)
    try:
        page = int(page)
        limit = int(limit)
    except ValueError:
        ctx.msg_vk.messages.send(
            peer_id=msg['peer_id'],
            random_id=random.randint(0, 2000000000),
            message='охуел',
        )
    if limit <= 10:
        result = booru_parser.parse(query, page, limit)
        photos = ctx.msg_upload.photo_messages(photos=result)
        attachments = []
        for ph in photos:
            try:
                attachments.append('photo{}_{}'.format(ph['owner_id'], ph['id']))
            except vk_api.exceptions.ApiError as e:
                print(e)
        print(attachments)
        ctx.msg_vk.messages.send(
            peer_id=msg['peer_id'],
            random_id=random.randint(0, 2000000000),
            message=query,
            attachments=','.join(attachments),
        )
    else:
        ctx.msg_vk.messages.send(
            peer_id=msg['peer_id'],
            random_id=random.randint(0, 2000000000),
            message='не больше 10',
        )

def process_attachments(msg):
    files = []
    for atch in msg["attachments"]:
        if(atch["type"] == "photo"):
            file_url = atch["photo"]["sizes"][-1]["url"]
            filename = file_url.split("/")[-1].split("?")[0]
            download_image(file_url, filename)
            files.append(filename)
    if len(files) > 0:
        uploaded_files = ctx.wall_upload.photo(photos=files, group_id=config.GROUP_ID, album_id=config.GROUP_ALBUM_ID)
        for file in files:
            os.remove(file)
        wall_attachments = map(lambda ph: 'photo{}_{}'.format(ph['owner_id'], ph['id']), uploaded_files)
        ctx.wall_vk.wall.post(
            owner_id = f"-{config.GROUP_ID}", 
            from_group = 1, 
            attachments = ",".join(wall_attachments))
        logging.info(f"Uploaded {len(files)} file to album {config.GROUP_ALBUM_ID}")

