import os
import streamlit as st
import praw
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from dotenv import load_dotenv
import json

# Load environment variables from .env file
load_dotenv()

# Get credentials for Reddit and YouTube
REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")
REDDIT_USER_AGENT = os.getenv("REDDIT_USER_AGENT")
REDDIT_USERNAME = os.getenv("REDDIT_USERNAME")
REDDIT_PASSWORD = os.getenv("REDDIT_PASSWORD")

YOUTUBE_CLIENT_SECRET_PATH = os.getenv("YOUTUBE_CLIENT_SECRET_PATH", "client_secret.json")


# Authenticate YouTube API using client_secret.json
def authenticate_youtube():
    st.info("Authenticating YouTube API...")
    scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]

    # Run OAuth flow
    flow = InstalledAppFlow.from_client_secrets_file(YOUTUBE_CLIENT_SECRET_PATH, scopes)
    credentials = flow.run_local_server(port=0)

    # Build YouTube API client
    youtube = build("youtube", "v3", credentials=credentials)
    return youtube


# Authenticate Reddit API
def authenticate_reddit():
    st.info("Authenticating Reddit API...")
    reddit = praw.Reddit(
        client_id=REDDIT_CLIENT_ID,
        client_secret=REDDIT_CLIENT_SECRET,
        user_agent=REDDIT_USER_AGENT,
        username=REDDIT_USERNAME,
        password=REDDIT_PASSWORD
    )
    return reddit


# YouTube CRUD Operations
def youtube_crud_operations(youtube):
    st.subheader("YouTube CRUD Operations")
    action = st.selectbox("Select an Operation", ["Create (Upload Video)", "Read Video Details", "Update Video", "Delete Video"])

    if action == "Create (Upload Video)":
        video_path = st.text_input("Enter Video Path (Local Path)")
        title = st.text_input("Enter Video Title")
        description = st.text_area("Enter Video Description")
        tags = st.text_input("Enter Tags (comma-separated)").split(",")
        if st.button("Upload Video"):
            try:
                body = {
                    "snippet": {
                        "title": title,
                        "description": description,
                        "tags": tags,
                        "categoryId": "22",
                    },
                    "status": {"privacyStatus": "public"},
                }
                request = youtube.videos().insert(
                    part="snippet,status",
                    body=body,
                    media_body=video_path
                )
                response = request.execute()
                st.success(f"Video uploaded successfully! Video ID: {response['id']}")
            except Exception as e:
                st.error(f"Error: {e}")

    elif action == "Read Video Details":
        video_id = st.text_input("Enter Video ID")
        if st.button("Fetch Details"):
            try:
                response = youtube.videos().list(part="snippet,statistics", id=video_id).execute()
                st.json(response)
            except HttpError as e:
                st.error(f"Error: {e}")

    elif action == "Update Video":
        video_id = st.text_input("Enter Video ID")
        new_title = st.text_input("Enter New Title")
        new_description = st.text_area("Enter New Description")
        if st.button("Update Video"):
            try:
                body = {
                    "id": video_id,
                    "snippet": {
                        "title": new_title,
                        "description": new_description,
                        "categoryId": "22",
                    },
                }
                youtube.videos().update(part="snippet", body=body).execute()
                st.success("Video updated successfully!")
            except HttpError as e:
                st.error(f"Error: {e}")

    elif action == "Delete Video":
        video_id = st.text_input("Enter Video ID")
        if st.button("Delete Video"):
            try:
                youtube.videos().delete(id=video_id).execute()
                st.warning("Video deleted successfully!")
            except HttpError as e:
                st.error(f"Error: {e}")


# Reddit CRUD Operations
def reddit_crud_operations(reddit):
    st.subheader("Reddit CRUD Operations")
    action = st.selectbox("Select an Operation", ["Create Post", "Read Posts", "Update Post", "Delete Post"])

    if action == "Create Post":
        subreddit_name = st.text_input("Enter Subreddit Name")
        title = st.text_input("Enter Post Title")
        content = st.text_area("Enter Post Content")
        if st.button("Submit Post"):
            try:
                subreddit = reddit.subreddit(subreddit_name)
                subreddit.submit(title, selftext=content)
                st.success(f"Post submitted to r/{subreddit_name}!")
            except Exception as e:
                st.error(f"Error: {e}")

    elif action == "Read Posts":
        subreddit_name = st.text_input("Enter Subreddit Name")
        limit = st.slider("Number of Posts to Fetch", 1, 10, 5)
        if st.button("Fetch Posts"):
            try:
                subreddit = reddit.subreddit(subreddit_name)
                for post in subreddit.new(limit=limit):
                    st.write(f"Title: {post.title}\nScore: {post.score}\nID: {post.id}\n")
            except Exception as e:
                st.error(f"Error: {e}")

    elif action == "Update Post":
        post_id = st.text_input("Enter Post ID")
        new_content = st.text_area("Enter New Content")
        if st.button("Update Post"):
            try:
                submission = reddit.submission(id=post_id)
                submission.edit(new_content)
                st.success("Post updated successfully!")
            except Exception as e:
                st.error(f"Error: {e}")

    elif action == "Delete Post":
        post_id = st.text_input("Enter Post ID")
        if st.button("Delete Post"):
            try:
                submission = reddit.submission(id=post_id)
                submission.delete()
                st.warning("Post deleted successfully!")
            except Exception as e:
                st.error(f"Error: {e}")


# Main Streamlit App
def main():
    st.title("Social Media CRUD Operations")
    st.sidebar.title("Navigation")
    platform = st.sidebar.radio("Choose a Platform", ["YouTube", "Reddit"])

    if platform == "YouTube":
        youtube = authenticate_youtube()
        youtube_crud_operations(youtube)
    elif platform == "Reddit":
        reddit = authenticate_reddit()
        reddit_crud_operations(reddit)


if __name__ == "__main__":
    main()
