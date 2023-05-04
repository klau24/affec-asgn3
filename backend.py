from flask import Flask, request, jsonify, Response
from flask_cors import CORS
import os
import io
import math
import csv
import glob
import pandas as pd
from emotiv_socket import main

app = Flask(__name__)
#cors = CORS(app, resources={r"/*": {"origins": "http://127.0.0.1:5000"}})

@app.route('/run_script')
def run_script():
    # Run the Emotiv script here
    # ...
    emotiv_data = main()
    
    response = jsonify({'result': 'success'})
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE')
    return response

@app.route('/combine_data', methods=['POST'])
def combine_data():
    csv_file = request.data
    csv_data = io.TextIOWrapper(io.BytesIO(csv_file), encoding='utf-8')
    csv_reader = csv.reader(csv_data)

    directory = "/Users/klau/Classes/csc570-affec/asgn3/affec-asgn3/"
    emoitivFile = glob.glob(os.path.join(directory, "exampleEmotiv*.csv"))[0]

    eyedataDF = pd.DataFrame(list(csv_reader))
    eyedataDF.columns = ['Timestamp', 'x', 'y']
    brainDF = pd.read_csv(emoitivFile, skiprows=[0])

    eyedataDF['Timestamp']=eyedataDF['Timestamp'].astype(float)
    brainDF['Timestamp']=brainDF['Timestamp'].astype(float)

    # round timestamp down to a whole number for more collisions on merge
    eyedataDF['Timestamp'] = eyedataDF['Timestamp'].apply(lambda x: math.floor(x))
    brainDF['Timestamp'] = brainDF['Timestamp'].apply(lambda x: math.floor(x))

    # join dataframes based on the same timestamp
    merged_df = pd.merge(eyedataDF, brainDF, on='Timestamp', how='inner')
    merge_csv_string = merged_df.to_csv(index=False)

    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE',
        'Content-Disposition': 'attachment;filename=combined.csv',
        'Content-Type': 'text/csv'
    }
    return Response(merge_csv_string, headers=headers)

if __name__ == '__main__':
    app.run()