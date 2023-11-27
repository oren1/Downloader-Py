# Welcome to Cloud Functions for Firebase for Python!
# To get started, simply uncomment the below code or create your own.
# Deploy with `firebase deploy`

from firebase_functions import https_fn, options
from firebase_admin import initialize_app
from pytube import YouTube
from urllib.parse import unquote

initialize_app()


@https_fn.on_request()
def on_request_example(req: https_fn.Request) -> https_fn.Response:
    return https_fn.Response("Hello world!")

@https_fn.on_request(cors=options.CorsOptions(cors_origins="*", cors_methods=["get", "post"]))
def get_download_url(req: https_fn.Request) -> https_fn.Response:
    """Take the text parameter passed to this HTTP endpoint and insert it into
    a new document in the messages collection."""
    # Grab the text parameter.

    encodedOriginalUrl = req.args.get('url')
    print('url', encodedOriginalUrl)
    if encodedOriginalUrl is None:
        return https_fn.Response("No url parameter provided", status=400)
    
    originalUrl = unquote(encodedOriginalUrl)

    downloadUrl = getDownloadUrl(originalUrl, '720p')
    print(originalUrl)
    # Send back a message that we've successfully written the message
    return https_fn.Response(f"Download Url is: {downloadUrl}")


def getDownloadUrl(url, resolution = '360p'):
        streams = YouTube(url).streams
        for stream in streams:
            if (stream.mime_type == 'video/mp4' and stream.resolution == resolution and stream.is_progressive == True):
                return stream.url

