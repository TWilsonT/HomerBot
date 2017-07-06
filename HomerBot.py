import sys

import twitter
import urllib2
import re
import time

## Constants and Global Variables
TEAM_SHORT_NAME = "TOR"
TEAM_NAME = "Blue Jays"
HOMERUN_GROUP = 2
PLAYER_GROUP = 0
homerunData = []
WEBSITE_URL_BASE = "http://www.cbssports.com/"

api = twitter.Api(consumer_key='skESbPn16O3VfJQFyH33DnrYI',
                      consumer_secret='a3Ke5lhjSA28TmQ3bLaeZGUnyM74EB6kYGdrU7VdTlcZKQiAcY',
                      access_token_key='880951260312068096-oQ5FU0dtyvpGJC4aS2e8TRbDrf0QpRn',
                      access_token_secret='hVmTdkT4aZu4oetLOwE4xwhH06VsTTOaKjeUnvUS2Racz')

try:
	api.VerifyCredentials()
except:
	print "Could Not Connect to Twitter, Exiting Program"
	sys.exit()

def postHomeRunToTwitter(playerData):
	playerDataRegex = re.compile('^(\w+\. \w*) \((\d+)\)*$')

	result = re.match(playerDataRegex, playerData)
	result = result.groups()

	playerName = result[0]
	playerHomerCount = result[1]

	twitterMessage = "Home Run for " + playerName + " his " + playerHomerCount + "th of the season!"
	status = api.PostUpdate(twitterMessage)
	print status

def getBoxScoreURL(url):
	# get the HTML text from the input url
	rawHTML = urllib2.urlopen(url).read()

	# whittle down the HTML text
	boxScoreRegex = re.compile('(.|\n)*Blue Jays(.|\n)*?\<a class="" href="/((.|\n)*?)Box Score(.|\n)*')
	boxScoreRegex = re.match(boxScoreRegex, rawHTML)
	urlText = boxScoreRegex.group(3)

	# pull out the final URL
	boxScoreRegex = re.compile('(.*?)".*')
	urlText = re.match(boxScoreRegex, urlText)
	urlText = urlText.group(1)

	print WEBSITE_URL_BASE + urlText


scoresHomePage = "http://www.cbssports.com/mlb/scoreboard/"
boxScoreURL = getBoxScoreURL(scoresHomePage)

while (False):
	rawHTML = urllib2.urlopen(boxScoreURL).read()

	## get the home run data for both teams (want to pair this expression down)
	homerunRegex = re.compile("((.|\n)*)HR: </span\><!-- react-text: 121 -->((.|\n)*)<!-- /react-text --></span></li>(.|\n)*")

	result = re.match(homerunRegex, rawHTML)
	result = result.groups()

	homeRunText = result[HOMERUN_GROUP]

	## narrow down to just the team we care about
	# create the regular expression
	teamNameRegex = TEAM_SHORT_NAME + " -(.*), \w\w\w -.*"
	teamNameRegex = re.compile(teamNameRegex)

	# extract the home run info
	result = re.match(teamNameRegex, homeRunText)
	result = result.groups()
	playerText = result[PLAYER_GROUP]

	# get the individual player data
	playerData = playerText.split(",")
	for player in range(0, len(playerData)):
		playerData[player] = playerData[player].strip()
		if playerData[player] not in homerunData:
			postHomeRunToTwitter(playerData[player])
			homerunData.append(playerData[player])

	time.sleep(300)
