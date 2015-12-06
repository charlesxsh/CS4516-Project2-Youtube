import csv
import sys
import pandas as pd

WordCount = {}

viewCountThreshold = 1

class KeyWord:
	word = ""
	vid = ""
	popularity = 0.0

	def __init__(word, vid):
		self.word = word
		self.vid = vid

	def addPopularity(viewcounts):
		popularity += viewcounts/1000

# class VideoInfo:
# 	vid = ""
# 	viewcounts = 0

# 	def __init__(vid, viewcounts):
# 		self.vid = vid
# 		self.viewcounts = viewcounts

IdToCount = {}

def main(argv):
	with open('/Users/Charles/Downloads/Data/title-set-1.csv') as csvtitlefile, open('/Users/Charles/Downloads/Data/result-set-1.csv') as csvinfofile:
		titlefile = csv.DictReader(csvtitlefile)
		infofile = csv.DictReader(csvinfofile)

		for row in infofile:
			if row['view count'] != 'title length':
				IdToCount[row['video id']] = float(row['view count'])

		for row in titlefile:
			if row['video id'] != 'video id':
				temp = row['video title']
				templist = temp.split()
				vc = IdToCount[row['video id']]/1000
				for x in templist:
					if x.isalpha():
						x = x.lower()
						if x not in WordCount:
							WordCount[x] = vc
						else:
							WordCount[x] += vc

		# for w in sorted(WordCount, key=WordCount.get, reverse=False):
		# 	if WordCount[w] > viewCountThreshold:
		# 		print(w, WordCount[w])
		sorted_list = sorted(WordCount, key=WordCount.get, reverse=True)
		i = 0
		with open("word_statistic.csv","w") as ws:
			ws_writer = csv.writer(ws, delimiter=',')
			tempset = [["word","popularity"]]
			for x in range(1000):
				tempset.append([sorted_list[x], WordCount[sorted_list[x]]])
			ws_writer.writerows(tempset)


if __name__ == "__main__":
	main(sys.argv)