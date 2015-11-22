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

# @description search by keyword
# @param:youtube authenticated object <- created by get_authenticated_service()
# @param:keyword keyword used to search 
def searchByKeyword(youtube, keyword):
  search_response = youtube.search().list(q="wpi",part="id,snippet",maxResults=25).execute()

  videos = []
  channels = []
  playlists = []

  # Add each result to the appropriate list, and then display the lists of
  # matching videos, channels, and playlists.
  for search_result in search_response.get("items", []):
    if search_result["id"]["kind"] == "youtube#video":
      videos.append("%s (%s)" % (search_result["snippet"]["title"],
                                 search_result["id"]["videoId"]))
    elif search_result["id"]["kind"] == "youtube#channel":
      channels.append("%s (%s)" % (search_result["snippet"]["title"],
                                   search_result["id"]["channelId"]))
    elif search_result["id"]["kind"] == "youtube#playlist":
      playlists.append("%s (%s)" % (search_result["snippet"]["title"],
                                    search_result["id"]["playlistId"]))

  print "Videos:\n", "\n".join(videos), "\n"
  print "Channels:\n", "\n".join(channels), "\n"
  print "Playlists:\n", "\n".join(playlists), "\n"


if __name__ == '__main__':
  youtube = get_authenticated_service()
	# now you can do anything you want

  searchByKeyword(youtube, "wpi")



  