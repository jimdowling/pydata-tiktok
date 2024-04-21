from mimesis import Generic
from mimesis.locales import Locale
import random
from datetime import datetime, timedelta
from typing import List, Dict, Any


def generate_video_content(num_videos: int, historical=False) -> List[Dict[str, str]]:
    """
    Generate a list of dictionaries, each representing video content with various attributes.

    Each video includes details such as a unique video ID, category, views count, likes count,
    video length in seconds, and the upload date. The function uses the mimesis library
    for generating random data and Python's random module for numerical attributes.

    Args:
        num_videos (int): The number of video entries to generate.

    Returns:
        List[Dict[str, str]]: A list of dictionaries, each containing details of a video.
    """
    generic = Generic(locale=Locale.EN)
    videos = []  # List to store generated video data
    
    max_views = 500_000

    for _ in range(num_videos):
        if historical:
            days_ago = random.randint(0, 730)  # Choose a random number of days up to two years
            upload_date = datetime.now() - timedelta(days=days_ago)  # Compute the upload date
            
            # Views are influenced by the age of the video, simulating realistic view count accumulation
            age_factor = (730 - days_ago) / 730  # Decreases with the recency of the video
            views = random.randint(0, int(max_views * age_factor))
            
        else:
            upload_date = datetime.now()
            views = random.randint(0, max_views)
        
        # Likes should not exceed the number of views
        likes = random.randint(0, views)

        categories = ['Education', 'Entertainment', 'Lifestyle', 'Music', 'News', 'Sports', 'Technology', 'Dance', 'Cooking', 'Comedy', 'Travel']
        video_length_seconds = random.randint(10, 250)  # Video length in seconds

        video = {
            'video_id': generic.person.identifier(mask='#@@##@'),  # Unique video identifier
            'category': random.choice(categories),
            'views': views,
            'likes': likes,
            'video_length': video_length_seconds,
            'upload_date': upload_date.strftime('%Y-%m-%d')
        }

        videos.append(video)  # Add the video to the list

    return videos
