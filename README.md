# twitbot-iwpt: What Prime Is Today?

A Twitter bot that tweets, if the current date in ISO 8601 format, without the
hyphens (e.g., 20170913), is a prime number. For example, on September 1,
2017, it would tweet

```
Today 20170901 is a prime 
a Chen prime
an Eisenstein prime
a Pythagorean prime
has a twin prime
has a cousin prime.
```

# Dependencies
- Python 2.7, and modules: twython, pyOpenSSL, ndg-httpsclient, pyasn1
- Unix/Linux environment with the 'date' command and the [Pari/GP
  calculator](http://pari.math.u-bordeaux.fr/)
- The ['prime_classes' project](https://github.com/syncom/prime_classes) on
  Github

# Usage
Similar to that described in https://github.com/syncom/twitbot-tih.

1. Create a Twitter app and obtain the API Key, API Secret, Access Token, and
Access Token Secret for the app. This can be done by following the
instructions at:
http://www.instructables.com/id/Raspberry-Pi-Twitterbot/?ALLSTEPS.

2. Override the corresponding strings in the file '.auth' with appropriate
Twitter app API access token strings obtained in the last step.

3. Run `python iwpt_bot.py` (or `./iwpt_bot_run.sh`) to tweet. Note that it
only tweets when the ISO 8601 formatted string for today's date is a prime
number. The log files for each day's tweet can be found in the 'logs' 
subdirectory. They keep state of the primality info and the tweet status,
and are used by our application to make tweeting decisions.

4. (Optional) Create a cron job to invoke the bot multiple times a day. 

