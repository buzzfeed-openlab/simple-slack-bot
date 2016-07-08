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
            except Exception as e:
                self._log(e, level=' ERROR ')
            while True:
                self.process_messages(self.client.rtm_read())
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
        for call, response in self.searches.iteritems():
            if re.search(call, message):
                self.client.api_call("chat.postMessage", as_user="true",
                                     channel=room, text=response)

    def process_messages(self, messages):
        for msg in messages:
            # We're only interested in entries of type "message"
            if msg['type'] == "message":
                # TODO also check the text of expanded links.
                if 'text' in msg:
                    body = msg.get('text')
                elif 'subtype' in msg:
                    body = msg['message']['text']
                if body is None:
                    self._log(msg + " didn't appear to have text or subtype?")

                if msg.get('user') != self.user_id:
                    self.filter_speak(message=body, room=msg['channel'])
