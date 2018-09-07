from twython import Twython
from random import randint
import pickle

#  Test account: https://twitter.com/KarlSmi27061701
#APP_KEY = 'luHRvldqcRWjn6JBXVN6PTCE3' #get these from your app's page: https://apps.twitter.com/
#APP_SECRET = 'x6KPLivvIoXIN178Ci0O3lvobq5cRdGu5dPq5HWOY8HY0T7Qyp'

#OAUTH_TOKEN = '1013096420549713921-K0um6QbXDp3sTuKyUBFZ6yiqYTDOir'
#OAUTH_TOKEN_SECRET = '3tCYypTDhqRcTJTG12WW7P0Ov6j5vDmQTVXr58kG2QmJb'

#oauth_verifier = '6297523'    # get this from following the link at auth_url. Only needed for AuthStep 2


#  Real account: https://twitter.com/10centstories
APP_KEY = 'ZW0JDzaqn05U71gBst4R9kZhi' #get these from your app's page: https://apps.twitter.com/
APP_SECRET = '56LE8DPRt9swyI9aki2XsQFyUesoCagEEpfWqj5upWBnNJuWOP'

OAUTH_TOKEN = '480039358-0sutvgfuix9AnygMgNTVqoIq2Igz4KfurfFgNMFv'
OAUTH_TOKEN_SECRET = 'oGQJsAi5IAZ9nJ5StnjFf6TOXdozN0i7hA807tPHDHDhl'

oauth_verifier = '6559674'    # get this from following the link at auth_url. Only needed for AuthStep 2

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