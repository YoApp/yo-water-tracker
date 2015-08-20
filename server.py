# -*- coding: utf-8 -*-
"""


"""
from datetime import datetime, timedelta
import os

from flask import request
from flask import Flask
import pytz

import db
from utils import get_remote_addr, get_location_data


app = Flask(__name__)


@app.route('/yo-water/', methods=['POST', 'GET'])
def yowater():

    payload = request.args if request.args else request.get_json(force=True)
    username = payload.get('username')

    reminder = db.reminders.find_one({'username': username})

    reply_object = payload.get('reply')

    if reply_object is None:

        if db.reminders.find_one({'username': username}) is None:

            address = get_remote_addr(request)
            data = get_location_data(address)
            if not data:
                return 'Timezone needed'

            user_data = {'created': datetime.now(pytz.utc),
                         'username': username}

            if data.get('time_zone'):
                user_data.update({'timezone': data.get('time_zone')})

            db.reminders.insert(user_data)

            return 'OK'

    else:
        reply_text = reply_object.get('text')

        if reply_text == u'Can\'t right now 😖':
            reminder['trigger_date'] = datetime.now(pytz.utc) + timedelta(minutes=15)
        else:

            reminder['step'] += 1
            reminder['trigger_date'] = datetime.now(pytz.utc) + timedelta(minutes=60)

        reminder['last_reply_date'] = datetime.now(pytz.utc)

        db.reminders.update({'username': username},
                            reminder)

        db.replies.insert({'username': username,
                           'created': datetime.now(pytz.utc),
                           'reply': reply_text})

        return 'OK'


if __name__ == "__main__":
    app.debug = True
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", "5000")))
