# -*- coding: utf-8 -*-
import random
import string
import urllib2
from datetime import timedelta, datetime
import requests
import unicodecsv
from config import CSV_URL, YO_API_TOKEN
from db import db
import pytz


def fetch_reminders_texts():
    response = urllib2.urlopen(CSV_URL)
    reader = unicodecsv.reader(response, encoding='utf-8')

    texts = []
    for row in reader:
        texts.append(row)

    texts = [list(x) for x in zip(*texts)]
    return texts


reminders_texts = fetch_reminders_texts()


def trigger_applicable_reminders():

    reminders = db.reminders.find({})
    for reminder in reminders:
        trigger_applicable_reminders_for_username(reminder['username'])


def tomorrow_start_datetime(timezone):
    today = datetime.now(pytz.timezone(timezone))
    tomorrow = today + timedelta(days=1)
    tomorrow_start_date = tomorrow.replace(hour=9, minute=00)
    return tomorrow_start_date


def trigger_applicable_reminders_for_username(username):

    reminder = db.reminders.find_one({'username': username})

    if reminder.get('step') is None:
        reminder['step'] = 0

    if reminder.get('trigger_date') is None:

        reminder['trigger_date'] = tomorrow_start_datetime(reminder['timezone'])

        db.reminders.update({'username': username},
                            reminder)

    if reminder:

        if reminder.get('step') >= len(reminders_texts):

            reminder['step'] = 0
            reminder['trigger_date'] = tomorrow_start_datetime(reminder['timezone'])

        elif reminder['trigger_date'] <= datetime.now(pytz.utc):

            now_aware = datetime.now(pytz.timezone(reminder['timezone']))
            nine_pm_aware = now_aware.replace(hour=21, minute=00)

            if now_aware > nine_pm_aware and reminder['step'] < len(reminders_texts)-1:

                response_pair = 'Good night.Dismiss'

                reminder_text = u'You had only ' + str(reminder['step']) + u'.. last reminder for today! Good night 😀'

                reminder['step'] = 0
                reminder['trigger_date'] = tomorrow_start_datetime(reminder['timezone'])

                rendered_reminder_text = string.Template(reminder_text).substitute({'username': reminder['username']})

                send_yo(username=reminder['username'],
                        text=rendered_reminder_text,
                        response_pair=response_pair)

                return

            response_pair = 'Can\'t right now 😖.Done ✅'

            reminders_texts_options = reminders_texts[reminder['step']]
            reminder_text = (random.choice(reminders_texts_options))
            rendered_reminder_text = string.Template(reminder_text).substitute({'username': reminder['username']})
            send_yo(username=reminder['username'],
                    text=rendered_reminder_text,
                    response_pair=response_pair)

            
def send_yo(username, text, response_pair):
    params = {'api_token': YO_API_TOKEN,
              'response_pair': response_pair,
              'text': text,
              'username': username}

    res = requests.post('http://api.justyo.co/yo/',
                        json=params)

    if res.status_code == 200:
        print 'Sent to ' + username + ': ' + text
    else:
        print 'Failed sending to ' + username + ': ' + text + ' ; ' + str(res.status_code) + ' ' + res.text