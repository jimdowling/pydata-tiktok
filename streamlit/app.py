import streamlit as st
import hopsworks
from mimesis import Generic
from mimesis.locales import Locale
import pandas as pd
import random

# Function to print a styled header
def print_header(text, font_size=22):
    res = f'<span style=" font-size: {font_size}px;">{text}</span>'
    st.markdown(res, unsafe_allow_html=True)

# Function to retrieve and start model deployments
@st.cache_resource()
def get_deployments():
    # Displaying a message indicating the process has started
    st.write("🚀 Retrieving and Starting Deployments...")

    # Logging into the Hopsworks project
    project = hopsworks.login()

    fs = project.get_feature_store()

    interactions_fg = fs.get_feature_group(
        name="interactions",
        version=1,
    )

    videos_fg = fs.get_feature_group(
        name="videos",
        version=1,
    )

    # Getting the model serving instance from the project
    ms = project.get_model_serving()

    # Retrieving deployments for the query model and ranking model
    query_model_deployment =  ms.get_deployment("querydeployment")
    ranking_deployment =  ms.get_deployment("rankingdeployment")

    # Starting the ranking deployment with a maximum waiting time of 180 seconds
    ranking_deployment.start(await_running=180)

    # Starting the query model deployment with a maximum waiting time of 180 seconds
    query_model_deployment.start(await_running=180)

    # Displaying a message indicating that deployments are ready
    st.write('✅ Deployments are ready!')

    # Returning deployment instances
    return interactions_fg, videos_fg, ranking_deployment, query_model_deployment

def insert_interaction(user_id, video_id, interactions_fg):
    generic = Generic(locale=Locale.EN)
    interaction_id = generic.person.identifier(mask='####-##-####')
    interaction_type = random.choices(
        ['like', 'dislike', 'view', 'comment', 'share', 'skip'],
        weights=[1.5, 0.2, 3, 0.5, 0.8, 10], k=1
    )[0]
    watch_time = random.randint(1, 50)

    interaction_df = pd.DataFrame({
        'interaction_id': [interaction_id],
        'interaction_type': [interaction_type],
        'user_id': [user_id],
        'video_id': [video_id],
        'watch_time': [watch_time]
    })

    interactions_fg.insert(interaction_df)


# Define function to fetch recommendations
def fetch_recommendations(user_id, query_model_deployment):
    st.write('🔮 Getting recommendations...')
    deployment_input = {"instances": {"user_id": user_id}}
    prediction = query_model_deployment.predict(deployment_input)['predictions']['ranking']
    return prediction

# Function to insert interaction and fetch new recommendations
def handle_interaction(user_id, video_id, interactions_fg, query_model_deployment):
    insert_interaction(user_id, video_id, interactions_fg)
    return fetch_recommendations(user_id, query_model_deployment)


# Main Streamlit application logic
def main():
    st.title('🎬 Video Recommender')
    # Initialize or re-use existing deployments
    if 'deployments_initialized' not in st.session_state:
        st.session_state.interactions_fg, st.session_state.videos_fg, st.session_state.ranking_deployment, st.session_state.query_model_deployment = get_deployments()
        st.session_state['deployments_initialized'] = True

    # User selection box
    user_id_option = st.selectbox(
        'For which user?',
        ('AH790A','PE989U'), # TODO - change this to a valid `user_id` in your feature group
        key='user_select'
    )

    # Initialize or refresh recommendations
    if 'recommendations' not in st.session_state or 'refresh' in st.session_state:
        recommendations = fetch_recommendations(user_id_option, st.session_state.query_model_deployment)
        random.shuffle(recommendations)
        st.session_state.recommendations = recommendations
        st.session_state.pop('refresh', None)

    print_header('📝 Top 3 Recommendations:')
    displayed_recommendations = st.session_state.recommendations[:3]
    for recommendation in displayed_recommendations:
        video_id = recommendation[1]
        if st.button(f"🔗 Video ID: {video_id}", key=video_id):
            new_recommendations = handle_interaction(
                user_id_option,
                video_id,
                st.session_state.interactions_fg,
                st.session_state.query_model_deployment,
            )
            random.shuffle(new_recommendations)
            st.session_state.recommendations = new_recommendations
            st.experimental_rerun()

    if st.button("Stop Streamlit"):
        st.write('⚙️ Stopping Deployments...')
        st.session_state.ranking_deployment.stop()
        st.session_state.query_model_deployment.stop()
        st.success('✅ App finished successfully!')
        st.stop()

if __name__ == '__main__':
    main()
