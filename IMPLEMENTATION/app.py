
from flask import Flask, render_template, request
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def create_visualization(data, x, y):
    if x in data.columns and y in data.columns:
        plt.figure(figsize=(8, 6))
        sns.scatterplot(x=x, y=y, data=data)
        plt.title(f'{x} vs {y}')
        plt.xlabel(x)
        plt.ylabel(y)
        plt.savefig('static/visualization.png')
    else:
        return "Required columns not found in the dataset."

    

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        x = request.form['x']
        y = request.form['y']
        if file:
            df = pd.read_csv(file)
            result = create_visualization(df, x, y)
            if result == "Required columns not found in the dataset.":
                return result
            else:
                return render_template('visualization.html')
    return "Upload failed"

if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True)
