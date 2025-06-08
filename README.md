# YouTube Playlist Builder

This script automates the process of building YouTube playlists by searching for videos on a specific channel based on title keywords — and adding them to a playlist while avoiding duplicates.

## 🔧 Features

- ✅ OAuth 2.0 authentication (no API key required)
- 🔍 Filters videos by title keyword prhase only (e.g., `"battle commander"`)
- ♻️ Skips duplicates already in the playlist
- 📚 Handles more than 50 videos (with pagination)
- 🧠 Great for curating large, long-running channels

## 🚀 Setup

1. Clone this repository
2. Install dependencies:
   ```bash
   pip install google-api-python-client google-auth google-auth-oauthlib
3. Login to Google Cloud Console (https://console.cloud.google.com) and create a new project (CTRL + O or CMD + O)
4. Create Oauth Credentials: https://console.cloud.google.com/apis/credentials
5. Download/save Oauth credential client_secret.json
6. Add yourself as test user for your app by editing your audience https://console.cloud.google.com/auth/audience
7. Create a Playlist on Youtube (you'll need the Playist ID). Open any video, click Save, In the new window, Create playlist (only way I see to do this if you have existing playists)
7. Open your new playlist in a web browser and grab the playist ID from the URL.  Starts with PLxxxxxxxxxxxxxxxxxxx
8. Navigate to the channel you want to make a playlist out of https://youtube.com/@berrics
9. Get the channel ID from any free online service like TunePocket https://www.tunepocket.com/youtube-channel-id-finder/
10. Channel ID's start with a UCxxxxxxxxxxx   IE: UCVq1Crat76rKsgu6WosKwmA
11. Edit youtube-playlist-builder.py line 8, 9, and 10 for the keyword, channelId, and Playlist_ID's
12. First time running the script it'll open a web browser and promt you to allow your app.  This creates token.pickle (your saved login)
13. DONE

 
   
