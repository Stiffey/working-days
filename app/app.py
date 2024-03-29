from datetime import date, timedelta, datetime
import numpy as np
import json
import requests
from calendar import month, monthrange
from flask import Flask, render_template, request, url_for, redirect
import os
import logging
logging.basicConfig(level=logging.INFO)


# from werkzeug.exceptions import HTTPException

app = Flask(__name__)

@app.route('/', methods=('GET', 'POST'))
def workingDays():
    month_year = request.args.get("month")
    months = ['January', "Febuary", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    holidaysJSON = requests.get("https://www.gov.uk/bank-holidays.json")
    ukHolidaysJSON = json.loads(holidaysJSON.text)['england-and-wales']['events']
    min_date = ukHolidaysJSON[0]['date']
    min_date_yyyy_mm = min_date[0:7]
    max_date = ukHolidaysJSON[-1]['date']
    max_date_yyyy_mm = max_date[0:7]

    current_month_yyyy_mm = str(datetime.now())[0:7]
    
    
    try:
        month_year
    except:
        day = "Select a date"
    
    # else:
    if month_year is None:
        day = "Select a date"
        logging.info('No month selected')
        date_picker_spec = {
                            "day" : day,
                            "current_month" : current_month_yyyy_mm,
                            "minimum_date" : min_date_yyyy_mm,
                            "maximum_date" : max_date_yyyy_mm
                            }

        return render_template('index.html', date_picker_spec=date_picker_spec)
    
    else:
        month_year_split = month_year.split("-")
        month = month_year_split[1]
        year = month_year_split[0]

        try:
            month_name = months[(int(month  ) - 1)]
            monthInput = month
            yearInput = year
            ukHolidayList = []
            holidaysJSON = requests.get("https://www.gov.uk/bank-holidays.json")
            ukHolidaysJSON = json.loads(holidaysJSON.text)['england-and-wales']['events']
            min_date = ukHolidaysJSON[0]['date']

            # for events in ukHolidays:
            eventIterator = 0

            for events in ukHolidaysJSON:
                # if partialDate in ukHolidays[eventIterator].values():
                ukHolidayDate = list(ukHolidaysJSON[eventIterator].values())[1]
                ukHolidayList.append(ukHolidayDate)
                eventIterator += 1
            
            # Calculate days in the month
            daysInMonth = monthrange(int(yearInput), int(monthInput))[1] # Extract the number of days in the month

            # Define start and end dates
            sdate = date(int(yearInput), int(monthInput), 1)   # start date
            edate = date(int(yearInput), int(monthInput), int(daysInMonth))   # end date

            # Calculate delta
            delta = edate - sdate     # as timedelta

        except:
            return "Date not found"

        # Find all of the business days in the month
        numberOfWorkingDays = 0
        workingDay = []
        for i in range(delta.days + 1):  # Look through all days in the month
            day = sdate + timedelta(days=i)
            if np.is_busday([day]) and str(day) not in ukHolidayList: # Determine if it's a business day
                # print("- " + str(day))
                workingDay.append(str(day))
                numberOfWorkingDays += 1

        # Count all of the UK hoidays
        public_holidays = []
        numberOfHolidays = 0
        for i in range(delta.days + 1):  # Look through all days in the month
            day = sdate + timedelta(days=i)
            if str(day) in ukHolidayList: # Determine if it's a uk holiday
                public_holidays.append(str(day))
                numberOfHolidays += 1

        # Make a list of public holidays
        public_holiday_list = [
            title["title"]
            for title in ukHolidaysJSON if datetime.strptime(title["date"],
                                                                '%Y-%m-%d').date() >= sdate and datetime.strptime(title["date"], "%Y-%m-%d").date() <= edate ]
        

        public_holiday_list.reverse()

        date_picker_spec = {
                    "day" : day,
                    "current_month" : current_month_yyyy_mm,
                    "minimum_date" : min_date_yyyy_mm,
                    "maximum_date" : max_date_yyyy_mm
                    }

        return render_template('index.html', date_picker_spec=date_picker_spec, day=workingDay, month_year=month_year, month=month, year=year, numberOfWorkingDays=numberOfWorkingDays, numberOfHolidays=numberOfHolidays, month_name=month_name, public_holidays=public_holidays, public_holiday_list=public_holiday_list)

@app.errorhandler(404)
def handle_bad_request(e):
    return '<h1>Bad URL</h1>', 400