#!/usr/bin/env python

import os
import sys
import errno
import subprocess
import re
from twython import Twython

ApiKey = ''
ApiSecret = ''
AccessToken = ''
AccessTokenSecret = ''
rootdir = os.path.dirname(os.path.realpath(__file__))
cred_file = os.path.join(rootdir, '.auth')
TWITTER_ALLOWED_CHAR = 140


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


def is_str_prime(d_str):
    '''Returns True if d_str is a prime, False otherwise
    '''
    script = os.path.join(rootdir, 'isprime.sh')
    gpout = subprocess.check_output([script, d_str], shell=False)
    return True if gpout.strip() == '1' else False


def prime_tweet_str(d_str):
    '''
    Returns a string to tweet for prime d_str
    '''
    script = os.path.join(rootdir, 'iswhatprime.sh')
    gpout = subprocess.check_output([script, d_str])
    tweet_str = 'Today ' + gpout
    return tweet_str


def print_base_expo_pair(pair):
    '''Format print (base, exponent) pairs. For example, for ('3' ,'2'),
       it prints '3^2'; for ('3', '1'), it prints '3'.
    Returns string output in specified format
    '''
    if pair[1] == '1':
        outstr = pair[0]
    else:
        outstr = pair[0] + '^' + pair[1]
    return outstr


def composite_tweet_str(d_str):
    '''
    Returns a string to tweet for composite d_str
    '''
    script = os.path.join(rootdir, 'factorit.sh')
    gpout = subprocess.check_output([script, d_str]).strip('\n\[\]Mat')
    gpoutlist = re.split(r'[;,\s]\s*', gpout)
    base_expo_pairs = zip(gpoutlist[0::2], gpoutlist[1::2]) # a list of pairs
    it = iter(base_expo_pairs)
    # Differentiate head and tail, for formatting
    head = it.next()
    tail = list(it)
    tweet_str = 'Today ' + d_str + ' is not a prime\n' \
                + d_str + ' = ' + print_base_expo_pair(head)
    for item in tail:
        tweet_str = tweet_str + ' x ' + print_base_expo_pair(item)
    return tweet_str


def get_tweet_str(d_str):
    '''Obtain primality information for d_str
    Returns (isprime, str) pair
    '''
    if is_str_prime(d_str):
        return (True, prime_tweet_str(d_str))
    else:
        return (False, composite_tweet_str(d_str))


def get_log_file_path(d_str):
    '''Get a string representing the absolute path the log file.
    Returns logfilepath
    '''
    logdir = os.path.join(rootdir, 'logs')
    logfilepath = os.path.join(logdir, d_str + '.log')
    return logfilepath


def write_tweet_str_to_file(d_str):
    '''Write the string to tweet, as well as the primality information and the
       twitter status for the tweet_str to logfile under the 'logs/'
       directory. A log file for this application always has a file name of
       the format <d_str>.log, e.g., 20170914.log. The content of
       a log file follows the following format: the first line of the file is
       0 or 1, where 0 means the text in the file has not been tweeted, and 1
       means the text in the file has already been tweeted; the second line of
       the file is 0 or 1, where 0 means the date for this file is not a
       prime, and 1 means the date for this file is a prime; the remaining
       text in the file is the tweet_str. 
    Returns logfilepath
    '''
    (isprime, tweet_str) = get_tweet_str(d_str)
    logfilepath = get_log_file_path(d_str)

    istweeted_str ='0'
    isprime_str = '1' if isprime else '0'
    log_str = istweeted_str + '\n' + isprime_str + '\n' + tweet_str
#    print('log_str: ' + log_str)

    with open(logfilepath, 'w') as logfile:
        logfile.write(log_str)

    return logfilepath


def mark_logfile_tweeted(logfilepath):
    '''Mark the log file as 'tweeted', by setting the first character to '1'.
    Returns None
    '''
    with open(logfilepath, 'r') as fin:
        oldstr = fin.read()

    templist = list(oldstr)
    templist[0] = '1'
    newstr = ''.join(templist)

    with open(logfilepath, 'w') as fout:
        fout.write(newstr)


def get_tweet_str_from_file(logfilepath):
    '''Obtain the string to tweet from a log file under the 'logs/' directory.
       A log file for this application always has a file name of the format
       <today_str_iso8601>.log, e.g., 20170914.log. The content of a log file
       follows the following format: the first line of the file is 0 or 1,
       where 0 means the text in the file has not been tweeted, and 1 means
       the text in the file has already been tweeted; the second line of the
       file is 0 or 1, where 0 means the date for this file is not a prime,
       and 1 means the date for this file is a prime; the remaining text in
       the file is the tweet_str. This function checks if tweet_str is too
       long or not, and truncates tweet_str if it is too long.

       Note that a log file is generated by the script, and shall not be
       modified manually.
    Returns (istweeted, isprime, tweet_str) triple
    '''
    tweet_str = ''
    with open(logfilepath) as logfile:
        istweeted = (logfile.readline().strip() == '1')
        isprime = (logfile.readline().strip() == '1')

        for line in logfile:
            tweet_str = tweet_str + line

    if len(tweet_str) > TWITTER_ALLOWED_CHAR:
                tweet_str = tweet_str[:TWITTER_ALLOWED_CHAR - 3] + '...'

    return (istweeted, isprime, tweet_str)


def do_tweet(str):
    ''' Tweet str to Twitter
    '''
    [ApiKey, ApiSecret, AccessToken, AccessTokenSecret] = get_api_token()
    api = Twython(ApiKey, ApiSecret, AccessToken, AccessTokenSecret)
    api.update_status(status=str)
    print("Tweeted: " + str)


if __name__ == '__main__':
    '''
    Tweet today's primality information if today is a prime day.
    It first writes the primality info into a log file, then checks this file
    to see if today is a prime AND it has not tweeted yet. It tweets if and
    only if in this case.
    '''
    d_str = get_today_str_iso8601()
    logfilepath = get_log_file_path(d_str)

    try:
        os.mkdir(os.path.dirname(logfilepath))
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

    # If log file does not exist, write log file
    if not os.path.isfile(logfilepath):
        write_tweet_str_to_file(d_str)

    # Tweet iff today is a prime day and we have not tweeted today
    (istweeted, isprime, tweet_str) = get_tweet_str_from_file(logfilepath)
    if isprime and not istweeted:
        print('A prime day; not yet tweeted')
        print('Tweeting now...')
        do_tweet(tweet_str)
        mark_logfile_tweeted(logfilepath)
        print('Tweeted!')
    elif not isprime and not istweeted:
        print('A composite day; not yet tweeted')
        print('Tweeting now...')
        do_tweet(tweet_str)
        mark_logfile_tweeted(logfilepath)
        print('Tweeted!')
    else:
        print('Already tweeted today. Check twitter.')
