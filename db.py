# -*- coding: utf-8 -*-
import pymongo
from config import MONGO_STRING


client = pymongo.MongoClient(MONGO_STRING, tz_aware=True)
db = client['yo-water']