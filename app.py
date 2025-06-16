from flask import Flask, render_template, request, redirect, url_for, session, flash
import pandas as pd
import joblib

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a secure key in production

# Load cleaned data
data = pd.read_csv("cleaned_data.csv")

# Load compressed similarity matrix
with open("cosine_similarity_compressed.pkl", "rb") as f:
    cosine_sim = joblib.load(f)

# Search by condition
def search_medicines(condition, top_n=5):
    condition = condition.lower()
    results = data[data['Uses_clean'].str.contains(condition, case=False, na=False)]
    return results.head(top_n)[['Medicine_Name', 'Uses']]

# Recommend similar medicines
def recommend(medicine_name, df=data, similarity_matrix=cosine_sim, top_n=5):
    if medicine_name not in df['Medicine_Name'].values:
        return []
    index = df[df['Medicine_Name'] == medicine_name].index[0]
    similarity_scores = list(enumerate(similarity_matrix[index]))
    similarity_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)[1:top_n+1]
    recommended = [df.iloc[i[0]][['Medicine_Name', 'Uses']].to_dict() for i in similarity_scores]
    return recommended

# Login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Dummy login check
        if username == 'admin' and password == 'password':
            session['logged_in'] = True
            session['username'] = username
            return redirect(url_for('index'))
        else:
            flash('Invalid credentials. Please try again.')
    return render_template('login.html')

# Logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# Home page with recommendation logic
@app.route('/', methods=['GET', 'POST'])
def index():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

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

    # Get unique medicine names for the dropdown
    medicine_names = sorted(data['Medicine_Name'].dropna().unique())

    return render_template(
        'index.html',
        results=recommendations,
        medicine_recommendations=medicine_recommendations,
        username=session.get('username'),
        medicine_names=medicine_names  # send to template
    )

if __name__ == '__main__':
    app.run(debug=True)

