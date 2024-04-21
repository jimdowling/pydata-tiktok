from mimesis import Generic
from mimesis.locales import Locale
import random
from datetime import datetime, timedelta
from typing import List, Dict, Any


def generate_interactions(num_interactions: int, users: List[Dict[str, str]], videos: List[Dict[str, str]]) -> List[Dict[str, Any]]:
    """
    Generate a list of dictionaries, each representing an interaction between a user and a video.

    This function creates interaction data by randomly pairing users with videos and assigning
    interaction details like interaction type, watch time, and whether the video was watched till the end.
    The likelihood of a video being watched till the end is inversely proportional to its length.

    Args:
        num_interactions (int): The number of interactions to generate.
        users (List[Dict[str, str]]): A list of dictionaries, where each dictionary contains user data.
        videos (List[Dict[str, str]]): A list of dictionaries, where each dictionary contains video data.

    Returns:
        List[Dict[str, Any]]: A list of dictionaries, each containing interaction data.
    """
    generic = Generic(locale=Locale.EN)
    interactions = []  # List to store generated interaction data

    for _ in range(num_interactions):
        user = random.choice(users)
        video = random.choice(videos)

        interaction_types = ['like', 'dislike', 'view', 'comment', 'share', 'skip']
        weights = [1.5, 0.2, 3, 0.5, 0.8, 10]

        # Generate watch time and determine if the video was watched till the end
        watch_time = random.randint(1, video['video_length'])
        
        probability_watched_till_end = 1 - (watch_time / video['video_length'])
        watched_till_end = random.random() < probability_watched_till_end

        if watched_till_end:
            watch_time = video['video_length']  # Adjust watch time to video length if watched till the end

        # Constructing the interaction dictionary
        interaction = {
            'interaction_id': generic.person.identifier(mask='####-##-####'),
            'user_id': user['user_id'],
            'video_id': video['video_id'],
            'interaction_type': random.choices(interaction_types, weights=weights, k=1)[0],
            'watch_time': watch_time,
        }

        interactions.append(interaction)  # Add the interaction to the list

    return interactions
