# Developed and modified by Ye Liang at 11:11 June,3 2017
# All rights reserved
import csv
from time import sleep

# The method that write the latest results into a csv file
def write_To_Csv(sortedNews, sortedScores, filename):
    outSortedNews = []
    for i, tweet in enumerate(sortedNews):
        # encode and decode text with ASCII to clean up non-ascii charactors
        outSortedNews.append([tweet[0], tweet[1], tweet[2], tweet[3].encode("ascii","ignore").decode("ascii"), tweet[4], tweet[5], tweet[6], sortedScores[i]])
    try:
        with open(filename, 'w', newline='') as csvfile:
            spamwriter = csv.writer(csvfile)
            spamwriter.writerow(['Tweet ID','Tweet Time (UTC)','Publisher','Tweet Text','URL','Number of Retweet','Number of Likes', 'Score'])
            spamwriter.writerows(outSortedNews)
        print ("Results have been successfully dumped in {}'\n".format(filename))
    except:
        print("Fail to open file, dumping procedure skipped")
        pass
    return True
    
# The method that make the service wait and restart every X minutes, X is the user assigned sleeping time in seconds.
def sleep_Module(sleepSeconds):
    for i in range(sleepSeconds):
        sleep(1)
        if (i % 10 == 0):
            print ("The sequence will restart in {} minutes and {} seconds".format((sleepSeconds - i) // 60, (sleepSeconds - i) % 60))
    print("Restarting the updating sequence......")
    return True