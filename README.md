# Yo Water Tracker - a smart interactive water consumption tracker.

![](http://cl.ly/image/2o1n313O2f3D/water.png)

Yo Water is a smart interactive reminder that reminds you to drink 8 cups of water a day.

* Why smart?  
Because each reminder is dependent on your previous interactions with it. No more annoying constant time interval reminders.

* Why interactive?  
Because you can interact with the reminder with the 2 buttons it provides.

* Why water?  
Because hydration. 

## Uses:

* Flask
* MongoDB
* Google Spreadsheets

## How it works?

* Reminders texts are stored in a [Google Spreadsheet](https://docs.google.com/spreadsheets/u/1/d/1rhZRohjtg3-yVXXbcvTcCgep93pCxbstJR-9gZe5XNU/pub?output=html)
* Users states are stored in a MongoDB. [Compose.io has free plans](compose.io) 

1. A user subscribes.
2. A reminder entry is created in the db with trigger date of tomorrow 9am (user's timezone).
4. There is a cron job running checking if reminders needs to be sent.
5. At 9am a random reminder text is selected from the first column of the sheet.
6. The user either replies "Done", "Can't now" or doesn't reply
7. The server recieves the reply via a callback from Yo servers, and either bumps user `step` (cup) or not, based on the response.
8. The day continues and reminders are being sent based on replies (or no replies).
9. At 9pm if the user didn't drink 8 cups, a digest is sent and no reminders until next day.



