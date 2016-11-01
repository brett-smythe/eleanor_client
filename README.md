# Eleanor Client

Client for interacting with [Eleanor](https://github.com/brett-smythe/eleanor) service.

## Install
Recommended to install and run in a virtualenv
The values in eleanor_client/settings/settings.py need to be set for your instance of eleanor

```
python setup.py install
```

### External Dependencies
* Setup and running [Eleanor](https://github.com/brett-smythe/eleanor) service

## Usage

```
from eleanor_client.endpoints import twitter

get_tracked_twitter_users()
>['twitter_uname_1', 'twitter_uname_2']

# This adds a username to eleanor's list of tracked twitter users
track_new_twitter_user('new_username_to_track')
>

get_username_last_tweet_id('last_tweet_for_uname')
>'<last_tweet_id_for_user>'
```
