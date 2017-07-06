import sys

import twitter
import urllib2
import re

## Constants and Global Variables
TEAM_SHORT_NAME = "TOR"
HOMERUN_GROUP = 2
PLAYER_GROUP = 0
homerunData = []

## temporary until I can extract this from the page
boxScoreURL = "http://www.cbssports.com/mlb/gametracker/boxscore/MLB_20170705_TOR@NYY/"

api = twitter.Api(consumer_key='',
                      consumer_secret='',
                      access_token_key='-',
                      access_token_secret='')

try:
	print api.VerifyCredentials()
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
	print twitterMessage
	#status = api.PostUpdate(twitterMessage)


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