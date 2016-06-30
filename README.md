## Getting Started

You're going to need an auth key -- so start by creating a new bot configuration and noting the API_TOKEN.

The app looks for an api token in your environment variables. If you're a `bash` user, set that with:

    export API_TOKEN='abc-1234xyzFakeTokenString'

and then you can use

    python run.py

to get your bot going. You probably want to set up some different pairs in `run.py`, though. If this is already confusing, I'm super happy to help. [Just ask](https://github.com/buzzfeed-openlab/simple-slack-bot/issues).

Where do you get an API_TOKEN? I am not even sure I know. I got mine at: <https://buzzfeed.slack.com/apps/new/A0F7YS25R-bots> but that URL is pretty specific to my Team. Try <https://my.slack.com/services/new/bot>, though.

I'll be honest: it took me longer than it should have to work out how an oath token is different from a bot token is different from an app key.


# Heroku Deploy
You can run it from your own computer. But you probably want it running on a server. Because this is pretty lightweight, I'm running it on Heruku.

There are probably a few ways to get set up on Heroku. Here's what I did:
[`heroku create botname`](https://devcenter.heroku.com/articles/creating-app) -- that created a heroku URL and added a heroku remote to my `.git/config`

You're also going to need a [`.env` file](https://devcenter.heroku.com/articles/heroku-local#add-a-config-var-to-your-env-file). And that's where you'll want to set your api token. Locally, you can just edit `.env` and add a line like:

    API_TOKEN = abc-1234xyzFakeTokenString

To set the vars on your Heroku deploy (ie. not locally) you need to do `heroku config:set API_TOKEN=abc-1234xyzFakeTokenString`. And consider reading more about [config vars on Heroku](https://devcenter.heroku.com/articles/config-vars#setting-up-config-vars-for-a-deployed-application).


Then you have to push to Heroku with `git push heroku master` (assuming `master` is the branch you want).

# Useful reading

A smattering of URL's that I needed.

<http://docs.python-guide.org/en/latest/dev/virtualenvs/>

<https://medium.com/@julianmartinez/how-to-write-a-slack-bot-with-python-code-examples-4ed354407b98#.nh8i8681g>


# To Do
+ Respond to DMs (or do ~something~ with them)
+ act on DMs
