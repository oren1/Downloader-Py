# Welcome to Cloud Functions for Firebase for Python!
# To get started, simply uncomment the below code or create your own.
# Deploy with `firebase deploy`

from firebase_functions import https_fn, options
from firebase_admin import initialize_app
from pytube import YouTube, exceptions
from urllib.parse import unquote
import json

initialize_app()

@https_fn.on_request(cors=options.CorsOptions(cors_origins="*", cors_methods=["get", "post"]))
def get_download_url(req: https_fn.Request) -> https_fn.Response:
   
    # grab the args
    if req.method == 'POST':
        encodedOriginalUrl = req.form.get('url')
        quality = req.form.get('quality')
    else:
        encodedOriginalUrl = req.args.get('url')
        quality = req.args.get('quality')
           

    if encodedOriginalUrl is None:
        return https_fn.Response("No url parameter provided", status=400)
    
    if quality is None:
        quality = '720p'

    # the url is sent encoded so we need to decode it
    originalUrl = unquote(encodedOriginalUrl)

    # get a downloadable url
    try:
        downloadUrl = getDownloadUrl(originalUrl, quality)
    except exceptions.AgeRestrictedError:
        return https_fn.Response(json.dumps({'error': 'this video is age restricted, and can`t be accessed'}))
    except:
        return https_fn.Response(json.dumps({'error': 'this video can`t be downloaded'}))

    # return the downloadable url in the response
    responseObject = json.dumps({'error': None, 'url': downloadUrl})

    return https_fn.Response(responseObject)


def getDownloadUrl(url, resolution = '360p'):
        streams = YouTube(url).streams
        for stream in streams:
            if (stream.mime_type == 'video/mp4' and stream.resolution == resolution and stream.is_progressive == True):
                return stream.url


