import os
import re

import googleapiclient.discovery
import pandas as pd
import xlwt
from urllib.parse import urlparse,parse_qs

from googleapiclient.errors import HttpError

DEVELOPER_KEY = "AIzaSyAPjiYDHl9bgB56vkyUEKxB0l7Fy0MKCxE"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

def buildServiceObject():
    return googleapiclient.discovery.build(
        YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey = DEVELOPER_KEY)

def getVideoId(url):
    return parse_qs(urlparse(url).query).get('v')[0]

def commentsParser(videoID,searchTerm,count,part):

    youtubeObj=buildServiceObject()
    comments, likesCount, authors = [], [], []
    try:
        response = youtubeObj.commentThreads().list(
        part=part,
        maxResults=count,
        searchTerms=searchTerm,
        videoId = videoID,
        textFormat="plainText").execute()
    except HttpError:
        print("HttpError Exception has occurred")
    except TimeoutError:
        print('TimedOut')
    except WindowsError:
        print('System issue')

    while 1==1:
        index=0
        for item in response["items"]:
            index+=1
            comment=item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
            likeCount=item["snippet"]["topLevelComment"]["snippet"]["likeCount"]
            author=item["snippet"]["topLevelComment"]["snippet"]["authorDisplayName"]
            comments.append(comment)
            likesCount.append(likeCount)
            authors.append(author)
        print("Generated {} items successfully".format(index))

        if 'nextPageToken' in response:
            try:
                response = youtubeObj.commentThreads().list(
                part=part,
                maxResults=count,
                searchTerms=searchTerm,
                videoId = videoID,
                pageToken=response["nextPageToken"],
                textFormat="plainText").execute()
            except HttpError:
                print("HttpError Exception has occurred")

        else:
            break

    print('Comments retrieved successfully')
    return dict({'Comments':comments,'Likes':likesCount,'Name':authors})

def getVideoTitle(videoID):
        response=buildServiceObject().videos().list(part = 'snippet',
                                                    id = videoID).execute()
        return response["items"][0]['snippet']['title']

def savetoCsv(comments,filename,searchTerm):
    filename=re.sub('[^A-Z a-z]','',filename,flags = re.I).strip(' ').replace(' ','_')
    df=pd.DataFrame(comments,columns=comments.keys()).sort_values(by='Likes',ascending=False)
    loc=os.path.join('C:\\Users\\anaray01\\Downloads','{}_Keyword=_{}.csv'.format(filename,searchTerm))
    print('Saving to '+loc)
    df.to_csv(loc,index=False,encoding='UTF-8')

def main(url,searchTerm):
    videoId=getVideoId(url)
    print('Go the video url')
    part="snippet"
    dict_comments=commentsParser(videoId,searchTerm,1000,part)
    title=getVideoTitle(videoId)
    savetoCsv(dict_comments,title,searchTerm)
    print('File saved Susseccfully')


if __name__ == "__main__":
    main("https://www.youtube.com/watch?v=UXY2jR-vGA4","hate")