from app import Bot
from os import environ

pairs = {}

pairs["[kK]nock[, -]*[kK]nock"] = "Who's there?"

pope_bot = Bot(environ['API_TOKEN'], pairs)
pope_bot.run()
