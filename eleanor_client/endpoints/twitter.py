"""Utility for interacting with eleanor's twitter related endpoints"""
import json
from datetime import datetime

import requests

from eleanor_client.settings import settings


eleanor_url = 'http://{0}:{1}/'.format(
    settings.eleanor_url, settings.eleanor_port
)


def get_tracked_twitter_users():
    """Get all currently tracked twitter users"""
    req_url = '{0}{1}'.format(eleanor_url, 'twitter-tl-users')
    response = requests.get(req_url)
    tracked_users = response.json()['twitter_usernames']
    return tracked_users


def track_new_twitter_user(username):
    """Track a new twitter user in eleanor"""
    req_url = '{0}{1}'.format(eleanor_url, 'twitter-tl-users')
    headers = {'content-type': 'application/json'}
    payload = json.dumps({'twitter_usernames': [username]})
    requests.post(req_url, headers=headers, data=payload)


def add_tweet_data(tweet):
    """Makes a request to eleanor adding tweet (which should be a dictionary
    formatted correctly for the request)"""
    req_url = '{0}{1}'.format(eleanor_url, 'add-tweet-data')
    headers = {'content-type': 'application/json'}
    payload = json.dumps(tweet)
    requests.post(req_url, headers=headers, data=payload)


def get_tweet_data(tweet_id):
    """When given a tweet_id pull the associated tweet data from eleanor, if no
    tweet is found with the given tweet_id returns None
    """
    query_url = 'tweet/{0}'.format(tweet_id)
    req_url = '{0}{1}'.format(eleanor_url, query_url)
    response = requests.get(req_url)
    if response.status_code == 204:
        return None
    else:
        return response.json()


def get_username_last_tweet_id(username):
    """When given a username check for the latest tweet id associated with it
    if there is no tweet id associated with that username returns None
    """
    query_url = 'last-tweet-id/{0}'.format(username)
    req_url = '{0}{1}'.format(eleanor_url, query_url)
    response = requests.get(req_url)
    if response.status_code == 204:
        return None
    else:
        return response.json()['last_tweet_id']


def tweet_search_on_date(username, date, search_term):
    """When given the above search parameters pull tweet search data
    this returns the count of tweets by username on date that includes
    search_term
    """
    req_url = '{0}{1}'.format(eleanor_url, 'stats/tweets-on-date')
    headers = {'content-type': 'application/json'}
    if isinstance(date, datetime):
        date = date.strftime("%Y-%m-%d")
    search_data = {
        'twitter_username': username,
        'search_date': date,
        'search_term': search_term
    }
    payload = json.dumps(search_data)
    response = requests.get(req_url, headers=headers, data=payload)
    if response.status_code == 204:
        return None
    else:
        return response.json()
