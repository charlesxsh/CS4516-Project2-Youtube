#!/usr/bin/python

import urllib2
import json
import csv

API_KEY = "AIzaSyD77NJ22EOTmNV9WPjLQqc5wAnIAcxStcE"

def filterIdByStartPrefix(prefix,list_id):
	result = []
	print "Here is case-sensitive result:"

	for i in list_id:
		if i.startswith(prefix):
			result.append(i)
			print i

	return result

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
		print x["id"]["videoId"]
	
	afterFilter_id_list = filterIdByStartPrefix(prefix,id_list)

	videos_list = []

	for i in afterFilter_id_list:
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

def writeToCSV(filename,videos_list):
	with open(filename,"w") as fp:
		csvWriter = csv.writer(fp, delimiter=',')
		data = [["video id", "video length", "view count", "title length", "description length"]];
		for x in videos_list:
			data.append([x.videoId, x.titleLength, x.viewCount, x.titleLength, x.descriptionLength])
		csvWriter.writerows(data)

if __name__ == '__main__':
	result = searchVideosByPrefix("abc")
	for x in result:
		printVideosInfo(x)
	
	writeToCSV("test.csv",result)  
