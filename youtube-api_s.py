import json
from decouple import config , Csv
import argparse
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import threading
import urllib.request


DEVELOPER_KEY = config('DEVELOPER_KEY' , cast=Csv())
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'

def download_image(url, file_name):
    urllib.request.urlretrieve(url, file_name)

def youtube_search(options):
  youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
    developerKey=DEVELOPER_KEY)

  # Call the search.list method to retrieve results matching the specified
  # query term.
  search_response = youtube.search().list(
    q=options.q,
    part='id,snippet',
    type='video',
    order = 'date',
    pageToken=None,
    maxResults=options.max_results
  ).execute()

  # videos = []
  # # print(search_response.get('items', []))
  # search_items = search_response.get('items', [])
  # # json_data = json.loads(items[0])
  # images = []
  
  # for item in search_items:
  #   for thumbnails in item['snippet']['thumbnails'].values():
  #     images.append(thumbnails)
  # threads = []
  # for image in images:
  #   download_image(image['url'], image['url'].split('/')[-1])
 

  # for thread in threads:
  #   thread.start()
  # for thread in threads:
  #   thread.join()

  

  # high_thumbnail = items[0]['snippet']['thumbnails']['high']['url']
  # default_thumbnail = items[0]['snippet']['thumbnails']['default']['url']
  # standard_thumbnail = items[0]['snippet']['thumbnails']['standard']['url']
  # maxres_thumbnail = items[0]['snippet']['thumbnails']['maxres']['url']
  # medium_thumnail = items[0]['snippet']['thumbnails']['medium']['url']




    # download_image(search_response.get('items', [])[0]['snippet']['thumbnails']['high']['url'], 'test.jpg')

  # Add each result to the appropriate list, and then display the lists of
  # matching videos, channels, and playlists.
  # for search_result in search_response.get('items', []):
  #     videos.append('%s (%s) thumbnails (%s) ' % (search_result['snippet']['title'],
  #                                   search_result['id']['videoId'] , search_result['snippet']['thumbnails']))

      
        

  # print ('Videos:\n', '\n'.join(videos), '\n')



if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('--q', help='Search term', default='Google')
  parser.add_argument('--max-results', help='Max results', default=25)
  args = parser.parse_args()

  try:
    # print(DEVELOPER_KEY[0])
    # print(type(DEVELOPER_KEY))
    youtube_search(args)
  except HttpError as e:
    print(e)
    print('An HTTP error %d occurred:\n%s' % (e.resp.status, e.content))