# youtube-api-analytics

This readme file gives representation how to fetch data from the YouTube Data API, process it, store it in a PostgreSQL database, and visualize insights using Streamlit.

## Architecture

The architecture involves several components:

1. **YouTube Integration (`youtube_integration.py`)**:
   - **API Integration**: Connects to the YouTube Data API to fetch video details.
   - **Data Processing**: Extracts video metadata such as title, description, view counts, likes, comments, and publication dates.
   - **Database Interaction**: Uses SQLAlchemy to interact with a PostgreSQL database for storing fetched data.

2. **Data Visualization (`visualization.py`)**:
   - **Streamlit App**: Provides a web interface to visualize YouTube video data.
   - **Update Mechanism**: Periodically fetches data from YouTube using `fetch_video_data` and updates the database.
   - **Visualization**: Utilizes Plotly and Streamlit for interactive charts showing view count trends, top videos by view count, and likes/comments analysis.

3. **Database (`PostgreSQL`)**:
   - Stores both raw video data and processed insights.
   - Schema includes fields like `video_id`, `title`, `description`, `view_count`, `like_count`, `comment_count`, and `published_at`.

## Setup and Installation

### Prerequisites

- Python 3.6+
- PostgreSQL database server
- Google Cloud Console API key for YouTube Data API v3

### Installation

Install dependencies:

   ```bash
      pip install -r requirements.txt
   ```

Create a PostgreSQL database and update db_string in both youtube_integration.py and visualization.py with your database credentials.

Obtain a YouTube API key from Google Cloud Console and update config.ini with your API key and channel ID.

### Running the Project
1. YouTube Data Integration:
- To fetch and store YouTube video data:

   ```bash
   python youtube_integration.py
   ```
  This script connects to the YouTube API, retrieves video data for the specified channel, processes it, and stores it in the PostgreSQL database.

2. Data Visualization

To run the Streamlit web app for visualization:

```bash
streamlit run visualization.py
```

Access the web app in your browser (http://localhost:8501) where you can enter your YouTube API key and channel ID to visualize video data insights.

### Project Maintenance

1. Error Handling: Both scripts include retry mechanisms for handling API rate limits and network errors.

2. Performance: Ensure the PostgreSQL database is optimized for handling large datasets as the application scales.

3. Deployment: Optionally, deploy the PostgreSQL database and Streamlit app on a cloud platform for scalability.

### Visualization Flow Charts
**Data Flow in youtube_integration.py**:

```
API (YouTube Data) -> Fetch Data -> Process Data -> Store in PostgreSQL
```

**Data Flow in visualization.py**:
```
Streamlit UI -> Fetch Data -> Visualize with Plotly -> Display Charts
```

### Additional Notes

This project can be extended to include more complex data processing, additional API endpoints, or advanced visualizations as per specific requirements
 
