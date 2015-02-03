from flask import Flask, Response
from flask.ext.restful import request,reqparse, abort, Api, Resource, fields, marshal
from flask.ext.cors import CORS  # The typical way to import flask-cors
import StringIO
import pandas as pd


app = Flask(__name__)
api = Api(app)
cors = CORS(app)



df = pd.read_csv("/home/hadrian/Desktop/MMDA Traffic /back end/data/01-24/01-24.csv")

def cleanFilterData(data=df, year=2014, month=8, line=0, station=0, bound=0):
    # Function to determine whether time is on the 1st/2nd half of the hour    
    quarterToHalf = lambda x: 0 if (x == 0 or x == 1) else 5    
    # Data Filtering; Select only rows which satisfy criteria
    result = data[(data.year == year) & (data.month == month) & (data.stationID == station) & (data.lineID == line)]
    # Remove unneeded index column     
    result = result.reset_index(drop=True)
    # Apply quarterToHalf to all rows    
    result['half'] = result.apply(lambda row: quarterToHalf(row['quarter']), axis = 1)
    # Remove unneeded columns    
    result = result.drop(['lineID','month','quarter','stationID', 'year'], 1)
    # Index by name of day, hour, half-hour    
    result = result.groupby(['day_name','hour','half'])
    # North or Southbound status
    if bound == 0:
        result = result.statusN.mean().reset_index()
        result.rename(columns={'day_name':'day', 'statusN':'status'}, inplace=True)    
    else:
        result = result.statusS.mean().reset_index()
        result.rename(columns={'day_name':'day', 'statusS':'status'}, inplace=True)    
    # Format hour for Front end
    result.hour = result.hour.map(str) + result.half.map(str)
    result.hour = result.hour.map(int)
    result.day_name = result.day.map(int)    
    # Drop unnecessary column        
    result = result.drop(['half'],1)
    return result



# Route that will process the AJAX request, sum up two
# integer numbers (defaulted to zero) and return the
# result as a proper JSON response (Content-Type, etc.)
@app.route('/')
def add_numbers():
    year = request.args.get('year', 2014, type=int)
    month = request.args.get('month', 8, type=int)
    lineID = request.args.get('lineID', 0, type=int)
    stationID = request.args.get('stationID', 1, type=int)
    bound = request.args.get('bound', 0, type=int)
    output = StringIO.StringIO()
    b = cleanFilterData(df, year, month, lineID, stationID, bound)
    b.to_csv(output, orient='records')
    return Response(output.getvalue(), mimetype="text/csv")



if __name__ == '__main__':
    app.run(debug=True)