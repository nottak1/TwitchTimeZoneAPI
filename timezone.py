from datetime import datetime
import pytz
import re
from flask import Flask, request

"""
Timezones:
AEST - Australia Eastern Standard Time
ACST - Australia Central Standard Time
AKST - Alaska Standard Time
AST - Atlantic Standard Time
AWST - Australia Western Standard Time
CET - Central European Time
CST - Central Standard Time
EET - Eastern European Time
EST - Eastern Standard Time
MSK - Moscow Standard Time
MST - Mountain Standard Time
PST - Pacific Standard Time
WET - Western European Time
HST - Hawaii Standard Time
"""
timezonesAbb = {
    "Australia/Brisbane": ['AEST', 'AEDT'],
    "Australia/Darwin": ['ACST', 'ACDT'],
    "Australia/Perth": ['AWST'],
    "US/Alaska": ['AKST', 'AKCT', 'ALASKA'],
    "America/Anguilla": ['AST', 'ADT'],
    "CET": ['CET'],
    "US/Central": ['CST', 'CDT', 'CT', 'CENTRAL'],
    "US/Eastern": ['EST', 'EDT', 'ET', 'EASTERN'],
    "Europe/Moscow": ['MSK', 'MOSCOW'],
    "US/Mountain": ['MST', 'MDT', 'MT', 'MOUNTAIN'],
    "US/Pacific": ['PST', 'PDT', 'PT', 'PACIFIC'],
    "Europe/London": ['WET'],
    "US/Hawaii": ['HST', 'HDT'],
    "UTC": ['UTC']
}


def get_current_time(timezone):
    for key, value in timezonesAbb.items():
        for abb in value:
            if abb == timezone.upper():
                tz = pytz.timezone(key)
                current_time = datetime.now(tz).time().strftime("%#I:%M%p") # MIGHT HAVE TO CHANGE TO %-I:%M%p if hosted on UNIX
    if current_time == None:
        return "Error"
    else:
        return current_time


def convert_time(time, timezone_from, timezone_to):
    split = time.split(":")
    hours = int(split[0])
    right = str(split[1])
    right_split = re.findall('(\d+|[A-Za-z]+)', right)
    minutes = int(right_split[0])
    am_pm = right_split[1].upper()
    if am_pm == "PM":
        hours += 12
    if hours == 24:
        hours -= 12

    if hours == 12 and am_pm == "AM":
        hours -= 12

    for key, value in timezonesAbb.items():
        for abb in value:
            if abb == timezone_from.upper():
                tz_from = pytz.timezone(key)
            if abb == timezone_to.upper():
                tz_to = pytz.timezone(key)
    local = datetime.now(tz_from).replace(hour=hours, minute=minutes)
    converted = local.astimezone(tz_to)
    print(local.time().strftime("%#I:%M%p"))
    print(converted.time().strftime("%#I:%M%p"))
    return converted.time().strftime("%#I:%M%p")

def temp_convert(temp, temp_from, temp_to):
    if temp_from.upper() == "C" and temp_to.upper() == "F":
        new_temp = (float(temp) * (9/5)) + 32
        return f'{"%.2f" % new_temp} F'
    elif temp_from.upper() == "F" and temp_to.upper() == "C":
        new_temp = (float(temp) - 32) * (5/9)
        return f'{"%.2f" % new_temp} C'
    else:
        return "Usage: To convert between different temperature units, type !temp [temperature] [temperature unit given] [temperature unit to convert to] " \
               "(Eg. to convert from 23 Celsius to Fahrenheit, type !temp 23 C F)"





app = Flask(__name__)


@app.route('/timezone')
def get_timezone():
    given_timezone_from = request.args.get('timezone_from')
    given_timezone_to = request.args.get('timezone_to')
    given_time = request.args.get('time')
    try:
        if given_time is None or given_timezone_to is None:
            time = str(get_current_time(given_timezone_from))
            return time
        else:
            converted_time = str(convert_time(given_time, given_timezone_from, given_timezone_to))
            return converted_time
    except:
        return "Usage: For getting a time in a specific timezone, " \
               "type !timezone &lttimezone abbreviation>. (Eg. !timezone CST) - " \
               "To convert a time from one timezone to another, type !timezone &lttime> &lttimezone from> &lttimezone to> " \
               "(Eg. to convert a time from CST to PST, type !timezone 7:30pm CST PST)"

@app.route('/temperature')
def convert_temp():
    temp = request.args.get('temp')
    temp_from = request.args.get('temp_from')
    temp_to = request.args.get('temp_to')
    message = "Usage: To convert between different temperature units, type !temp [temperature] [temperature unit given] [temperature unit to convert to] " \
              "(Eg. to convert from 23 Celsius to Fahrenheit, type !temp 23 C F)"

    try:
        result = temp_convert(temp, temp_from, temp_to)
        return result
    except:
        return message


app.run()
