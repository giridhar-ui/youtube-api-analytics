import streamlit as st
import pandas as pd
from tabulate import tabulate
import plotly.express as px
from youtube_integration import *
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Text, TIMESTAMP, text

import time
# Function to fetch video data using YouTube API
# Main Streamlit app


def update_data(api_key, channel_id):
    try:
        # Fetch video data using the API key and channel ID
        videos_data = fetch_video_data(api_key, channel_id)

        # Convert video data to DataFrame
        df = pd.DataFrame([{
            'video_id': v['id'],
            'title': v['snippet']['title'],
            'description': v['snippet']['description'],
            'view_count': int(v['statistics'].get('viewCount', 0)),
            'like_count': int(v['statistics'].get('likeCount', 0)),
            'comment_count': int(v['statistics'].get('commentCount', 0)),
            'published_at': v['snippet']['publishedAt']
        } for v in videos_data])

        # Convert published_at to datetime
        df['published_at'] = pd.to_datetime(df['published_at'])

        # Insert data into PostgreSQL database
        # insert_data_into_db(df, engine)

        st.write("Data updated successfully!")
    except Exception as e:
        st.error(f"Error updating data: {e}")


def visualization(videos_data, engine):

    df = pd.DataFrame([{
        'video_id': v['id'],
        'title': v['snippet']['title'],
        'description': v['snippet']['description'],
        'view_count': int(v['statistics'].get('viewCount', 0)),
        'like_count': int(v['statistics'].get('likeCount', 0)),
        'comment_count': int(v['statistics'].get('commentCount', 0)),
        'published_at': v['snippet']['publishedAt']
    } for v in videos_data])

    insert_data_into_db(df, engine)

    st.dataframe(df)

    st.subheader("View Count Over Time")
    fig_line = px.line(df, x='published_at', y='view_count', title='View Count Over Time')
    fig_line.update_layout(xaxis_title='Published At', yaxis_title='View Count')
    st.plotly_chart(fig_line)

    # Top Videos by View Count (Plotly bar chart)
    st.subheader("Top Videos by View Count")
    top_videos = df.nlargest(10, 'view_count')
    fig_bar = px.bar(top_videos, x='video_id', y='view_count', title='Top Videos by View Count')
    fig_bar.update_layout(xaxis_title='Video Title', yaxis_title='View Count')
    fig_bar.update_xaxes(tickangle=45, tickfont=dict(size=10))
    st.plotly_chart(fig_bar)

    # Likes and Comments (Plotly grouped bar chart)
    st.subheader("Likes and Comments")
    fig_likes_comments = px.bar(df, x='video_id', y=['like_count', 'comment_count'],
                                barmode='group', title='Likes and Comments')
    fig_likes_comments.update_layout(xaxis_title='Video Title', yaxis_title='Count')
    fig_likes_comments.update_xaxes(tickangle=45, tickfont=dict(size=10))
    st.plotly_chart(fig_likes_comments)


def main():
    st.title("YouTube Data Visualization App")

    # Input fields for API key, channel ID, and video ID
    api_key = st.text_input("Enter your YouTube API Key:")
    channel_id = st.text_input("Enter Channel ID:")

    if st.button("Collected Information"):
        st.subheader("Table View:")

        while True:
            print("update data")

            db_string = "postgresql://giridhar:dbpassword@127.0.0.1:5432/youtube"
            engine = create_engine(db_string)

            # Create table if it doesn't exist
            create_table(engine)

            videos_data = fetch_video_data(api_key, channel_id)
            visualization(videos_data, engine)
            time.sleep(50)


if __name__ == "__main__":
    main()
