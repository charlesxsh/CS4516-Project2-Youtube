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

	id_list = []

	# get list of id which prefix is given prefix
	for x in raw_videos_json:
		id_list.append(x["id"]["videoId"])
		#print x["id"]["videoId"]
	
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
def writeToCSV(video_info_file, video_title_file, videos_list):
	with open(video_info_file,"wb") as video_info, open(video_title_file, "wb") as video_title:
		video_info_writer = csv.writer(video_info, delimiter=',')
		video_title_writer = csv.writer(video_title, delimiter= ',')
		info_file_data = [["video id", "video length", "view count", "title length", "description length"]]
		video_file_data = [["video title"]]
		for x in videos_list:
			info_file_data.append([x.videoId, x.titleLength, x.viewCount, x.titleLength, x.descriptionLength])
			video_file_data.append([x.title.encode("UTF-8")])
		video_info_writer.writerows(info_file_data)
		video_title_writer.writerows(video_file_data)
		
def generateRandPrefix(size=3, chars=string.ascii_letters + string.digits + '-' + '_'):
   return ''.join(random.choice(chars) for _ in range(size))


if __name__ == '__main__':
	randPrefix = generateRandPrefix()
	print "RANDOM PREFIX = " + randPrefix
	result = searchVideosByPrefix(randPrefix)
	for x in result:
		printVideosInfo(x)
	
	writeToCSV("video_info.csv","video_title.csv", result)
