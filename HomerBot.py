import twitter
import urllib2
import re

HOMRUN_GROUP = 2
boxScoreURL = "http://www.cbssports.com/mlb/gametracker/boxscore/MLB_20170705_TOR@NYY/"
api = twitter.Api(consumer_key='skESbPn16O3VfJQFyH33DnrYI',
                      consumer_secret='a3Ke5lhjSA28TmQ3bLaeZGUnyM74EB6kYGdrU7VdTlcZKQiAcY',
                      access_token_key='880951260312068096-oQ5FU0dtyvpGJC4aS2e8TRbDrf0QpRn',
                      access_token_secret='hVmTdkT4aZu4oetLOwE4xwhH06VsTTOaKjeUnvUS2Racz')

#print(api.VerifyCredentials())



#status = api.PostUpdate('Hello, I am the Blue Jays Home Run Bot!')
#print status

rawHTML = urllib2.urlopen(boxScoreURL).read()

## get the home run data for both teams
homerunRegex = re.compile("((.|\n)*)HR: </span\><!-- react-text: 121 -->((.|\n)*)<!-- /react-text --></span></li>(.|\n)*")

result = re.match(homerunRegex, rawHTML)
result = result.groups()

result = result[2]
## narrow down to just toronto

torontoRegex = re.compile("TOR -(.*), \w\w\w -.*")
result = re.match(torontoRegex, result)

result = result.groups()
result = result[0]

result = result.split(",")
print result
