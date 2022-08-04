
from geopy import distance, Point
from math import (
    degrees, radians,
    sin, cos, atan2
)
import pandas as pd

def calculate_initial_compass_bearing(pointA, pointB):

    if (type(pointA) != tuple) or (type(pointB) != tuple):
        raise TypeError("Only tuples are supported as arguments")

    lat1 = radians(pointA[0])
    lat2 = radians(pointB[0])

    diffLong = radians(pointB[1] - pointA[1])

    x = sin(diffLong) * cos(lat2)
    y = cos(lat1) * sin(lat2) - (sin(lat1)
            * cos(lat2) * cos(diffLong))

    initial_bearing = atan2(x, y)

    initial_bearing = degrees(initial_bearing)
    compass_bearing = round((initial_bearing + 360) % 360)

    return compass_bearing
file_name = input("Enter your cords file: ").replace("\"","");
l = int(input("Enter your rect length in meters: "))
w = int(input("Enter your rect width in meters: "))
df = pd.read_csv(file_name)
right_lat = df.loc[df['Circle']==1]['Lat'].mean()
right_long = df.loc[df['Circle']==1]['Lon'].mean()
center_lat = df.loc[df['Circle']==2]['Lat'].mean()
center_long = df.loc[df['Circle']==2]['Lon'].mean()
center = (center_lat,center_long)
right = (right_lat,right_long)
brn_original= calculate_initial_compass_bearing(center, right)

offsets = [-15,-10,-5,0,5,10,15]
for offset in offsets:
    brn = (brn_original + offset) % 360
    length = l/1000.0
    width = w/1000.0
    half_length = length/2.0
    half_width = width/2.0

    middle_top = distance.distance(kilometers=half_width).destination(Point(center_lat,center_long), brn - 90)
    middle_bottom = distance.distance(kilometers=half_width).destination(Point(center_lat,center_long), brn + 90)
    top_right = distance.distance(kilometers=half_length).destination(middle_top, brn)
    top_left = distance.distance(kilometers=half_length).destination(middle_top, brn + 180)
    bottom_right = distance.distance(kilometers=half_length).destination(middle_bottom, brn)
    bottom_left = distance.distance(kilometers=half_length).destination(middle_bottom, brn + 180)
    f = open("polygon"+str(offset)+".poly", "w")
    f.write("#Generated Box!\n")
    f.write(str(top_right.latitude)+ " " + str(top_right.longitude) +"\n")
    f.write(str(bottom_right.latitude)+ " " + str(bottom_right.longitude)+"\n")
    f.write(str(bottom_left.latitude)+ " " + str(bottom_left.longitude)+"\n")
    f.write(str(top_left.latitude)+ " " + str(top_left.longitude)+"\n")
    f.close()


