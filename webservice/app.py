from context import TripParameters, TripScheduler
import flask
import json
from flask_cors import CORS

app = flask.Flask(__name__)
CORS(app)
#app.config["DEBUG"] = True


@app.route('/evscheduler/trip/driving/<locations>', methods=['GET'])
def ScheduleTrip(locations):
    # Logan to St George
    coordinatePairs = str(locations).split(';')
    start = coordinatePairs[0].split(',')
    end = coordinatePairs[1].split(',')
    parameters = TripParameters(28, 40, 'NissanLeaf', startPoint=[start[1],start[0]], endPoint=[end[1],end[0]], hasDestinationCharger=True)

    scheduler = TripScheduler()
    schedule = scheduler.Schedule(parameters)
    schedule.Print()
    return json.dumps(schedule.OsrmRoute)

app.run()