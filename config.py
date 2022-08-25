from dotenv import load_dotenv
import os

class Config:
    WALL_TOKEN = ""
    MSG_TOKEN = ""
    GROUP_ID = ""
    GROUP_ALBUM_ID = ""


config = Config()

def init_config(env_vars):
    global config
    load_dotenv()
    for var in env_vars:
        setattr(config, var, os.environ.get(var))
