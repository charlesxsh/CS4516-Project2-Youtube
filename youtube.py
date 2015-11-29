#!/usr/bin/python

import httplib2
import os
import sys
from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.file import Storage
from oauth2client.tools import argparser, run_flow
import webbrowser

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

YOUTUBE_READ_WRITE_SCOPE = "https://www.googleapis.com/auth/youtube"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

# basic authenticated request
def get_authenticated_service():
  flow = OAuth2WebServerFlow(client_id='227757159817-le2a2ehp21l59l1dc4thi1b7cp56vadd.apps.googleusercontent.com',
                           client_secret='ptApzyBZZnQuEzioAOK8j3wx',
                           scope=YOUTUBE_READ_WRITE_SCOPE,
                           redirect_uri='http://www.google.com')
  auth_uri = flow.step1_get_authorize_url()
  webbrowser.open(auth_uri)
  code = raw_input("Input your code:")
  credentials = flow.step2_exchange(code)

  return build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
    http=credentials.authorize(httplib2.Http()))

def printVideosInfo(x):
		print 'video title: {0}\nvideo description: {1}\nvideo quality: {2}\nvideo length: {3}'.format(x.title.encode('utf8'), x.description.encode('utf8'), x.videoQuality.encode('utf8'), x.videoLength.encode('utf8'))

# @description search by keyword
# @param:youtube authenticated object <- created by get_authenticated_service()
# @param:keyword keyword used to search 
def searchVideoById(youtube, videoId):
	search_response = youtube.videos().list(id=videoId,part="snippet,contentDetails",maxResults=25).execute()
	videos = []

	for search_result in search_response.get("items", []):
			videoLength = search_result["contentDetails"]["duration"]
			videoQuality = search_result["contentDetails"]["definition"]
			title = search_result["snippet"]["title"]
			description = search_result["snippet"]["description"]
			videos.append(SingleVideo(videoLength, videoQuality, title, description))
  # After loop, print the infomation
  	return videos[0]
	

if __name__ == '__main__':
	youtube = get_authenticated_service()
	# now you can do anything you want
	v = searchVideoById(youtube, "1nzHSkY4K18")
	printVideosInfo(v)



  
