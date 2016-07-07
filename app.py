from slackclient import SlackClient
import time
import re
import datetime


class Bot(object):

    def __init__(self, token, searches, boss):
        self.boss = boss
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
            except Exception as e:
                self._log(e, level=' ERROR ')
            # Make a list of IM channels to listen to:
            for im in self.client.api_call("im.list")['ims']:
                self.ims.add(im.get('id'))
                self._log(str(self.ims))
            # Find the User ID of the owner

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

    def relay_home(self, message):
        """
        Should have looked up the rooms that owners live in.
        """
        for bosser in self.boss:
            im = self.client.api_call("im.open", user=bosser)
            im_chan = im.get('channel')
            if im_chan is not None:
                im_chan_id = im_chan.get('id')
            try:
                if message.get('user') != self.user_id:
                    self._log(message)
                    self.client.api_call("chat.postMessage", as_user="true",
                                         channel=im_chan_id,
                                         text=message.get('text'))
            except Exception as e:
                self._log(e, level=' ERROR ')

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
                if msg.get("channel") in self.ims:
                    body = msg.get('text')
                    relay_home(body)
                if 'text' in msg:
                    body = msg.get('text')
                elif 'subtype' in msg:
                    body = msg['message']['text']
                if body is None:
                    self._log(msg + " didn't appear to have text or subtype?")

                if msg.get('user') != self.user_id:
                    self.filter_speak(message=body, room=msg['channel'])

    def log_messages(self, messages):
        """
        Log everything. You don't really want to do this, but it is helpful for
        debugging, and for writing new functions.
        """
        boring_type = (['dnd_updated_user', 'presence_change', 'reconnect_url',
                        'user_typing', 'reaction_added', 'file_shared',
                        'file_change'])
        for msg in messages:
            if msg['type'] == "message":
                if msg.get("channel") in self.ims:
                    self.relay_home(msg)
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
                except Exception as e:
                    self._log(e, level=' ERROR ')
            elif msg['type'] == "im_created":
                self._log("Someone opened an IM with you.")
                self.ims.add(im.get('id'))
            elif msg['type'] not in boring_type:
                self._log(msg)
                channel = msg.get("channel")
                log_string = str(msg['type']) + " in " + str(channel)
                self._log(log_string)
                # Search for DMs
