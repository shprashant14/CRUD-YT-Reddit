# Social Media CRUD Operations Using Streamlit

This project provides a **Streamlit-based web application** that allows users to perform **CRUD operations** (Create, Read, Update, Delete) on **YouTube** and **Reddit** platforms using their respective APIs. The application simplifies interaction with these platforms by offering an intuitive UI for managing video and post content.

---

## Features

### YouTube
- **Create**: Upload a video with title, description, and tags.
- **Read**: Fetch video details using video ID.
- **Update**: Edit the title and description of an existing video.
- **Delete**: Remove a video from your channel.

### Reddit
- **Create**: Submit a new post to a subreddit with optional flair.
- **Read**: Fetch recent posts from a subreddit.
- **Update**: Edit the content of an existing post.
- **Delete**: Delete an existing post.

---

## Installation

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/social-media-crud-operations.git
cd social-media-crud-operations
```

### 2. Set Up Dependencies
Install the required Python packages using pip:
```bash
pip install -r requirements.txt
```

### 3. Set Up Secrets
Create a `.streamlit/secrets.toml` file to store the API credentials. Use the following format:

```toml
[reddit]
client_id = "your_reddit_client_id"
client_secret = "your_reddit_client_secret"
user_agent = "your_user_agent"
username = "your_reddit_username"
password = "your_reddit_password"

[youtube]
client_secret = '''
{
    "installed": {
        "client_id": "your_youtube_client_id",
        "project_id": "your_project_id",
        ...
    }
}
'''
```

---

## Usage

### Run the Application
Start the Streamlit app:
```bash
streamlit run app.py
```

### Interact with the App
1. Open the app in your browser using the link provided in the terminal.
2. Use the sidebar to navigate between **YouTube** and **Reddit**.
3. Perform CRUD operations as per your requirements.

---

## API Authentication

### YouTube
The app uses **OAuth 2.0** for authenticating with the YouTube Data API. During the first run, a browser window will open for you to log in and authorize the app.

### Reddit
The app uses **Reddit API credentials** to authenticate via the PRAW (Python Reddit API Wrapper) library.

---

## Dependencies

The project uses the following libraries:
- `streamlit`: For creating the web application.
- `praw`: For interacting with the Reddit API.
- `google-api-python-client`: For interacting with the YouTube Data API.
- `google-auth-oauthlib`: For YouTube API authentication.

Install them using the `requirements.txt` file.

---

## Limitations
1. **YouTube**: Uploading videos requires the video file to be stored locally.
2. **Reddit**: Updating a post is limited to text content; flair updates are not supported.
3. **Streamlit Cloud**: Some OAuth authentication flows might not work seamlessly.

---

## Contributing
Contributions are welcome! Feel free to:
1. Fork the repository.
2. Create a feature branch.
3. Submit a pull request.

---

## License
This project is licensed under the [MIT License](LICENSE).

---

## Acknowledgments
- [Streamlit](https://streamlit.io)
- [Reddit API Documentation](https://www.reddit.com/dev/api)
- [YouTube Data API](https://developers.google.com/youtube)
