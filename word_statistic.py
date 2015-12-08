import csv
import sys
import pandas as pd

# PT H M S
def parseTimeStrToSecond(str):
	totalTime = 0
	temp = str[2:] # get rid of PT

	tempIndexH = temp.find('H')
	tempIndexM = temp.find('M')
	tempIndexS = temp.find('S')

	if tempIndexH != -1:
		totalTime += int(temp[:tempIndexH])*3600
	else:
		tempIndexH = 0

	if tempIndexM != -1:
		if tempIndexH == 0:
			totalTime += int(temp[:tempIndexM])*60
		else:
			totalTime += int(temp[tempIndexH+1:tempIndexM])*60
	else:
		tempIndexM = 0

	if tempIndexS != -1:
		if tempIndexM == 0:
			if tempIndexH == 0:
				totalTime += int(temp[:tempIndexS])
			else:
				totalTime += int(temp[tempIndexH+1:tempIndexS])
		else:
			totalTime += int(temp[tempIndexM+1:tempIndexS])
			
	return totalTime

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