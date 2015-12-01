#!/usr/bin/python

import urllib2
import json
import csv
import string
import random

API_KEY = "AIzaSyD77NJ22EOTmNV9WPjLQqc5wAnIAcxStcE"

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

	videos_list = []

	for i in id_list:
		videos_list.append(getDetailsById(i))

	return videos_list

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

# Writes video information to a csv file and video titles to a separate csv file
def writeToCSV(randPrefix, videos_list):
	with open("video_info_file.csv","a") as video_info, open("video_title_file.csv", "a") as video_title, open("randPrefix.csv", "a") as prefix:
		video_info_writer = csv.writer(video_info, delimiter=',')
		video_title_writer = csv.writer(video_title, delimiter= ',')
		prefix_writer = csv.writer(prefix, delimiter= ',')
		
		#info_file_data = [["video id", "video length", "view count", "title length", "description length"]]
		#video_file_data = [["video title"]]
		#prefix_file_data = [["prefix"]]		
		
		info_file_data = [[]]
		video_file_data = [[]]
		prefix_file_data = [[]]
		
		for x in videos_list:
			info_file_data.append([x.videoId, x.titleLength, x.videoQuality, x.viewCount, x.titleLength, x.descriptionLength])
			video_file_data.append([x.title.encode("UTF-8")])
			prefix_file_data.append([randPrefix])
			
		video_info_writer.writerows(info_file_data)
		video_title_writer.writerows(video_file_data)
		prefix_writer.writerows(prefix_file_data)

def generateRandPrefix(size=3, chars=string.ascii_letters + string.digits + '-' + '_'):
   return ''.join(random.choice(chars) for _ in range(size))
	

if __name__ == '__main__':
	prefixSet = set()

	for i in range(0,2):
		randPrefix = generateRandPrefix()
		prefixSet.add(randPrefix)
		result = searchVideosByPrefix(randPrefix)
		writeToCSV(randPrefix, result)
		
	
	