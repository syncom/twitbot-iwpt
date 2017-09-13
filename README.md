# twitbot-iwpt: What Prime Is Today?

A Twitter bot that tweets, if the current date in ISO 8601 format without the
hyphens (e.g., 20170913) is a prime number. For example, on September 1, 2017,
it would tweet

```
Today, 20170901, is a prime, a Chen prime, an Eisenstein prime, a Pythagorean
prime, has a twin prime, has a cousin prime.
```

# Dependencies
- Python 2.7, and modules: wikipedia, twython, pyOpenSSL, ndg-httpsclient,
  pyasn1
- Unix/Linux environment with the 'date' command and the Pari/GP calculator
- The ['prime_classes' Pari-GP script on
  github](https://github.com/syncom/prime_classes)

# Usage
Similar to that described in https://github.com/syncom/twitbot-tih.

1. Create a Twitter app and obtain the API Key, API Secret, Access Token, and
Access Token Secret for the app. This can be done by following the
instructions at:
http://www.instructables.com/id/Raspberry-Pi-Twitterbot/?ALLSTEPS.

2. Override the corresponding strings in the file '.auth' with appropriate
Twitter app API access token strings obtained in the last step.

3. Run 'python iwpt_bot.py' to tweet.

4. (Optional) Create a cron job to invoke the bot once a day.

