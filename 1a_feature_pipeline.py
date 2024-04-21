import pandas as pd
import hopsworks

from features.users import generate_users
from features.videos import generate_video_content
from features.interactions import generate_interactions


project = hopsworks.login()
fs = project.get_feature_store()

users_fg = fs.get_feature_group(
    name="users",
    version=1,
)

videos_fg = fs.get_feature_group(
    name="videos",
    version=1,
)

interactions_fg = fs.get_feature_group(
    name="interactions",
    version=1,
)

# Generate data for users
user_data = generate_users(1_000)
data_users_df = pd.DataFrame(user_data)

# Generate data for videos
video_data = generate_video_content(1_000)
data_video_df = pd.DataFrame(video_data)

# Generate interactions
num_interactions = 10_000
interactions = generate_interactions(num_interactions, user_data, video_data)
data_interactions_df = pd.DataFrame(interactions)

users_fg.insert(data_users_df)
videos_fg.insert(data_video_df)
interactions_fg.insert(data_interactions_df)
