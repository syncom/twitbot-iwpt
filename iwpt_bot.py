#!/usr/bin/env python

import os
import sys
import subprocess
from twython import Twython


ApiKey = ''
ApiSecret = ''
AccessToken = ''
AccessTokenSecret = ''
rootdir = os.path.dirname(os.path.realpath(__file__))
cred_file = os.path.join(rootdir, '.auth')
twitter_allowed_char = 140

def get_api_token():
    ''' Obtain Twitter app's API token from file .auth
    Returns list
    '''
    f = open(cred_file, 'rb')
    c = f.read()
    t = c.splitlines()
    return t[0:4]

def get_today_str_iso8601():
    ''' Obtain current date in ISO8601 format, without the hyphens,
        e.g., 20170913.
    Returns str
    '''
    d = subprocess.check_output(["date", "+%Y%m%d"])
    d_str = d.translate(None, '\n')
    return d_str

def get_tweet_str():
    '''Obtain primality information for today
    Returns (isprime, str) pair
    '''
    script = os.path.join(rootdir, 'iswhatprime.sh')
    tweet_str = ''
    d_str = get_today_str_iso8601()
    gpout = subprocess.check_output([script, d_str])
    # If d_str is prime, first line would be 
    #        <d_str> is a prime\n
    # If d_str is not prime, first line would be
    #        <d_str> is not a prime\n
    line_1st = gpout.split('\n')[0]
    if line_1st[-9] == 's':
        # "is a prime"
        isprime = True
        tweet_str = 'Today ' + gpout
        if len(tweet_str) > twitter_allowed_char:
            tweet_str = tweet_str[:twitter_allowed_char - 3] + '...'
            
    else:
        # "is not a prime"; thus line_1st[-9] should be 't'
        isprime = False
        tweet_str = 'Today ' + d_str + ' is not a prime'

    return (isprime, tweet_str)


def do_tweet(str):
    ''' Tweet str to Twitter
    '''
    [ApiKey, ApiSecret, AccessToken, AccessTokenSecret] = get_api_token()
    api = Twython(ApiKey, ApiSecret, AccessToken, AccessTokenSecret)
    api.update_status(status=str)
    print "Tweeted: " + str


if __name__ == '__main__':
    '''
    Tweet today's primality information if today is a prime day
    '''
    (isprime, tweet_str) = get_tweet_str()
    
    if isprime:
#        print tweet_str
        do_tweet(tweet_str)
    else:
        print "Not tweeted: " + tweet_str

