"""Tests for eleanor client twitter endpoint"""
# pylint: disable=import-error
import unittest
import json

from datetime import datetime

import mock

from eleanor_client.endpoints import twitter


class TwitterEndpointCase(unittest.TestCase):
    """Eleanor client twitter endpoint test class"""
    # pylint: disable=too-many-public-methods
    json_headers = {'content-type': 'application/json'}
    tl_users_url = '{0}{1}'.format(
        twitter.eleanor_url, twitter.tl_users_endpoint
    )

    @mock.patch('eleanor_client.endpoints.twitter.requests')
    def test_get_tracked_twitter_users(self, mock_requests):
        """Test gettting tracked twitter users from eleanor"""
        # pylint: disable=no-self-use
        twitter.get_tracked_twitter_users()

        mock_requests.get.assert_called_with(self.tl_users_url)

    @mock.patch('eleanor_client.endpoints.twitter.requests')
    def test_track_new_twitter_user(self, mock_requests):
        """Test adding a new tracked twitter user to eleanor"""
        # pylint: disable=no-self-use
        test_uname = 'TestUsername'
        twitter.track_new_twitter_user(test_uname)

        payload = json.dumps({'twitter_usernames': [test_uname]})
        mock_requests.post.assert_called_with(
            self.tl_users_url, headers=self.json_headers, data=payload
        )

    @mock.patch('eleanor_client.endpoints.twitter.requests')
    def test_add_tweet_data(self, mock_requests):
        """Test adding tweet data to eleanor"""
        # pylint: disable=no-self-use
        tweet_data = {'some': 'fake tweet data'}
        twitter.add_tweet_data(tweet_data)

        req_url = '{0}{1}'.format(twitter.eleanor_url, 'add-tweet-data')
        payload = json.dumps(tweet_data)
        mock_requests.post.assert_called_with(
            req_url, headers=self.json_headers, data=payload
        )

    @mock.patch('eleanor_client.endpoints.twitter.requests')
    def test_get_tweet_data_no_data(self, mock_requests):
        """Test getting tweet data from eleanor with no existing tweet data"""
        class MockResponse(object):
            """Mock return object for requests get"""

            def __init__(self, status_code):
                self.status_code = status_code

        tweet_id = '10'
        mock_requests.get.return_value = MockResponse(204)
        self.assertEqual(twitter.get_tweet_data(tweet_id), None)

        query_url = 'tweet/{0}'.format(tweet_id)
        req_url = '{0}{1}'.format(twitter.eleanor_url, query_url)
        mock_requests.get.assert_called_with(req_url)

    @mock.patch('eleanor_client.endpoints.twitter.requests')
    def test_get_tweet_data_has_tweet_data(self, mock_requests):
        """Test getting tweet data from eleanor when tweet data exists"""
        class MockResponse(object):
            """Mock return object for requests get"""

            def __init__(self, status_code):
                self.status_code = status_code

            def json(self):
                """Return false json data"""
                # pylint: disable=no-self-use
                return 'json data'

        tweet_id = '10'
        mock_requests.get.return_value = MockResponse(200)
        self.assertEqual(twitter.get_tweet_data(tweet_id), 'json data')

        query_url = 'tweet/{0}'.format(tweet_id)
        req_url = '{0}{1}'.format(twitter.eleanor_url, query_url)
        mock_requests.get.assert_called_with(req_url)

    @mock.patch('eleanor_client.endpoints.twitter.requests')
    def test_get_username_last_tweet_id_no_last_tweet(self, mock_requests):
        """Test getting last tweet id for a twitter user when no last tweet id
        exists"""
        class MockResponse(object):
            """Mock return object for requests get"""

            def __init__(self, status_code):
                self.status_code = status_code

            def json(self):
                """Return false json data"""
                # pylint: disable=no-self-use
                return {'last_tweet_id': 42}

        test_uname = 'MalcomReynolds'
        mock_requests.get.return_value = MockResponse(204)
        self.assertEqual(
            twitter.get_username_last_tweet_id(test_uname), None
        )

        query_url = 'last-tweet-id/{0}'.format(test_uname)
        req_url = '{0}{1}'.format(twitter.eleanor_url, query_url)
        mock_requests.get.assert_called_with(req_url)

    @mock.patch('eleanor_client.endpoints.twitter.requests')
    def test_get_username_last_tweet_id_with_last_tweet(self, mock_requests):
        """Test getting last tweet id for a twitter user when no last tweet id
        exists"""
        class MockResponse(object):
            """Mock return object for requests get"""

            def __init__(self, status_code):
                self.status_code = status_code

            def json(self):
                """Return false json data"""
                # pylint: disable=no-self-use
                return {'last_tweet_id': 42}

        test_uname = 'MalcomReynolds'
        mock_requests.get.return_value = MockResponse(200)
        self.assertEqual(
            twitter.get_username_last_tweet_id(test_uname), 42
        )

        query_url = 'last-tweet-id/{0}'.format(test_uname)
        req_url = '{0}{1}'.format(twitter.eleanor_url, query_url)
        mock_requests.get.assert_called_with(req_url)

    @mock.patch('eleanor_client.endpoints.twitter.requests')
    def test_get_tweet_search_on_data_no_data(self, mock_requests):
        """Test getting tweet data from eleanor with no data found"""
        class MockResponse(object):
            """Mock return object for requests get"""

            def __init__(self, status_code):
                self.status_code = status_code

            def json(self):
                """Return false json data"""
                # pylint: disable=no-self-use
                return 'json data'

        test_uname = 'MalcomReynolds'
        search_date = datetime(year=2016, month=01, day=01).strftime(
            '%Y-%m-%d'
        )
        search_term = 'Miranda'
        search_data = {
            'twitter_username': test_uname,
            'search_date': search_date,
            'search_term': search_term
        }
        mock_requests.post.return_value = MockResponse(204)
        self.assertEqual(
            twitter.tweet_search_on_date(
                test_uname, search_date, search_term
            ),
            None
        )
        req_url = '{0}{1}'.format(twitter.eleanor_url, 'stats/tweets-on-date')
        payload = json.dumps(search_data)
        mock_requests.post.assert_called_with(
            req_url, headers=self.json_headers, data=payload
        )

    @mock.patch('eleanor_client.endpoints.twitter.requests')
    def test_get_tweet_search_on_data_has_data(self, mock_requests):
        """Test getting tweet data from eleanor with no data found"""
        class MockResponse(object):
            """Mock return object for requests get"""

            def __init__(self, status_code):
                self.status_code = status_code

            def json(self):
                """Return false json data"""
                # pylint: disable=no-self-use
                return 'json data'

        test_uname = 'MalcomReynolds'
        search_date = datetime(year=2016, month=01, day=01).strftime(
            '%Y-%m-%d'
        )
        search_term = 'Miranda'
        search_data = {
            'twitter_username': test_uname,
            'search_date': search_date,
            'search_term': search_term
        }
        mock_requests.post.return_value = MockResponse(200)
        self.assertEqual(
            twitter.tweet_search_on_date(
                test_uname, search_date, search_term
            ),
            'json data'
        )
        req_url = '{0}{1}'.format(twitter.eleanor_url, 'stats/tweets-on-date')
        payload = json.dumps(search_data)
        mock_requests.post.assert_called_with(
            req_url, headers=self.json_headers, data=payload
        )
