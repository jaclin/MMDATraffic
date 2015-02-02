from flask import Flask
from flask.ext.cors import CORS  # The typical way to import flask-cors
from flask.ext import restful
from flask import Response
import StringIO
import pandas as pd

app = Flask(__name__)
api = restful.Api(app)
cors = CORS(app)


df = pd.read_csv("../data/01-24/01-24.csv")

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

a = cleanFilterData()


class HelloWorld(restful.Resource):
	@app.route('/')
	def output_dataframe_csv():
	    output = StringIO.StringIO()
	    a.to_csv(output)
	 
	    return Response(output.getvalue(), mimetype="text/csv")

class Hello(restful.Resource):
    @app.route('/<int:year>/<int:month>/<int:lineID>/<int:stationID>/<int:bound>')
    def get(year,month,lineID,stationID,bound):
        output = StringIO.StringIO()
        b = cleanFilterData(df, year, month, lineID, stationID, bound)
        b.to_json(output, orient='records')
        return Response(output.getvalue(), mimetype="text/csv")


api.add_resource(HelloWorld, '/')
api.add_resource(Hello, '/?/<int:year>/<int:month>/<int:lineID>/<int:stationID>/<int:bound>')

if __name__ == '__main__':
    app.run(debug=True)
