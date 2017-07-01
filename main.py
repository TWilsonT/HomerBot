import twitter

api = twitter.Api(consumer_key='',
                      consumer_secret='',
                      access_token_key='',
                      access_token_secret='')

print(api.VerifyCredentials())
print "fart"

status = api.PostUpdate('Hello, I am the Blue Jays Home Run Bot!')
print status