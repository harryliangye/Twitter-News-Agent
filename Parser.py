# Developed and modified by Ye Liang at 20:10 June,2 2017
# All rights reserved
import re
import string
import math
class Parser(object):
	# The method that formats tweets list
	def parse_All(self, tweetList):
		parsedTweetsList = []
		for eachTweet in tweetList:
			parsedTweetsList.append(self.parse_Tweet(eachTweet))
		return parsedTweetsList
	# The method that formats a single tweet
	
	def parse_Tweet(self, tweet):
		tweetId = tweet.id
		createdAt = tweet.created_at
		tweetText = self.clean_Tweet(tweet.text)
		publisher = tweet.user.screen_name
		numOfRetweet = tweet.retweet_count 
		numOfLikes = tweet.favorite_count
		# If the tweet contains a formal URL then keep the URL.
		if(len(tweet.entities['urls']) > 0):
			url = tweet.entities['urls'][0]['url']
		else:
			url = "NULL"
		# Return the information we are going to get from each tweet.
		return [tweetId, createdAt, publisher, tweetText, url, numOfRetweet, numOfLikes]

	def clean_Tweet(self, tweetText):
	#-------------remove Url from test--------
		caseUrl = re.match(re.compile("(.*?)http(.*?)$",re.IGNORECASE), tweetText)#group(1)
		if (caseUrl):
			tweetText = caseUrl.group(1)
	#-------------remove RT @Sb:--------------
		caseRt = re.match(re.compile("RT\s@(.*?):\s(.*?)$",re.IGNORECASE), tweetText)#group(2)
		if (caseRt):
			tweetText = caseRt.group(2)
	#-------------remove @Sb:-----------------
		caseAt = re.match(re.compile("@(.*?)\s(.*?)$",re.IGNORECASE), tweetText)#group(2)
		if (caseAt):
			tweetText = caseAt.group(2)
		return tweetText
