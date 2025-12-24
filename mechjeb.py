import krpc
import math
import json

def processing_data():
    global vessel, flight, start_time, time_passed, data, earth, conn, ascent

    pitch = vessel.flight(vessel.surface_reference_frame).pitch
    gravitational_acceleration = earth.gravitational_parameter / (earth.equatorial_radius + flight.mean_altitude)**2
    vertical_acceleration = vessel.thrust*math.sin(math.radians(pitch))/vessel.mass - gravitational_acceleration

    if conn.space_center.ut - start_time > time_passed + 1:

        time_passed += 1

        data['time'].append(time_passed)
        data['altitude'].append(round(flight.mean_altitude, 2))
        data['speed'].append(round(flight.speed, 2))
        data['pitch'].append(round(pitch, 2))
        data['vertical acceleration'].append(round(vertical_acceleration, 2))

        print(
            f"t: {time_passed:>3} c  "
            f"h: {flight.mean_altitude:>7.2f} м\t"
            f"V: {flight.speed:>7.2f} м/с"            
        )

data = {
    'time' : [],
    'altitude' : [],
    'speed' : [],
    'pitch' : [],
    'vertical acceleration' : []
}

conn = krpc.connect()

sc = conn.space_center
vessel = sc.active_vessel
flight = vessel.flight(vessel.orbit.body.reference_frame)
mj = conn.mech_jeb
ascent = mj.ascent_autopilot
earth = sc.bodies['Kerbin']

ascent.desired_orbit_altitude = 80000
ascent.desired_inclination = 6

ascent.force_roll = True
ascent.vertical_roll = 90
ascent.turn_roll = 90

ascent.autostage = True

ascent.enabled = True

start_time = conn.space_center.ut
time_passed = 0

sc.active_vessel.control.activate_next_stage() 

enabled_stream = conn.stream(getattr, ascent, "enabled")
enabled_stream.rate = 1

while ascent.status != 'Выключен':    
    processing_data()

with open("ksp_data.json", "w") as f:
    json.dump(data, f, indent = 2)

ascent.enabled = False
conn.close()