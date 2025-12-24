import krpc
import time as t
import json

conn = krpc.connect(name='Data recording')
vessel = conn.space_center.active_vessel
array_speed = []
array_time = []
array_hight = []
time = 0
while True:
    speed = vessel.flight(vessel.orbit.body.reference_frame).speed
    hight = vessel.flight().surface_altitude
    array_hight.append(hight)
    array_speed.append(speed)
    array_time.append(time)

    t.sleep(1)
    time+=1
    if time > 1000:
        break

data = {
    "time": array_time,
    "speed": array_speed,
    "hight": array_hight}

with open("data_from_ksp.json", "w") as f:
    json.dump(data, f)
