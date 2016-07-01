from app import Bot
from os import environ

pairs = {}
pairs["[kK]nock[, -]*[kK]nock"] = "Who's there?"

# If you don't know your user_id, there are a few ways to find it.
owners = (['U0BGRJLMU'])

pope_bot = Bot(environ['API_TOKEN'], pairs, owners)
pope_bot.run()
