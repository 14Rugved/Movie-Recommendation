Movie Recommendation System 🎬

This is a Movie Recommendation System built using Streamlit and TMDb API to fetch movie posters. The system suggests similar movies based on a similarity matrix using cosine similarity.

🚀 Features

Movie selection from a dropdown list

Fetches 5 recommended movies based on similarity

Displays movie posters using TMDb API

Error handling for missing data and API failures

Deployed online for easy access

🛠️ Technologies Used

Python

Streamlit (for UI)

Pandas (for data handling)

Pickle (to load precomputed similarity matrix & movie data)

TMDb API (to fetch movie posters)

Requests (to handle API requests)

📌 Installation

Clone the repository:

git clone https://github.com/yourusername/movie-recommendation-system.git
cd movie-recommendation-system

Install dependencies:

pip install -r requirements.txt

Ensure you have movies.pkl and similarity.pkl files in the project directory.

Run the Streamlit app:

streamlit run app.py

⚡ Deployment

This app has been successfully deployed. You can access it at:
🔗[ Live App](https://movie-recommendation-gwzqv2kl2mvftsswkxldqf.streamlit.app/)


🎯 How It Works

Select a Movie from the dropdown.

Click on Recommend to get suggestions.

The system fetches 5 similar movies and displays posters.

If any error occurs, meaningful messages are shown.


