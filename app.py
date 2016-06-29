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

    def run(self):
        if self.client.rtm_connect():
            try:
                self.user_id = self.client.api_call("auth.test")['user_id']
                self.username = self.client.api_call("auth.test")['user']
                self._log(self.username + ": " + self.user_id)
            except:
                print Exception
            while True:
                self.process_messages(self.client.rtm_read())
                time.sleep(1)
        else:
            self._log("Connection failed.")

    def _log(self, message, level=' DEBUG '):
        """
        TODO this should actually put logs somewhere useful;
        """
        print str(datetime.datetime.utcnow()) + level + message

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
                else:
                    self._log(msg + " didn't appear to have text or subtype?")

                if 'user' in msg:
                    if msg['user'] != self.user_id:
                        self.filter_speak(message=body, room=msg['channel'])
