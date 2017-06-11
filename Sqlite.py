# Developed and modified by Ye Liang at 15:37 June,2 2017
# All rights reserved
import sqlite3

class Sqlite(object):
	# Initialize the database module, creat a SQLite database if not exists,
	# create the table for storing news if not exists; Get connection and
	# cursor ready to use.
	def __init__(self, dbName):
		self.__conn = sqlite3.connect(dbName)
		self.__c = self.__conn.cursor()
		self.__c.execute('''CREATE TABLE IF NOT EXISTS news (tweetId integer primary key, date text, publisher text, tweetText text, tweetUrl text, nRetweets integer, nLikes integer)''')
		self.__conn.commit()

	# The method of updating tweets in the database.
	def update_Into_DB(self, cleanedTweets):
		self.__c.executemany('''REPLACE INTO news (tweetId, date, publisher, tweetText, tweetUrl, nRetweets, nLikes) VALUES (?, ?, ?, ?, ?, ?, ?)''', cleanedTweets)
		self.__conn.commit()

	# The method of getting stored news from the database from a given period of time.
	def get_stored_news(self, daysElapsed):
		results = []
		self.__c.execute('''SELECT * FROM news WHERE julianday("now") - julianday(date) < ?''', (daysElapsed,))
		for item in self.__c.fetchall():
			results.append([item[0], item[1], item[2], item[3], item[4], item[5], item[6]])
		return results

	# The method of closing connection.
	def close(self):
		self.__conn.close()

