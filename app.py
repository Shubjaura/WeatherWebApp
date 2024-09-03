from flask import Flask, render_template, request, jsonify
import pandas as pd
import json
import numpy as np

class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.int64):
            return int(obj)
        return super().default(obj)

app = Flask(__name__, static_folder='static')
app.json_encoder = CustomJSONEncoder

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'})
    
    print(file.filename)

    try:
        # Read the Excel file into a DataFrame
        df = pd.read_excel(file)
        cf= pd.read_excel(file)
        df['date'] = pd.to_datetime(df['Date/Time'])
        df['year_month'] = df['date'].dt.strftime('%Y-%b')
        df = df.sort_values('date')

        monthly_max_temp = df.groupby('year_month')['Max Temp (°C)'].max().reset_index()
        monthly_max_temp['year_month'] = pd.to_datetime(monthly_max_temp['year_month'], format='%Y-%b')
        monthly_max_temp = monthly_max_temp.sort_values('year_month')

        # Convert 'year_month' back to the desired format
        monthly_max_temp['year_month'] = monthly_max_temp['year_month'].dt.strftime('%Y-%b')

        monthly_min_temp = df.groupby('year_month')['Min Temp (°C)'].min().reset_index()
        monthly_min_temp['year_month'] = pd.to_datetime(monthly_min_temp['year_month'], format='%Y-%b')
        monthly_min_temp = monthly_min_temp.sort_values('year_month')
        monthly_min_temp['year_month'] = monthly_min_temp['year_month'].dt.strftime('%Y-%b')

        # Prepare the result as a dictionary
        result = {
            'Max_temp_date': str(cf[cf['Max Temp (°C)'] == cf['Max Temp (°C)'].max()]['Date/Time'].values[0])[:10]+" ",
            'Min_temp_date': str(cf[cf['Min Temp (°C)'] == cf['Min Temp (°C)'].min()]['Date/Time'].values[0])[:10]+" ",
            'Max_temp': df['Max Temp (°C)'].max(),
            'Min_temp': df['Min Temp (°C)'].min(),
            'chart_data': {
                'x': monthly_max_temp['year_month'].tolist(),
                'y': monthly_max_temp['Max Temp (°C)'].tolist(),
            },
            'chart_data2': {
                'x': monthly_min_temp['year_month'].tolist(),
                'y': monthly_min_temp['Min Temp (°C)'].tolist(),
            }
        }
        print(result)
        return jsonify(result)
    except Exception as e:
        print("error")
        print(str(e))  # Add this line to print any exception raised
        return jsonify({'error': 'Error uploading file.'})
if __name__ == '__main__':
    app.run(debug=True)
