from slackclient import SlackClient
import time
import re
import datetime


class Bot(object):

    def __init__(self, token, searches):
        self.searches = searches
        self.client = SlackClient(token)
        self.username = {}
        self.user_id = {}
        self.ims = set()

    def run(self):
        if self.client.rtm_connect():
            try:
                self.user_id = self.client.api_call("auth.test")['user_id']
                self.username = self.client.api_call("auth.test")['user']
                self._log(self.username + ": " + self.user_id)
            except:
                print Exception
            # Make a list of IM channels to listen to:
            for im in self.client.api_call("im.list")['ims']:
                self.ims.add(im.get('id'))
                self._log(str(self.ims))

            while True:
                # self.process_messages(self.client.rtm_read())
                self.log_messages(self.client.rtm_read())
                time.sleep(0.25)
        else:
            self._log("Connection failed.")

    def _log(self, message, level=' DEBUG '):
        """
        TODO this should actually put logs somewhere useful;
        """
        print str(datetime.datetime.utcnow()) + level + str(message)

    def filter_speak(self, room, message):
        """
        posts a message to a channel if it matches the call.
        """
        for call in self.searches:
            response = self.searches[call]
            if re.search(call, message):
                self.client.api_call("chat.postMessage", as_user="true",
                                     channel=room, text=response)

    def process_messages(self, messages):
        for msg in messages:
            # We're only interested in entries of type "message"
            if msg['type'] == "message":
                # TODO also check the text of expanded links.
                if 'text' in msg:
                    body = msg['text']
                elif 'subtype' in msg:
                    if msg['subtype'] == "message_changed":
                        body = msg['message']['text']
                if not body:
                    self._log(msg + " didn't appear to have text or subtype?")

                if 'user' in msg:
                    if msg['user'] != self.user_id:
                        self.filter_speak(message=body, room=msg['channel'])

    def log_messages(self, messages):
        """
        Log everything. You don't really want to do this, but it is helpful for
        debugging, and for writing new functions.
        """
        boring_types = (['presence_change', 'reconnect_url', 'user_typing'])
        for msg in messages:
            if msg['type'] == "message":
                try:
                    self._log(msg.get("text"))
                except:
                    self._log(str(msg))
                try:
                    if re.search(self.user_id, msg["text"]) or \
                       re.search(self.username, msg["text"]):
                        self._log("The bot was mentioned!")
                    if msg.get("channel") in self.ims:
                        self._log("^^ this looks like a DM.")
                except:
                    self._log(Exception)
            elif msg['type'] == "im_open":
                self._log("Someone opened an IM with you.")
                self.ims.add(im.get('id'))
            elif msg['type'] not in boring_types:
                # If it isn't a message what is it?
                try:
                    channel = msg.get("channel")
                except:
                    channel = "(no channel)"
                log_string = str(msg['type']) + " in " + str(channel)
                self._log(log_string)
                # Search for DMs
