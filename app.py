from flask import Flask, request, render_template, redirect, url_for, send_from_directory
import pandas as pd
import matplotlib.pyplot as plt
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    if file:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)
        # Leer el archivo .csv
        df = pd.read_csv(file_path)
        columns = df.columns.tolist()
        return render_template('select_columns.html', columns=columns, file_name=file.filename)
    return redirect(request.url)

@app.route('/plot', methods=['POST'])
def plot_file():
    x_column = request.form['x_column']
    y_column = request.form['y_column']
    file_name = request.form['file_name']
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file_name)
    df = pd.read_csv(file_path)
    
    if x_column and y_column:
        plt.figure()
        plt.scatter(df[x_column], df[y_column])
        plt.xlabel(x_column)
        plt.ylabel(y_column)
        plt.title(f'{y_column} vs {x_column}')
        plot_path = os.path.join(app.config['UPLOAD_FOLDER'], 'plot.png')
        plt.savefig(plot_path)
        plt.close()
        return render_template('result.html', plot_url=url_for('static', filename='uploads/plot.png'))
    return redirect(url_for('index'))

@app.route('/static/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)
