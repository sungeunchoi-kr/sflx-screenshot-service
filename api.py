import os
import uuid
from datetime import datetime
from pathlib import Path
from flask import Flask, Response, request
from flask_restful import Resource, Api
from waitress import serve
import base64

from snapshotter import Snapshotter

#
# Environment Variables:
#   PORT - The port on which the api service runs [default=8080]
#   ROOTDIR - The path to the root directory where the data/screenshots will be saved. [default='./snapshots']
#   CHROME_DRIVER_PATH - The path to the chrome driver [default='./chromedriver']
#

rootdir = os.environ.get('ROOTDIR') or './snapshots'

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

@app.route('/api/take-screenshot/soundcloud/tracks', methods=['POST'])
def take_screenshot_soundcloud_tracks():
    try:
        url = request.args.get('url')
        print('POST /api/take-screenshot/soundcloud/charts?url={}'
              .format(url))

        now = datetime.now()
        subdir = now.strftime("%Y%m")
        date_time = now.strftime("%Y%m%dT%H%M%S")

        filename = date_time + '-' + str(uuid.uuid4()) + '.png'
        uri = subdir + '/' + filename
        filepath = rootdir + '/' + uri

        Path(rootdir + '/' + subdir).mkdir(parents=True, exist_ok=True)
        snap.soundcloud_track_fullpage(url, filepath)

        return { 'uri': uri }
    except Exception as e:
        return { 'error': repr(e) }

if __name__ == '__main__':
    port = os.environ.get('PORT') or 8080
    serve(app, host='0.0.0.0', port=port)

