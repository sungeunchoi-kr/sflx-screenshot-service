import os
import uuid
from datetime import datetime
from pathlib import Path
from flask import Flask, Response, request
from flask_restful import Resource, Api
from waitress import serve
import base64

from snapshotter import Snapshotter

rootdir = os.environ.get('ROOTDIR') or './post-snapshots'

app = Flask(__name__)
api = Api(app)

snap = Snapshotter()

##### begin api route definitions #####
@app.route('/api/take-screenshot/soundcloud/charts/<chart_descriptor>', methods=['POST'])
def takeSnapshots(chart_descriptor):
    try:
        print('POST /api/take-screenshot/soundcloud/charts/<chart_descriptor={}>'
              .format(chart_descriptor))

        now = datetime.now()
        subdir = now.strftime("%Y%m")
        date_time = now.strftime("%Y%m%dT%H%M%S")

        filename = date_time + '-' + str(uuid.uuid4()) + '.png'
        uri = subdir + '/' + filename
        filepath = rootdir + '/' + uri

        Path(rootdir + '/' + subdir).mkdir(parents=True, exist_ok=True)
        snap.soundcloud_charts(chart_descriptor, filepath)

        return { 'uri': uri }
    except Exception as e:
        return { 'error': repr(e) }

if __name__ == '__main__':
    port = os.environ.get('PORT') or 8080
    serve(app, host='0.0.0.0', port=port)

