from datetime import timedelta
from decouple import config,Csv
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from django.utils.dateparse import  parse_datetime
import urllib.request
from .models import VideoDataModel, ThumbnailModel
from django.utils.timezone import is_aware, make_aware , now
from django.core.files import File

DEVELOPER_KEY = config('DEVELOPER_KEY', cast=Csv())
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'


def get_aware_datetime(date_str):
  ret = parse_datetime(date_str)
  if not is_aware(ret):
      ret = make_aware(ret)
  return ret


class YoutubeAPIClient():
  """
  The youtubeapi client is used to fetch the video data from youtube.
  The data is then stored in the database.
  It rotates the api key index to fetch the next api key from the .env to avoid hitting the quota.
  If the request fails it moves to the next.
  If the request fails for all the api keys it retrires for maxTries times.
  If it still failes then it stops the scheduler.
  It also updates the publishedAfter date to fetch the next day's data after every request.
  """
  def __init__(self, query=None, pageToken=None, max_results=None , publishedAfter=None , scheduleJob=None , maxTries=None):
      self.query = query
      self.pageToken = pageToken
      self.max_results = max_results
      if publishedAfter != None:
        self.publishedAfter = publishedAfter
      else:
        self.publishedAfter = now()
      self.apiKeyIndex = 0
      self.apiKeyIndexMaxValue=len(DEVELOPER_KEY)-1
      self.maxTries = maxTries
      self.tryCount = 0
      self.scheduleJob = scheduleJob

  def execute(self):
    try:
      print('start')
      result = self.__youtube_search()
    except HttpError as e:
      if e.status_code == 403 or e.status_code == 400:
        print(f"Http Error : {e.content}")
        if self.tryCount < self.maxTries:
          self.__update_api_key_index()
          self.execute()
        else:
          print('Max tries reached')
          self.scheduleJob.stop_scheduler()
      return
    for item in result:
      self.__load_data(item)

  def __update_publishedAfter(self):
    self.publishedAfter = self.publishedAfter + timedelta(days=1)


  def __update_api_key_index(self):
    if self.apiKeyIndex < self.apiKeyIndexMaxValue:
      self.apiKeyIndex +=1
    else:
      self.apiKeyIndex = 0
      self.__update_try_count()
  
  def __update_try_count(self):
    self.tryCount += 1

  def __youtube_search(self):
      youtube = build(YOUTUBE_API_SERVICE_NAME,
                      YOUTUBE_API_VERSION,
                      developerKey=DEVELOPER_KEY[self.apiKeyIndex])

      # Call the search.list method to retrieve results matching the specified
      # query term.
      t = self.publishedAfter.isoformat()
      search_response = youtube.search().list(
          q=self.query,
          part='id,snippet',
          type='video',
          order='date',
          publishedAfter=self.publishedAfter.isoformat(),
          pageToken=self.pageToken,
          maxResults=self.max_results).execute()

      result_items = search_response.get('items', [])
      self.__update_publishedAfter()
      return result_items

  """
Load the videodata in the database
"""

  def __load_data(self, item):
      snippet = item['snippet']
      vdata = VideoDataModel(title=snippet['title'],
                              description=snippet['description'],
                              published=get_aware_datetime(
                                  snippet['publishedAt']),
                              channel_name=snippet['channelTitle'],
                              video_id=item['id']['videoId'])
      vdata.save()
      self.__save_images(snippet['thumbnails'], vdata)

  """
Save thumbnail images for the particular video data object
"""

  def __save_images(self, thumbnails, vdata):
      for type in thumbnails.keys():
          thumb = thumbnails[type]
          try:
              # fetch the image object inside the temp directory.
              result = urllib.request.urlretrieve(thumb['url'])
          except:
              # idelly log the failed request
              continue
          tmodel = ThumbnailModel(type=type,
                                  width=int(thumb['width']),
                                  height=int(thumb['width']))
          tmodel.video = vdata
          tmodel.image.save(thumb['url'].split('/')[-1],
                            File(open(result[0], 'rb')))
