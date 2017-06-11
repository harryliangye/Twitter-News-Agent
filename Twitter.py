# Developed and modified by Ye Liang at 12:21 June,2 2017
# All rights reserved
import tweepy
import datetime

class Twitter(object):
    # Initialization: Dealing with authetication 'paperworks', having tweepy API repared;
    # Accpeting database object and parser object, which will be used for processing and
    # storing tweets; Setting up the news publisher's screen name on twitter.
    def __init__(self, dbObject, parserObject):
        #User authentication: Ye Liang
        consumer_key=""
        consumer_secret=""
        access_token=""
        access_token_secret=""
        #authorize twitter, initialize tweepy
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        self.parser = parserObject
        self.db = dbObject
        self.api = tweepy.API(auth)
        self.screenNameList = ["nytimes","thesun","thetimes","ap","cnn","bbcnews","cnet","msnuk",\
            "telegraph","wsj","washingtonpost","bostonglobe","newscomauhq","skynews","sfgate",\
            "ajenglish","independent","guardian","latimes","reutersagency"]

    # The method for getting the latest update of the tweets in the past 24 hours.
    def update_All(self):
        allUpdatedTweets = []
        # Update news from every news publisher in the name list.
        for index, screenName in enumerate(self.screenNameList):
            print("Updating {} ...".format(screenName), end = "")
            updated = self.get_New_Tweets(screenName)
            if(len(updated) > 0):
                allUpdatedTweets.extend(updated)
            print("Success!")

        print("{} tweets updated in total".format(len(allUpdatedTweets)))
        # Parse all fetched tweets, and extract the information needed.
        parsedUpdatedTweets = self.parser.parse_All(allUpdatedTweets)
        # Update the tweets information in database, and store new tweets.
        self.db.update_Into_DB(parsedUpdatedTweets)
        return True

    # The method for getting the latest update of the tweets from the given publisher in 24h.
    def get_New_Tweets(self, screenName):
        # initialize a list to hold all the incoming Tweets
        allNewTweets = []
        # make initial request for most recent tweets (200 is the maximum allowed count)
        newTweets = self.api.user_timeline(screen_name = screenName, count=200)
        while (len(newTweets) > 0):
            # save most recent tweets
            allNewTweets.extend(newTweets)
            # save the id of the oldest tweet less one
            newOldestId = newTweets[-1].id - 1
            # Have no more than 200 new tweets, or go beyond 24 hours.
            if (len(newTweets) < 200 or (datetime.datetime.utcnow() - newTweets[-1].created_at).days > 0):
                break
            else:
                # more than one bags
                newTweets = self.api.user_timeline(screen_name = screenName, count=200, max_id = newOldestId)
        return allNewTweets


    

    
