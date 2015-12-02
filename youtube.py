#!/usr/bin/python

import urllib2
import json
import csv
import string
import random
import threading
from collections import deque

API_KEY = "AIzaSyD77NJ22EOTmNV9WPjLQqc5wAnIAcxStcE"
##### Thread Test
SingleVideo_list = []
mutex = threading.Lock()
workQueue = deque() 
rows = 0
file_index = 0

def t_getDetailsById(vid):
	global rows
	global mutex
	json_result = urllib2.urlopen("https://www.googleapis.com/youtube/v3/videos?part=snippet%2CcontentDetails%2Cstatistics&id={0}&key={1}".format(vid,API_KEY)).read()
	json_data = json.loads(json_result)
	video_json = json_data["items"][0]
	videoLength = video_json["contentDetails"]["duration"]
	videoQuality = video_json["contentDetails"]["definition"]
	title = video_json["snippet"]["title"]
	description = video_json["snippet"]["description"]
	viewCount = video_json["statistics"]["viewCount"]
	mutex.acquire()
	SingleVideo_list.append(SingleVideo(vid,videoLength, videoQuality, title, description, viewCount))
	rows += 1
	mutex.release()

class TgetDetailsById(threading.Thread):
    def __init__(self, vid):
        threading.Thread.__init__(self)
        self.vid = vid
    def run(self):
        t_getDetailsById(self.vid)
        #print "get {0} success".format(self.vid)

# id_list youtube video id list
# SingleVideo_list holds every videos details
def getAllDetails(id_list):
	global workQueue
	SingleVideo_list = []
	for vid in id_list:
		if len(workQueue) >= 50:
			workQueue.popleft().join()
		t = TgetDetailsById(vid)
		t.start()
		workQueue.append(t)

	for x in workQueue:
		x.join()
	workQueue.clear()
# search videos by using given video id prefix
def searchVideosByPrefix(prefix):
	# q="watch?v=abc"
	json_result = urllib2.urlopen("https://www.googleapis.com/youtube/v3/search?part=id&q=%22watch%3Fv%3D{0}%22&type=video&key={1}&maxResults=50&videoCategoryId=25".format(prefix,API_KEY)).read()
	json_data = json.loads(json_result)
	raw_videos_json = json_data["items"]

	#Get the next page if there is one
	try:
		nextPageToken = json_data["nextPageToken"]
	except:
		nextPageToken = None

	id_list = []

	# get list of id which prefix is given prefix
	for x in raw_videos_json:
		id_list.append(x["id"]["videoId"])
		#print x["id"]["videoId"]

	#While there are additional pages to search...
	while (nextPageToken is not None):
		json_result = urllib2.urlopen("https://www.googleapis.com/youtube/v3/search?part=id&q=%22watch%3Fv%3D{0}%22&type=video&key={1}&maxResults=50&videoCategoryId=25&pageToken={2}".format(prefix,API_KEY, nextPageToken)).read()
		json_data = json.loads(json_result)
		raw_videos_json = json_data["items"]
		try:
			nextPageToken = json_data["nextPageToken"]
		except:
			nextPageToken = None

		for x in raw_videos_json:
			# Check for duplicates. API can return duplicates per page if the estimated
			# results are too far off.
			if (x["id"]["videoId"] not in id_list):
				id_list.append(x["id"]["videoId"])
				#print x["id"]["videoId"]

	print "Expected Results: {0}".format(json_data["pageInfo"]["totalResults"])
	print "Actual Results: {0}".format(len(id_list));
	print "\n\n"

	#videos_list = []

	#for i in id_list:
	# 	videos_list.append(getDetailsById(i))
	getAllDetails(id_list)
	# result is in global variable SingleVideo_list
	#return videos_list

# use video id to get more details information about that video
def getDetailsById(vid):
	json_result = urllib2.urlopen("https://www.googleapis.com/youtube/v3/videos?part=snippet%2CcontentDetails%2Cstatistics&id={0}&key={1}".format(vid,API_KEY)).read()
	json_data = json.loads(json_result)
	video_json = json_data["items"][0]

	videoLength = video_json["contentDetails"]["duration"]
	videoQuality = video_json["contentDetails"]["definition"]
	title = video_json["snippet"]["title"]
	description = video_json["snippet"]["description"]
	viewCount = video_json["statistics"]["viewCount"]
	return SingleVideo(vid,videoLength, videoQuality, title, description, viewCount)

# data structure
class SingleVideo(object):
	videoId = ""
	videoLength = ""
	videoQuality = ""
	titleLength = 0
	title = ""
	description = ""
	descriptionLength = 0
	viewCount = 0
	def __init__(self,videoId, videoLength, videoQuality, title, description, viewCount):
		self.videoId = videoId
		self.videoLength = videoLength
		self.videoQuality = videoQuality
		self.title = title
		self.description = description
		self.titleLength = len(self.title)
		self.descriptionLength = len(self.description)
		self.viewCount = viewCount

# print data structure
# @parameter x SingleVideo

def printVideosInfo(x):
		#print 'video title: {0}\nvideo description: {1}\nvideo quality: {2}\nvideo length: {3}'.format(x.title.encode('utf8'), x.description.encode('utf8'), x.videoQuality.encode('utf8'), x.videoLength.encode('utf8'))
		print 'video length:{0} view count:{1} title length:{2} description length:{3}'.format(x.videoLength, x.viewCount, x.titleLength, x.descriptionLength)

def writeToCSV(video_info_file_name,video_title_file_name, videos_list):

	with open(video_info_file_name,"a") as video_info, open(video_title_file_name, "a") as video_title:
		video_info_writer = csv.writer(video_info, delimiter=',')
		video_title_writer = csv.writer(video_title, delimiter= ',')
		
		#info_file_data = [["video id", "video length", "view count", "title length", "description length"]]
		#video_file_data = [["video title"]]
		#prefix_file_data = [["prefix"]]		
		
		info_file_data = [["video id", "video length", "view count", "title length", "description length"]]
		video_file_data = [["video id", "video title"]]
		
		for x in videos_list:
			info_file_data.append([x.videoId, x.videoLength, x.videoQuality, x.viewCount, x.titleLength, x.descriptionLength])
			video_file_data.append([x.videoId, x.title.encode("UTF-8")])
			
		video_info_writer.writerows(info_file_data)
		video_title_writer.writerows(video_file_data)

def generateRandPrefix(size=3, chars=string.ascii_lowercase + string.digits + '-' + '_'):
   return ''.join(random.choice(chars) for _ in range(size))
	


if __name__ == '__main__':
	global rows
	global file_index
	video_info_file_name = ""
	video_title_file_name = ""
	prefix = open("randPrefix.csv", "a+")
	prefix_list = prefix.read().split(",")
	prefix_list.pop()
	prefixSet = set()
	print prefix_list

	video_info_file_name = "video_info_file_{0}.csv".format(file_index)
	video_title_file_name = "video_title_file_{0}.csv".format(file_index)

	for i in range(0,1000):
		randPrefix = generateRandPrefix()
		if(randPrefix not in prefix_list):
			prefix.write(randPrefix + ",")
			prefixSet.add(randPrefix)
			#result = searchVideosByPrefix(randPrefix)
			#writeToCSV(randPrefix, result)
			searchVideosByPrefix(randPrefix)
			writeToCSV(video_info_file_name,video_title_file_name, SingleVideo_list)
			del SingleVideo_list[:]
			if rows > 1000000:
				video_info_file_name = "video_info_file_{0}.csv".format(file_index)
				video_title_file_name = "video_title_file_{0}.csv".format(file_index)
				file_index += 1
				rows = 0

		else:
			i-=1


	