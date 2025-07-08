# Drug Recommendation System

This project presents the design, development, and deployment of a content-based medicine recommendation system aimed at aiding users in discovering appropriate medications based on their symptoms or similar medicines.  
Leveraging a TF-IDF (Term Frequency-Inverse Document Frequency) vectorizer and cosine similarity, the system compares textual descriptions of medicine uses to generate personalized recommendations.  
The project follows an end-to-end pipeline from data cleaning, feature engineering, similarity matrix computation, to web deployment using Flask and Render.  

A lightweight login mechanism ensures secure access, and an intuitive interface allows users to interact with the system through condition-based search or medicine name-based similarity.  
This work demonstrates the feasibility of building and deploying accessible recommendation tools for healthcare use cases.

---

## Methodology

- **Data Collection**: A curated dataset of medicines with fields such as `Medicine_Name`, `Uses`, and `Side_Effects`.
- **Text Preprocessing**: Cleaning and combining use-case fields.
- **Feature Engineering**: TF-IDF vectorization on the `combined` field to convert text into numerical features.
- **Similarity Matrix**: Cosine similarity between vectors computed and stored.

---

## System Design and Implementation

- **Backend**: Flask-based web server handles routing and form submission.
- **Frontend**: HTML templates for rendering recommendation results and login flow.
- **Security**: A basic login system using Flask sessions.
- **Deployment**: Application hosted on Render, with source control managed on GitHub.

---

## Results and Use Cases

Two main user flows are supported:

1. **Condition-Based Search**:  
   Input a condition (e.g., *“headache”*) to get relevant medicines.

2. **Medicine-Based Recommendation**:  
   Input a known medicine name (via dropdown or manual entry) to see similar alternatives.
