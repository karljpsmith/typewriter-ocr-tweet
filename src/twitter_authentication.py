from twython import Twython
from random import randint
import pickle


#  Real account: https://twitter.com/10centstories
APP_KEY = '' #get these from your app's page: https://apps.twitter.com/
APP_SECRET = ''

OAUTH_TOKEN = ''
OAUTH_TOKEN_SECRET = ''

oauth_verifier = ''    # get this from following the link at auth_url. Only needed for AuthStep 2

with open('../auth/twitter_keys_PROD.pkl', 'wb') as f:
    pickle.dump([APP_KEY,APP_SECRET,OAUTH_TOKEN,OAUTH_TOKEN_SECRET], f, protocol=2)

scramble = randint(100, 999)  # status updates that are identical to the current status get 403 errors

# There's a multi-step process to getting the proper keys. Follow the guide here:
# https://twython.readthedocs.io/en/latest/usage/starting_out.html#dynamic-function-arguments

AuthStep = 4

if AuthStep == 1:
    twitter = Twython(APP_KEY, APP_SECRET)
    auth = twitter.get_authentication_tokens()
    OAUTH_TOKEN = auth['oauth_token']
    OAUTH_TOKEN_SECRET = auth['oauth_token_secret']
    print(auth['auth_url'])   # update oauth_verifier with the pin at this link
    print(OAUTH_TOKEN)        # update the saved versions with these versions
    print(OAUTH_TOKEN_SECRET)

if AuthStep == 2:
    twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
    final_step = twitter.get_authorized_tokens(oauth_verifier)
    OAUTH_TOKEN = final_step['oauth_token']
    OAUTH_TOKEN_SECRET = final_step['oauth_token_secret']
    print(OAUTH_TOKEN)        # update the saved versions with these versions
    print(OAUTH_TOKEN_SECRET)

if AuthStep == 3:
    twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
    print('Test post, from python random: {}'.format(scramble))
    twitter.update_status(status='Test post, from python random: {}'.format(scramble))
