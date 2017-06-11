# Developed and modified by Ye Liang at 21:32 June,2 2017
# All rights reserved
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import AgglomerativeClustering
from math import exp
import datetime
import csv
CONST_OUTPUT_CLUSTER_RESULT = True

class Cluster(object):
	# Initialize the cluster module, the TF-IDF is used here for feature extraction.
	def __init__(self):
		self.vectorizer = TfidfVectorizer(stop_words='english')

	def cluster_AP(self, proTweetsList):
		tweetsTextList = []
		# Get only the text part
		for eachTweet in proTweetsList:
			tweetsTextList.append(eachTweet[3])
		# Feature extraction with TF-IDF vectorizer.
		tfidfVec = self.vectorizer.fit_transform(tweetsTextList)
		# Clustering with traditional agglomerative clustering algorithm to ENSURE that the SAME news/tweets will be clustered together.
		model = AgglomerativeClustering(n_clusters = len(proTweetsList) // 5, linkage = 'ward')
		print("clustering...",end="")
		# Turn sparse matrix into a dense array.
		model.fit(tfidfVec.toarray())
		print("Success!")
		# Output the clustering results to a CSV file if needed.
		if(CONST_OUTPUT_CLUSTER_RESULT):
			self.write_Cluster_Result(proTweetsList, model.labels_, 'Raw_Cluster_Result.csv')
		# Find the best of each cluster
		print("Ranking best tweets of each cluster based on their latency and heat...",end="")
		bOfEachC, sortedScores  = self.find_Best_Of_EachC(model.labels_, proTweetsList)
		print("Success!")
		return bOfEachC, model.labels_, sortedScores

	# The method of finding the best of each cluster
	def find_Best_Of_EachC(self, clusterLabels, proTweetsList):
		bestOfEachC = []
		sortedScores = []
		# Initialize bestIndex with invalid index -1 and -Inf score.
		bestIndex = [[-float('inf'), -1] for i in range(len(set(clusterLabels)))]
		# Calculate the score for every tweet according to their TIME ELAPSED and their RETWEET COUNT
		for index, eachTweet in enumerate(proTweetsList):
			score = self.hot_Latency(eachTweet)
			# Update the best score of each cluster.
			if (score > bestIndex[clusterLabels[index]][0]):
				bestIndex[clusterLabels[index]][0] = score
				bestIndex[clusterLabels[index]][1] = index
		# Sort the representatives of clusters by their score.
		sortedBestIndex = sorted(bestIndex, key=lambda x: x[0], reverse=True)
		# Put the best of each cluster in the sorted order. And put their scores in the same order.
		for index in sortedBestIndex:
			bestOfEachC.append(proTweetsList[index[1]])
			sortedScores.append(index[0])
		return bestOfEachC, sortedScores

	# The method that do the calculation of the scores. [THE ONE THAT MAKE ALL THE DIFFERENCE ^_^]
	def hot_Latency(self, tweet):
		# First, we need to get the time latency in seconds, then convert it into the unit of 10 minutes.
		tweetTime = datetime.datetime.strptime(tweet[1], '%Y-%m-%d %H:%M:%S')
		timeElapsed = (datetime.datetime.utcnow() - tweetTime).seconds
		distX = timeElapsed / 600
		# Then, we calculate the RELATIVE HOTNESS using the power function we get from the regression of historical tweets data.
		muHat = -80.91*max(distX, 1)**(-0.8868) + 89.13
		sigmaHat = 83.28*max(distX,0.1)**(0.2045)
		relHotness = (tweet[5] - muHat) / sigmaHat
		# Furthurmore, we need to consider the TIME DECAY EFFECTS for news by multiplying the time decaying equation.
		timeEffect = 1.402 - 1.8*exp(0.01167 * distX -1.5)
		return relHotness * timeEffect

	# displaying clusters if needed
	def write_Cluster_Result(self, proTweetsList, clusterLabels, filename):
		try:
			outtweets = []
			for i, tweet in enumerate(proTweetsList):
				outtweets.append([ tweet[0], tweet[1], tweet[2], tweet[3].encode("ascii","ignore").decode("ascii"), tweet[4], tweet[5], tweet[6], clusterLabels[i]])
			with open(filename, 'w', newline='') as csvfile:
				spamwriter = csv.writer(csvfile)
				spamwriter.writerow(['Tweet ID','Tweet Time','Publisher','Tweet Text','URL','Number of Retweets','Number of Likes','Cluster Number'])
				spamwriter.writerows(outtweets)
			return True
		except:
			print("Fail to open the file, dumping procedure skipped")
			return False

	'''
	def find_Center(self, proTweetsList): deprecated due to center doesn't mean anything here. if we don't have to be political right.

	'''