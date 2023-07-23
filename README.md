# twitbot-iwpt: Is What Prime Today?

[![Shellcheck](https://github.com/syncom/twitbot-iwpt/actions/workflows/shellcheck.yml/badge.svg)](https://github.com/syncom/twitbot-iwpt/actions/workflows/shellcheck.yml)
[![Pylint](https://github.com/syncom/twitbot-iwpt/actions/workflows/pylint.yml/badge.svg)](https://github.com/syncom/twitbot-iwpt/actions/workflows/pylint.yml)

A Twitter bot that tweets, if the current date in ISO 8601 format, without the
hyphens (e.g., 20170913), is a prime number. For example, on September 1,
2017, it would tweet

```text
Today 20170901 is a prime
a Chen prime
an Eisenstein prime
a Pythagorean prime
has a twin prime
has a cousin prime.
```

If the current date is not a prime number, it will tweet the factorization
of the ISO-8601-formatted date. For example,

```text
Today 20180503 is not a prime
20180503 = 7^2 x 37 x 11131
```

## Dependencies

- Python 3.6 or above
- Unix/Linux environment with the 'date' command and the [Pari/GP
  calculator](http://pari.math.u-bordeaux.fr/). On Ubuntu, `apt install pari-gp`
  will get Pari/GP installed.
- The ['prime_classes' project](https://github.com/syncom/prime_classes) on
  Github.

## Usage

Similar to that described in <https://github.com/syncom/twitbot-tih>.

1. Create a Twitter app and obtain the API Key, API Secret, Access Token, and
   Access Token Secret for the app. This can be done by following the
   instructions at:
   <https://developer.twitter.com/en/docs/twitter-api/getting-started/getting-access-to-the-twitter-api>.
   On 20230429, we started to see API authentication errors, and a message "This
   app has violated Twitter rules and policies" on the Twitter app setting page.
   According to [this
   discussion](https://twittercommunity.com/t/this-app-has-violated-twitter-rules-and-policies/191204/10),
   we signed up for the Free tier of "[Twitter API
   v2](https://developer.twitter.com/en/portal/products)" (at no cost), and
   clicked button "downgrade to free"; this resolved the auth issue. You may
   also need to put the Twitter app under a "project" for better organization
   and monitoring of the app.

1. Clone this repository with the submodule and change directory to it. Set up
   Python3 virtual environment.

   ```bash
   git clone --recursive https://github.com/syncom/twitbot-iwpt.git
   cd twitbot-iwpt
   # Set up virtualenv and pip install packages
   make install
   ```

1. Set up authentication and authorization secrets by following [this Getting
   Started
   guide](https://developer.twitter.com/en/docs/twitter-api/getting-started/getting-access-to-the-twitter-api).
   The preferred way is to set environment variables `IWPT_API_KEY`,
   `IWPT_API_SECRET`, `IWPT_ACCESS_TOKEN`, and `IWPT_ACCESS_SECRET` with API
   Key, API Secret, Access Token, and Access Token Secret values obtained in the
   first step. Alternatively, one can override the corresponding strings in the
   file '.auth' with appropriate secret strings.  When any of the aformetioned
   environment variables are set, they take precedence over values in the
   `.auth` file.

1. Run `./iwpt_bot_run.sh` to tweet. Note that it only tweets when the ISO 8601
   formatted string for today's date is a prime number. The log files for each
   day's tweet can be found in the 'logs' subdirectory. They keep state of the
   primality info and the tweet status, and are used by our application to make
   tweeting decisions.

1. (Optional) Create a cron job to invoke the bot multiple times a day, to
   account for sporadic connecitivity issues.
