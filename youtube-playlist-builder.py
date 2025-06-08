from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import os

# ----------------------------- CONFIG -----------------------------
CLIENT_SECRETS_FILE = "client_secret.json"  # Path to OAuth credentials
SCOPES = ["https://www.googleapis.com/auth/youtube"]
SEARCH_KEYWORD = "battle commander"
CHANNEL_ID = "UCVq1Crat76rKsgu6WosKwmA"  # <- Replace with actual channel ID
PLAYLIST_ID = "PL2125d6tKUddcx2Kpo0UQCXLWzh-jcuRL"  # <- Replace with your playlist ID
MAX_VIDEOS = 500
# ------------------------------------------------------------------

# Authenticate with YouTube
def authenticate_youtube():
    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
    creds = flow.run_local_server(port=0)
    return build("youtube", "v3", credentials=creds)

# Search for videos on a channel that match the title filter
def search_videos(youtube, channel_id, query, max_total=200):
    video_ids = []
    next_page_token = None

    while len(video_ids) < max_total:
        request = youtube.search().list(
            part="snippet",
            channelId=channel_id,
            q=query,
            type="video",
            maxResults=50,
            pageToken=next_page_token
        )
        response = request.execute()

        for item in response["items"]:
            title = item["snippet"]["title"]
            if query.lower() in title.lower():
                video_id = item["id"]["videoId"]
                video_ids.append(video_id)
                print(f"✅ Match: {title}")
            else:
                print(f"⏭️ Skipped: {title}")

        next_page_token = response.get("nextPageToken")
        if not next_page_token:
            break

    return video_ids

# Get existing video IDs in the target playlist to avoid duplicates
def get_existing_playlist_video_ids(youtube, playlist_id):
    video_ids = []
    next_page_token = None

    while True:
        request = youtube.playlistItems().list(
            part="contentDetails",
            playlistId=playlist_id,
            maxResults=50,
            pageToken=next_page_token
        )
        response = request.execute()

        for item in response["items"]:
            video_ids.append(item["contentDetails"]["videoId"])

        next_page_token = response.get("nextPageToken")
        if not next_page_token:
            break

    return set(video_ids)

# Add a single video to the playlist
def add_to_playlist(youtube, playlist_id, video_id):
    request = youtube.playlistItems().insert(
        part="snippet",
        body={
            "snippet": {
                "playlistId": playlist_id,
                "resourceId": {
                    "kind": "youtube#video",
                    "videoId": video_id
                }
            }
        }
    )
    return request.execute()

# ----------------------------- MAIN -----------------------------

def main():
    youtube = authenticate_youtube()

    print("🔍 Searching for videos...")
    search_results = search_videos(youtube, CHANNEL_ID, SEARCH_KEYWORD, MAX_VIDEOS)

    print(f"\n🧼 Checking for duplicates in playlist...")
    existing_ids = get_existing_playlist_video_ids(youtube, PLAYLIST_ID)

    added = 0
    skipped = 0

    for video_id in search_results:
        if video_id in existing_ids:
            print(f"🚫 Already in playlist: {video_id}")
            skipped += 1
            continue
        try:
            add_to_playlist(youtube, PLAYLIST_ID, video_id)
            print(f"✅ Added to playlist: {video_id}")
            added += 1
        except Exception as e:
            print(f"❌ Error adding {video_id}: {e}")

    print(f"\n🎉 Done! {added} added, {skipped} skipped.")

if __name__ == "__main__":
    main()
