### Get tokens read/modify tokens from, e.g.,
### https://developer.spotify.com/web-api/console/put-following/#complete

READ_AUTH_TOKEN="[]" # For account locked to facebook

MODIFY_AUTH_TOKEN="[]" # For new account tied to an email address

import time    
import json
import numpy as np
import urllib2

def run_transfer():
    
    ## Albums
    album_list = fetch_album_list(limit=50)
    put_album_list(album_list)
    
    ## Followed artists
    artist_list = fetch_artist_list()
    put_artist_list(artist_list)
    
class MethodRequest(urllib2.Request):
    """
    PUT request with urllib2
    
    From GitHub @logic: https://gist.github.com/logic/2715756
    """
    def __init__(self, *args, **kwargs):
        if 'method' in kwargs:
            self._method = kwargs['method']
            del kwargs['method']
        else:
            self._method = None
        return urllib2.Request.__init__(self, *args, **kwargs)

    def get_method(self, *args, **kwargs):
        if self._method is not None:
            return self._method
        return urllib2.Request.get_method(self, *args, **kwargs)

def fetch_album_list(limit=50, output='my_spotify_albums.json'):

    total = 10000
    offset = 0
    albums = []

    first = True

    while offset < total:
        request = urllib2.Request("https://api.spotify.com/v1/me/albums?limit=%d&offset=%d" %(limit, offset))
        request.add_header("Authorization", "Bearer %s" %(READ_AUTH_TOKEN))
        request.add_header("Accept", "application/json")

        response = urllib2.urlopen(request)
        data = json.load(response)
    
        if first:
            total = data['total']
            first = False
    
        albums.extend(data['items'])
        print 'Fetch albums %d - %d of %d' %(offset, offset+limit, total)

        offset += limit
    
    out = {'items': albums}
    fp = open(output,'w')
    json.dump(out, fp)
    fp.close()
    
    return out

def fetch_artist_list(limit=50, output='my_spotify_artists.json'):
    total = 10000
    offset = 0
    artists = []

    first = True
    
    url = "https://api.spotify.com/v1/me/following?type=artist&limit=%d" %(limit)
    
    while offset < total:
        request = urllib2.Request(url)
        request.add_header("Authorization", "Bearer %s" %(READ_AUTH_TOKEN))
        request.add_header("Accept", "application/json")

        response = urllib2.urlopen(request)
        data = json.load(response)
    
        if first:
            total = data['artists']['total']
            first = False
    
        artists.extend(data['artists']['items'])
        
        print 'Fetch artists %d - %d of %d' %(offset, offset+limit, total)

        offset += limit
        url = data['artists']['next']
    
    out = {'artists': {'items': artists}}
    
    fp = open(output,'w')
    json.dump(out, fp)
    fp.close()
    
    return out
    
def show_albums(album_list):
    for i, item in enumerate(album_list['items']):
        album = item['album']
        artists = [artist['name'] for artist in album['artists']]
        print '%4d: %s / %s' %(i, album['name'], ','.join(artists))

def show_artists(artist_list):
    for i, item in enumerate(artist_list['artists']['items']):
        print '%4d: %s / %s' %(i, item['name'], item['id'])

def put_artist_list(artist_list):    
    #artist_list = json.loads(open('my_spotify_artists.json','r').read())

    artist_names = [artist['name'] for artist in artist_list['artists']['items']]
    
    limit=20
    N = len(artist_list['artists']['items'])
    offset = 0
    while offset < N:
        if offset+limit > N:
            list_i = artist_list['artists']['items'][offset:]
        else:
            list_i = artist_list['artists']['items'][offset:offset+limit]
        
        print 'Send artists %d - %d' %(offset, offset+limit)
        offset += limit
        
        artist_ids = [str(artist['id']) for artist in list_i]
        artist_str = ','.join(artist_ids)
        url = "https://api.spotify.com/v1/me/following?type=artist&ids=%s" %(artist_str)
    
        request = MethodRequest(url, method='PUT') #, data=artist_str)
        request.add_header("Authorization", "Bearer %s" %(MODIFY_AUTH_TOKEN))
        request.add_header("Accept", "application/json")
        response = urllib2.urlopen(request)
        
def put_album_list(album_list):
    ### add them in order of "added_at" time
    dates = [item['added_at'] for item in album_list['items']]
    so = np.argsort(dates)
    
    for ix, i in enumerate(so):
        album_ids = [str(album_list['items'][i]['album']['id'])]
        album_name = album_list['items'][i]['album']['name']
        
        #album_ids = [str(id) for id in album_list[0:10]]
        album_str = ("%s" %(album_ids)).replace('\'', '\"')
    
        url = "https://api.spotify.com/v1/me/albums"
        request = MethodRequest(url, method='PUT', data=album_str)
        request.add_header("Authorization", "Bearer %s" %(MODIFY_AUTH_TOKEN))
        request.add_header("Content-Type", "application/json")
    
        print '%d/%d: %s' %(ix, len(so), album_name)
        time.sleep(1.1)
        
        response = urllib2.urlopen(request)
