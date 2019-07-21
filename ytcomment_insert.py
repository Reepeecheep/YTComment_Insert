#!/usr/bin/python

import httplib2
import os
import sys
import random
import uuid

from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import argparser, run_flow

''' The CLIENT_SECRETS_FILE variable specifies the name of a file that contains
# the OAuth 2.0 information for this application, including its client_id and
# client_secret. You can acquire an OAuth 2.0 client ID and client secret from
# the Google Developers Console at
# https://console.developers.google.com/.
# Please ensure that you have enabled the YouTube Data API for your project.
# For more information about using OAuth2 to access the YouTube Data API, see:
#   https://developers.google.com/youtube/v3/guides/authentication
# For more information about the client_secrets.json file format, see:
#   https://developers.google.com/api-client-library/python/guide/aaa_client_secrets '''
CLIENT_SECRETS_FILE = "client_secrets.json"

# This OAuth 2.0 access scope allows for full read/write access to the authenticated user's account.
YOUTUBE_READ_WRITE_SCOPE = "https://www.googleapis.com/auth/youtube.force-ssl"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

# This variable defines a message to display if the CLIENT_SECRETS_FILE is missing.
MISSING_CLIENT_SECRETS_MESSAGE = """
WARNING: Please configure OAuth 2.0

To make this sample run you will need to populate the client_secrets.json file
found at:

   %s

with information from the Developers Console
https://console.developers.google.com/

For more information about the client_secrets.json file format, please visit:
https://developers.google.com/api-client-library/python/guide/aaa_client_secrets
""" % os.path.abspath(os.path.join(os.path.dirname(__file__),
                                   CLIENT_SECRETS_FILE))

def get_authenticated_service(args):
    flow = flow_from_clientsecrets(
        CLIENT_SECRETS_FILE,
        scope=YOUTUBE_READ_WRITE_SCOPE,
        message=MISSING_CLIENT_SECRETS_MESSAGE
    )
    storage = Storage("%s-oauth2.json" % sys.argv[0])
    credentials = storage.get()
    if credentials is None or credentials.invalid:
        credentials = run_flow(flow, storage, args)

    return build(
        YOUTUBE_API_SERVICE_NAME,
        YOUTUBE_API_VERSION,
        http=credentials.authorize(httplib2.Http())
    )

# Call the API's comments.insert method to reply to a comment.
# (If the intention is to create a new to-level comment, commentThreads.insert
# method should be used instead.)
def insert_comment(youtube, video_id, text, counter):
    insert_result = youtube.commentThreads().insert(
        part="snippet",
        body=dict(
            snippet=dict(
                topLevelComment=dict(
                    snippet=dict(
                        textOriginal=text
                    )
                ),
                videoId=video_id
            )
        )
    ).execute()
    
    counter += 1
    print ("Inserted comment {1}: {0}".format(text, counter))
    return counter

if __name__ == "__main__":
    argparser.add_argument("--video_id", required=True, help="ID of video to post.")
    argparser.add_argument("--message", required=True, help="Text of comment to post.")
    argparser.add_argument("--loop", required=False, help="Number of comments.")
    argparser.add_argument("--json", required=False, help="JSON FILE")
    
    args = argparser.parse_args()

    if (args.json):
        CLIENT_SECRETS_FILE = args.json

    if not (args.video_id and args.message):
        exit("Please specify:\n* video_id using the --video_id= parameter\n* message using the --message= parameter.")

    youtube = get_authenticated_service(args)
    
    counter = 0
    try:
        if (args.loop):
            for i in range(int(args.loop)):
                counter = insert_comment(youtube, args.video_id, "{} {}".format(args.message, counter+1), counter)
        else:
            counter = insert_comment(youtube, args.video_id, args.message, counter)
            
    except HttpError as e:
        print ("An HTTP error {} occurred:\n{}".format(e.resp.status, e.content))
