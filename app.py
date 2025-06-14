from flask import Flask, render_template, request
import pandas as pd
import pickle
import os

# Load your cleaned data
data = pd.read_csv(r"cleaned_data.csv")  

app = Flask(__name__)

pkl_path = os.path.join(os.path.dirname(__file__), 'cosine_similarity.pkl')
with open(pkl_path, "rb") as f:
    similarity = pickle.load(f)

def search_medicines(condition, top_n=5):
    condition = condition.lower()
    results = data[data['Uses_clean'].str.contains(condition, case=False, na=False)]
    return results.head(top_n)[['Medicine_Name', 'Uses']]

def recommend(medicine_name, df=data, similarity_matrix=similarity_matrix, top_n=5):
    if medicine_name not in df['Medicine_Name'].values:
        return []
    index = df[df['Medicine_Name'] == medicine_name].index[0]
    similarity_scores = list(enumerate(similarity_matrix[index]))
    similarity_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)[1:top_n+1]

    recommended = [df.iloc[i[0]][['Medicine_Name', 'Uses']].to_dict() for i in similarity_scores]
    return recommended

@app.route('/', methods=['GET', 'POST'])
def index():
    recommendations = []
    medicine_recommendations = []
    if request.method == 'POST':
        if 'condition' in request.form and request.form['condition']:
            condition = request.form['condition']
            recommendations_df = search_medicines(condition)
            recommendations = recommendations_df.to_dict(orient='records')

        if 'medicine_name' in request.form and request.form['medicine_name']:
            medicine = request.form['medicine_name']
            medicine_recommendations = recommend(medicine)

    return render_template('index.html', results=recommendations, medicine_recommendations=medicine_recommendations)

if __name__ == '__main__':
    app.run(debug=True)
