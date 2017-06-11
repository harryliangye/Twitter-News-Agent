# Developed and modified by Ye Liang at 11:11 June,3 2017
# All rights reserved
from ExtraTools import write_To_Csv, sleep_Module
import Twitter
import Sqlite
import Parser
import Cluster
CONST_DAYS_INCLUDED = 1


if __name__ == '__main__':
    #----------initialize the modules and settings---------------------begin
    db = Sqlite.Sqlite("database.db")
    parserModule = Parser.Parser()
    clusterModule = Cluster.Cluster()
    twitterModule = Twitter.Twitter(db, parserModule)
    #----------initialize the modules and settings---------------------end

    runSequence = True
    while(runSequence):
        # update all tweets into the database within CONST_DAYS_INCLUDED day
        twitterModule.update_All()
        # get all updated tweets within CONST_DAYS_INCLUDED day
        news24H = db.get_stored_news(CONST_DAYS_INCLUDED)
        # cluster, and find the best news
        sortedNews, labels, sortedScores = clusterModule.cluster_AP(news24H)
        # write to csv file
        write_To_Csv(sortedNews, sortedScores, 'Sorted_Best_Tweets (one for each cluster).csv')
        # sleeping procedure
        runSequence = sleep_Module(600)
    db.close()

