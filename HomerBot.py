import sys

import twitter
import urllib2
import re
import time

## Constants and Global Variables
TEAM_NAME = "Toronto Blue Jays"
TEAM_NAME_SHORT = "Blue Jays"
HOMERUN_GROUP = 1
PLAYER_GROUP = 0
WEBSITE_URL_BASE = "http://www.espn.com/mlb/boxscore?gameId="
HOMERUN_CALL_FILE = "callSheet.txt"

homerunData = []
checkNumber = 0

api = twitter.Api(consumer_key='skESbPn16O3VfJQFyH33DnrYI',
                      consumer_secret='a3Ke5lhjSA28TmQ3bLaeZGUnyM74EB6kYGdrU7VdTlcZKQiAcY',
                      access_token_key='880951260312068096-oQ5FU0dtyvpGJC4aS2e8TRbDrf0QpRn',
                      access_token_secret='hVmTdkT4aZu4oetLOwE4xwhH06VsTTOaKjeUnvUS2Racz')

try:
	api.VerifyCredentials()
except:
	print "Could Not Connect to Twitter, Exiting Program"
	sys.exit()

def getHomeRunCallText(file):
	pass

def postHomeRunToTwitter(playerData):
	playerDataRegex = re.compile('^.*?(\w+ \w+) \((\d+).*$')

	result = re.match(playerDataRegex, playerData)
	result = result.groups()

	playerName = result[0]
	playerHomerCount = result[1]

	twitterMessage = "Home Run for " + playerName + " his " + playerHomerCount + "th of the season!"
	print api.PostUpdate(twitterMessage)

def getBoxScoreURL(url):
	# get the HTML text from the input url
	rawHTML = urllib2.urlopen(url).read()

	# whittle down the HTML text
	boxScoreRegex = '(.|\n)*displayName\":\"' + TEAM_NAME + '(.|\n)*?gameId=([0-9]*?)"(.|\n).*'
	boxScoreRegex = re.compile(boxScoreRegex)
	boxScoreRegex = re.match(boxScoreRegex, rawHTML)
	urlText = boxScoreRegex.group(3)

	print "GAME URL FOUND AT: " + WEBSITE_URL_BASE + urlText
	return WEBSITE_URL_BASE + urlText


scoresHomePage = "http://www.espn.com/mlb/scoreboard"
boxScoreURL = getBoxScoreURL(scoresHomePage)

## get the home run data for both teams (want to pair this expression down)
homerunRegex = "(.|\n)*" + TEAM_NAME + ".*?BATTING.*?HR:.*?>(.*?)<(.|\n)*"
homerunRegex = re.compile(homerunRegex)

while (True):
	rawHTML = urllib2.urlopen(boxScoreURL).read()

	result = re.match(homerunRegex, rawHTML)

	if result != None:	
		result = result.groups()
		homeRunText = result[HOMERUN_GROUP]

		homeRunText = homeRunText.split(';')
		for homeRun in homeRunText:
			if homeRun not in homerunData:
				print homeRun
				homerunData.append(homeRun)
				postHomeRunToTwitter(homeRun)

	print "Check Number: " + str(checkNumber) + "\nRe-check in 5 Minutes"
	checkNumber += 1

	time.sleep(300)