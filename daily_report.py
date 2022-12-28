import os
import argparse
from datetime import datetime, timedelta
import pytz
from credentials import *

parser = argparse.ArgumentParser()
parser.add_argument('-d', dest='date', type=str, help='Enter date in format MM-DD-YYYY')
args = parser.parse_args()

# Get date for report, default to yesterday
if args.date:
    month, day, year = map(int, args.date.split('-'))
else:
    yesterday = datetime.now() - timedelta(1)
    yesterday = datetime.strftime(yesterday, '%m-%d-%Y')
    month, day, year = map(int, yesterday.split('-'))
dt = datetime(year, month, day)
dt = dt.astimezone(pytz.timezone('US/Eastern'))

# Get creds
user, pwd = decrypt_user_and_pwd()

# Run report
from sense_energy import Senseable
sense = Senseable(None, None, 30)
sense.authenticate(user, pwd)
sense.update_trend_data(dt)
print ("Start time:", sense.start_time)
print ("End time:", sense.end_time)
print ("Daily Solar:", sense.daily_production, "KWh")
print ("Daily Consumption:", sense.daily_usage, "KWh")
print ("From Grid:", sense.daily_from_grid, "KWh")
print ("To Grid:", sense.daily_to_grid, "KWh")
print ("Powered by Solar:", sense.daily_solar_powered, "%")
print ("Net Production:", sense.daily_net_production, "KWh")
print ("Production pct:", sense.daily_production_pct, "%")

# Save report
if not os.path.exists('daily-report.csv'):
    f = open('daily-report.csv', 'w')
    f.write("Date,Production,Usage,From Grid,To Grid,Powered by Solar,Net,Production Pct\n")
else:
    f = open('daily-report.csv', 'a')

f.write("{},{},{},{},{},{},{},{}\n".format(
        datetime.strftime(dt, '%Y-%m-%d'),
        sense.daily_production,
        sense.daily_usage,
        sense.daily_from_grid,
        sense.daily_to_grid,
        sense.daily_solar_powered,
        sense.daily_net_production,
        sense.daily_production_pct
    )
)
f.close()
