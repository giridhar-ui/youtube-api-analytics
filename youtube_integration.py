import configparser
import requests
import pandas as pd
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Text, TIMESTAMP, text
from sqlalchemy.exc import IntegrityError
from retrying import retry


# Retry decorator configuration
retry_kwargs = {
    'wait_exponential_multiplier': 1000,
    'wait_exponential_max': 10000,
    'stop_max_attempt_number': 5,
}


@retry(**retry_kwargs)
def fetch_video_data(api_key, channel_id):
    url = (f"https://www.googleapis.com/youtube/v3/search?key="
           f"{api_key}&channelId={channel_id}&part=snippet,id&order=date&maxResults=20")
    response = requests.get(url)
    print(response.status_code)
    response.raise_for_status()  # Raise HTTPError for non-2xx responses
    video_data = response.json().get('items', [])

    videos = []

    for video in video_data:
        video_id = video['id'].get('videoId')
        if video_id:
            video_details = fetch_video_details(api_key, video_id)
            videos.append(video_details)
    return videos


@retry(**retry_kwargs)
def fetch_video_details(api_key, video_id):
    url = (f"https://www.googleapis.com/youtube/v3/videos?key="
           f"{api_key}&id={video_id}&part=snippet,contentDetails,statistics")
    response = requests.get(url)
    response.raise_for_status()  # Raise HTTPError for non-2xx responses
    return response.json().get('items', [])[0]


def create_table(engine):
    metadata = MetaData()

    videos = Table('videos', metadata,
                   Column('id', Integer, primary_key=True),
                   Column('video_id', String),
                   Column('title', String),
                   Column('description', Text),
                   Column('view_count', Integer),
                   Column('like_count', Integer),
                   Column('comment_count', Integer),
                   Column('published_at', TIMESTAMP)
                   )

    metadata.create_all(engine)


def insert_data_into_db(df, engine, table_name='videos', if_exists='append'):
    with engine.connect() as conn:

        delete_query = text(f"DELETE FROM {table_name}")
        conn.execute(delete_query)

        try:
            df.to_sql(table_name, con=conn, if_exists=if_exists, index=False)
            print("Data inserted successfully!")
        except IntegrityError as e:
            print(f"Error inserting data: {e}")


if __name__ == "__main__":
    # Read API key and channel ID from config file
    api_key = ""
    channel_id = ""

    # PostgreSQL connection string
    db_string = "postgresql://giridhar:dbpassword@127.0.0.1:5432/youtube"

    try:
        # Create engine
        engine = create_engine(db_string)

        # Create table if it doesn't exist
        create_table(engine)

        # Fetch video data using the fetched API key and channel ID
        videos_data = fetch_video_data(api_key, channel_id)

        # Convert videos data to DataFrame
        df = pd.DataFrame([{
            'video_id': v['id'],
            'title': v['snippet']['title'],
            'description': v['snippet']['description'],
            'view_count': int(v['statistics'].get('viewCount', 0)),
            'like_count': int(v['statistics'].get('likeCount', 0)),
            'comment_count': int(v['statistics'].get('commentCount', 0)),
            'published_at': v['snippet']['publishedAt']
        } for v in videos_data])

        # Insert data into the database
        insert_data_into_db(df, engine)

        # Print the DataFrame
        print(df)
    except Exception as e:
        print(f"Error fetching or inserting data: {e}")
