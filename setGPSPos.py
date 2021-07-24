#!/usr/bin/env python3
import sys
import math
import glob
import fnmatch

try:
    import gpxpy
except ModuleNotFoundError as me:
    print(me.msg.replace("No module named", "Please install"))
    print("by calling:")
    print(me.msg.replace("No module named", "pip install"))
    sys.exit(1)

files = []

# list of (filepattern, gpx-symbol)
patterns = [("*.jpg", "photo"), ("*.3gp", "speech")]

intToBase64 = [ 
        'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
        'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
        'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
        'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
        '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '_', '~'
        ]

# ported from https://github.com/osmandapp/OsmAnd/blob/master/OsmAnd-java/src/main/java/net/osmand/util/MapUtils.java#L411
def decodeAndGetWPT(filename, symbol=None):
    s = filename.split('.')[0]
    s = s.replace("@", "~");

    i = 0
    x = 0
    y = 0
    z = -8

    i = 0
    for c in s:
        try:
            digit = intToBase64.index(c)
        except ValueError:
            break
        i += 1
        x <<= 3
        y <<= 3
        for j in range(2, -1, -1):
            print(j)
            x |= 0 if ((digit & (1 << (j + j + 1))) == 0) else (1 << j)
            y |= 0 if ((digit & (1 << (j + j))) == 0) else (1 << j)
        z += 3;
    lon = x * math.pow(2, 2 - 3 * i) * 90. - 180
    lat = y * math.pow(2, 2 - 3 * i) * 45. - 90
    
    if (i < len(s) and s[i] == '-'):
        z -= 2
    i += 1

    if (i < len(s) and s[i] == '-'):
        z += 1

    w = gpxpy.gpx.GPXWaypoint(latitude=lat, longitude=lon, elevation=z, name=filename)
    w.link = filename
    if symbol:
        w.symbol = symbol
    return w


for p in patterns:
    files.extend(glob.glob(p[0]))

gpx = gpxpy.gpx.GPX()

for f in files:
    for p in patterns:
        if fnmatch.fnmatch(f,p[0]):
            gpx.waypoints.append(decodeAndGetWPT(f,p[1]))

open("avnotes.gpx", 'w').write(gpx.to_xml())
