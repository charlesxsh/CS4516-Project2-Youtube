#!/usr/bin/python

import urllib2
import json

API_KEY = "AIzaSyD77NJ22EOTmNV9WPjLQqc5wAnIAcxStcE"

# search videos by using given video id prefix
def searchVideosByPrefix(prefix):
	json_result = urllib2.urlopen("https://www.googleapis.com/youtube/v3/search?part=id&q=%22watch?v={0}&type=video&key={1}".format(prefix,API_KEY)).read()
	json_data = json.loads(json_result)
	raw_videos_json = json_data["items"]

	id_list = []

	# get list of id which prefix is given prefix
	for x in raw_videos_json:
		id_list.append(x["id"]["videoId"])
	
	videos_list = []
	for i in id_list:
		videos_list.append(getDetailsById(i))

	return videos_list

# use video id to get more details information about that video
def getDetailsById(vid):
	json_result = urllib2.urlopen("https://www.googleapis.com/youtube/v3/videos?part=snippet%2CcontentDetails&id={0}&key={1}".format(vid,API_KEY)).read()
	json_data = json.loads(json_result)
	video_json = json_data["items"][0]

	videoLength = video_json["contentDetails"]["duration"]
	videoQuality = video_json["contentDetails"]["definition"]
	title = video_json["snippet"]["title"]
	description = video_json["snippet"]["description"]

	return SingleVideo(videoLength, videoQuality, title, description)

# data structure
class SingleVideo(object):
	videoLength = ""
	videoQuality = ""
	titleLength = 0
	title = ""
	description = ""
	descriptionLength = 0
	def __init__(self, videoLength, videoQuality, title, description):
		self.videoLength = videoLength
		self.videoQuality = videoQuality
		self.title = title
		self.description = description
		self.titleLength = len(self.title)
		self.descriptionLength = len(self.description)

# print data structure
def printVideosInfo(x):
		print 'video title: {0}\nvideo description: {1}\nvideo quality: {2}\nvideo length: {3}'.format(x.title.encode('utf8'), x.description.encode('utf8'), x.videoQuality.encode('utf8'), x.videoLength.encode('utf8'))

if __name__ == '__main__':
	result = searchVideosByPrefix("abc")
	for x in result:
		printVideosInfo(x)

  
