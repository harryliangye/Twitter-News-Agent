#Twitter News Agent -- Fetch the best news on twitter with machine learning

##Usage:

To use this program, run: main.py

##Introduction:
This program will download the latest tweets from the twitter of the best 20 English media. Functions including:
1, Download all new tweets and update existing tweets in the past 24 hours every 10 minutes;

2, Once the tweets are updated, store tweet texts and attributes into the SQLite database in the same folder (the program will create a SQLite database by itself);

3, Cluster tweets about the same event;

4, Recognize events that are hot, urgent and worthy to send notification to users, calculate the hot/urgent/worthy score for the tweets in each cluster and sort them.

5, Select the best tweet among each cluster as its representative according to the hot/urgent/worthy score, to avoid duplicate tweets;

6, Output to CSV file with results for every representative of clusters


