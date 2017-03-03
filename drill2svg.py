#!/usr/bin/python

from sys import argv

# console argument evaluation
if len(argv) < 2:
    print "Nope. That's not how to use this script."
    exit()

filename_read = argv[1]

if len(argv) >= 3:
    filename_write = argv[2]
else:
    filename_write = filename_read[:-4]+".svg"

# import drill file
print "Importing Excellon / IPC-NC-349 from '"+filename_read+"' ..."
drillfile = open(filename_read).read().replace("\r","").split("\n")

# create SVG
svg = "<svg>\n"

# diameter in mm
tool = 1
x = 0
y = 0

# append drill hole to SVG
def add_circle(x, y, r):
    global svg
    svg += '<circle' \
            + ' cx="' + str(x) + '"' \
            + ' cy="' + str(y) + '"' \
            + ' r="'  + str(r) + '"' \
            + ' stroke="none" fill="red" />\n'
    print ".",

# lookup table for tool diameters
radius = []
def set_radius(t, r):
    while len(radius) <= t:
        radius.append(0)
    radius[t] = r

# parser for numbers, since they lack commata
def parse_number(s):
    if zero_mode == "LZ":
        # kept leading zeroes, append trailing zeroes
        while len(s) < digits_before_comma + digits_after_comma:
            s = s+"0"
    if zero_mode == "TZ":
        # kept trailing zeroes, append leading zeroes
        while len(s) < digits_before_comma + digits_after_comma:
            if s[0] == '-':
                s = '-0'+s[1:]
            else:
                s = "0"+s
    c = digits_before_comma
    if s[0] == '-':
        c += 1
    return float(s[:c]+'.'+s[c:])

# parse drillfile
for line in drillfile:
    # empty line
    if len(line) == 0:
        continue

    # file format
    if line.find("FORMAT=") > -1:
        p = line.find(':')
        digits_before_comma = int(line[p-1])
        print "Digits before comma: "+str(digits_before_comma)
        digits_after_comma  = int(line[p+1])
        print "Digits after comma:  "+str(digits_after_comma)

    # comment
    if line[0] == ';' or line[0] == '%':
        continue

    # number format
    if line[:6] == 'METRIC':
        zero_mode = line[7:]
        print "Zero mode: "+zero_mode

    # tool
    if line[0] == 'T':
        q = line.find('F')
        if q == -1:
            q = len(line)
        p = line.find('C')
        if p > -1:
            # configure tool
            n = int(line[1:min(p,q)])
            c = float(line[p+1:])
            set_radius(n, c)
            print "Tool "+str(n)+" diameter = "+str(c)+" mm"
        else:
            # switch tool
            try:
                tool = int(line[1:])
                print "Selected tool "+str(tool)+".",
            except:
                continue
            continue

    if line[0] == 'X':
        s = line[1:]
        p = line.find('Y')
        if p > -1:
            s = line[1:p]
        x = parse_number(s)
        if p > -1:
            y = parse_number(line[p+1:])
        add_circle(x, y, radius[tool])
        continue

    if line[0] == 'Y':
        y = parse_number(line[1:])
        add_circle(x, y, radius[tool])
        continue

svg += "</svg>"
print "Done."

# save to file
open(filename_write, 'w').write(svg)
print "SVG written to '"+filename_write+'".'
