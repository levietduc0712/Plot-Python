from pylab import *
import csv, os
import math
import matplotlib.pyplot as plt
import numpy as np
import statistics as st

# constant definitions
STANDING_KMH = 10.0
SPEEDING_KMH = 50.0
NMI = 1852.0
D2R = math.pi/180.0

def read_csv_file(filename):
    """Reads a CSV file and return it as a list of rows."""

    data = []
    for row in csv.reader(open(filename)):
        data.append(row)
    return data

def process_gps_data(data):
    """Processes GPS data, NMEA 0183 format.

Returns a tuple of arrays: latitude, longitude, velocity [km/h], 
time [sec] and number of satellites. 
See also: http://www.gpsinformation.org/dale/nmea.htm.
    """

    latitude    = []
    longitude   = []
    velocity    = []
    t_seconds   = []
    num_sats    = []

    for row in data:
        if row[0] == '$GPGSV':
            num_sats.append(float(row[3]))
        elif row[0] == '$GPRMC': 
            t_seconds.append(float(row[1][0:2])*3600 + \
                float(row[1][2:4])*60+float(row[1][4:6]))
            latitude.append(float(row[3][0:2]) + \
                float(row[3][2:])/60.0)
            longitude.append((float(row[5][0:3]) + \
                float(row[5][3:])/60.0))
            velocity.append(float(row[7])*NMI/1000.0)

    return (np.array(latitude), np.array(longitude), \
        np.array(velocity), np.array(t_seconds), np.array(num_sats))

# process GPS data
filename = 'GPS-2008-05-30-09-00-50.csv'
y = read_csv_file(filename)
(lat, long, v, t, sats) = process_gps_data(y)

# translate spherical coordinates to Cartesian
py = (lat-min(lat))*NMI*60.0
px = (long-min(long))*NMI*60.0*np.cos(D2R*lat)

# find out when standing, speeding or cruising
Istand = np.where(v < STANDING_KMH)
Ispeed = np.where(v > SPEEDING_KMH)
Icruise = np.where((v >= STANDING_KMH) & (v <= SPEEDING_KMH))

# left side, GPS location graph
plt.figure()
plt.subplot(1, 2, 1)

# longitude values go from right to left, 
# we want increasing values from left to right
plt.gca().axes.invert_xaxis()

plt.plot(px, py, 'b', label=' Cruising', linewidth=3)
plt.plot(px[Istand], py[Istand], 'sg', label=' Standing')
plt.plot(px[Ispeed], py[Ispeed], 'or', label=' Speeding!')

# add direction of travel
for i in range(0, len(v), len(v)//10-1): 
    plt.text(px[i], py[i], ">>>", \
        rotation=np.arctan2(py[i+1]-py[i], -(px[i+1]-px[i]))/D2R, \
        ha='center')

# legends and labels
plt.title(filename[:-4])
plt.legend(loc='upper left')
plt.xlabel('east-west (meters)')
plt.ylabel('south-north (meters)')
plt.grid()
plt.axis('equal')

# top right corner,  speed graph
plt.subplot(2, 2, 2)

# set the start time as t[0]; convert to minutes
t = (t-t[0])/60.0
plt.plot(t, v, 'k')

# plot the standing and speeding threshold lines
plt.plot([t[0], t[-1]], [STANDING_KMH, STANDING_KMH], '-g')
plt.text(t[0], STANDING_KMH, \
    " Standing threshold: " + str(STANDING_KMH))
plt.plot([t[0], t[-1]], [SPEEDING_KMH, SPEEDING_KMH], '-r')
plt.text(t[0], SPEEDING_KMH, \
    " Speeding threshold: "+ str(SPEEDING_KMH))
plt.grid()

# legend and labels
plt.title('Velocity')
plt.xlabel('Time from start of file (minutes)')
plt.ylabel('Speed (Km/H)')

# right side corner, statistics data
plt.subplot(2, 2, 4)

# remove the frame and x/y axes. we want a clean slate
plt.axis('off')

# generate an np.array of strings to be printed
Total_distance  = float(sum(np.sqrt(np.diff(px)**2+np.diff(py)**2))/1000.0)
Stand_time  = (len(np.transpose(Istand))/60.0)
Cruise_time = (len(np.transpose(Icruise))/60.0)
Speed_time  = (len(np.transpose(Ispeed))/60.0)
Stand_per   = 100*len(np.transpose(Istand))/len(v)
Cruise_per  = 100*len(np.transpose(Icruise))/len(v)
Speed_per   = 100*len(np.transpose(Ispeed))/len(v)
stats=['Statistics', \
'%s' % filename, \
'Number of data points: %d' % len(y), \
'Average number of satellites: %d' % st.mean(sats), \
'Total driving time: %.1f minutes:' % (len(v)/60.0), \
'    Standing: %.1f minutes (%d%%)' % \
(Stand_time, Stand_per), \
'    Cruising: %.1f minutes (%d%%)' % \
(Cruise_time, Cruise_per), \
'    Speeding: %.1f minutes (%d%%)' % \
(Speed_time, Speed_per), \
'Average speed: %d km/h' % st.mean(v), \
'Total distance traveled: %.1f Km' % Total_distance ]

# display statistics information
for index, stat_line in enumerate(reversed(stats)):
    plt.text(0, index, stat_line, va='bottom') 

# draw a line below the "Statistics" text
plt.plot([index-.2, index-.2])

# set axis properly so all the text is displayed
plt.axis([0, 1, -1, len(stats)])

plt.show()
