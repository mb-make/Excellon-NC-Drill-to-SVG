#!/usr/bin/python

# import drill file
drillfile = open("Multi-Nutzen.TXT").read().replace("\r","").split("\n")

# create SVG
svg = ""

# diameter in mm
tool = 1
x = 0
y = 0

def add_circle(x, y, r):
    global svg
    svg += '<circle' \
            + ' cx="' + str(x/10000) + '"' \
            + ' cy="' + str(y/10000) + '"' \
            + ' r="'  + str(r) + '"' \
            + ' stroke="none" fill="red" />\n'

radius = [0.9000, 1.0000, 1.3000]

# parse drillfile
for line in drillfile:
    # empty line
    if len(line) == 0:
        continue

    # comment
    if line[0] == ';' or line[0] == '%':
        continue

    # change tool
    if line[0] == 'T':
        try:
            tool = int(line[1]+line[2])
        except:
            continue
        continue

    if line[0] == 'X':
        s = line[1:]
        p = line.find('Y')
        if p > -1:
            s = line[1:p]
        x = float(s)
        if p > -1:
            y = float(line[p+1:])
        add_circle(x, y, radius[tool-1])
        continue

    if line[0] == 'Y':
        y = float(line[1:])
        add_circle(x, y, radius[tool-1])
        continue

print "<svg>\n" \
    + svg \
    + "</svg>"
