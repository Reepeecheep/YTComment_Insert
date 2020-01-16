# YTComment_Insert

This is a simple Python Script for insert comments on a Youtube Video

Install Dependencies:

```bat
pip3 install --upgrade google-api-python-client
pip3 install --upgrade google-auth-oauthlib google-auth-httplib2
pip3 install oauth2client
```

Usage:

Download the client_secrets.json file of your google app

Execute on terminal:

```bat
python3 ytcomment_insert.py --video_id <VIDEO_ID> --message <MESSAGE>
```
  
Aditional parameters

--loop: If you need insert more than one comment
--json: If the name of your json api file is'nt "client_secrets.json". Example:

```bat
python3 ytcomment_insert.py --video_id <VIDEO_ID> --message <MESSAGE> --json "key.json"
```
