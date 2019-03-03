from twython import Twython
import pickle

# There's a multi-step process to getting the proper keys in twitter_authentication.py

max_tweet_length = 280  # characters
FLAG_TWEET_FROM_TEST_ACCOUNT = False
#  Test account: https://twitter.com/KarlSmi27061701
#  Real account: https://twitter.com/10centstories


# NOTE: If you're running this on boot via cron, the path begins "../auth/"
# But if you're running it with python3 on the pi (i.e. debugging) the path beginning is "auth/"
def get_saved_credentials():
    if (FLAG_TWEET_FROM_TEST_ACCOUNT):
        with open('../auth/twitter_keys.pkl', 'rb') as f:
            return pickle.load(f)
    with open('../auth/twitter_keys_PROD.pkl', 'rb') as f:
        return pickle.load(f)


def tweet_with_image(status_text :str, image_filepath :str):
    [APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET] = get_saved_credentials()
    twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
    image_open = open(image_filepath, 'rb')
    image_ids = twitter.upload_media(media=image_open)
    twitter.update_status(status=status_text, media_ids=image_ids['media_id'])


def tweet(status_text: str):
    [APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET] = get_saved_credentials()
    twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
    twitter.update_status(status=status_text)
