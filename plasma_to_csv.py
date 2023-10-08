import pathlib as pl 
import sys
import util

inp = sys.argv[1]


out = sys.argv[2]
dataset_raw = pl.Path(inp).read_text()

lines = []

for l in dataset_raw.splitlines():
    s = l.split()
    time_val = util.abs_time(int(s[0]), int(s[1]), int(s[2]), float(s[3]))
    lines.append({
        "time" : time_val,
        "year" : int(s[0]),
        "day" : int(s[1]),
        "hour" : int(s[2]),
        "minute" : float(s[3]),
        "field_density" : float(s[4]),
        "plasma_temp" : float(s[5]),
        "proton_density" : float(s[6])
    })

output = open(out, "w")



output.write("time,year,day,hour,minute,field_density,plasma_temp,proton_density\n")


for entry in lines:
    output.write(f" {entry['time']}, {entry['year']}, {entry['day']}, {entry['hour']}, {entry['minute']}, {entry['field_density']}, {entry['plasma_temp']}, {entry['proton_density']}\n")

output.close()
