# -*- coding: utf-8 -*-
import os

# url for a public google spreadsheet with all reminders texts as csv
CSV_URL = 'https://docs.google.com/spreadsheets/d/1rhZRohjtg3-yVXXbcvTcCgep93pCxbstJR-9gZe5XNU/pub?output=csv'


# Yo API Token for the account sending reminders (https://dev.justyo.co)
YO_API_TOKEN = os.environ.get('YO_API_TOKEN')


# connection string for a mongo db to store users states
MONGO_STRING = os.environ.get('MONGO_STRING')