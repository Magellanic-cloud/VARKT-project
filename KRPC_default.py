import time
import pyautogui
import krpc
import json
import numpy as np


# Константы, от которых надо избавиться
Q_limit = 8000
orbit_altitude = 80000
launch_time = None
time_passed = None

conn = krpc.connect()
vessel = conn.space_center.active_vessel 

earth = conn.space_center.bodies['Earth']


# Земля и Луна - для дальнейших маневров 
# earth = conn.space_center.bodies['Kerbin']
# moon = conn.space_center.bodies['Mun']

data = {
    'time': [],
    'altitude': [],
    'speed': []
}  

def processing_data():
    global launch_time
    global time_passed

    flight = vessel.flight(vessel.orbit.body.reference_frame)
    Q = 0.5 * flight.atmosphere_density * flight.speed**2
    data['time'].append(round(time.time() - launch_time))
    data['altitude'].append(round(flight.mean_altitude, 2))
    data['speed'].append(round(flight.speed, 2))

    if time.time() - launch_time > time_passed + 1:
        time_passed += 1

    '''
    # В случае, когда слишком высокое давление, чтобы ракету не разорвало
    if Q > Q_limit:
        vessel.control.throttle *= 0.9
    else:
        if vessel.control.throttle < 0.8:
            vessel.control.throttle *= 1.25
        else:
            vessel.control.throttle = 1.0
    '''

def stage_block():
    # Включаем/выключаем блокировку автоматической отстыковки ступеней
    time.sleep(0.5)
    pyautogui.hotkey('alt', 'l')
    time.sleep(0.5)
    processing_data()

# Начало программы: подготовка ракеты-носителя Сатурн 5 к корректному запуску
def pre_launch():

    # Включаем автопилот с курсом:
    # АЗИМУТ: 90 (на Восток) - добавляем к ракете скорость вращения планеты (headling)
    # ТАНГАЖ: 90 - вектор скорости ракеты направлен в зенит (pitch)

    vessel.control.sas = False
    vessel.control.rcs = False
    vessel.auto_pilot.engage()
    vessel.auto_pilot.target_pitch_and_heading(90, 90)
    vessel.control.activate_next_stage()


    # Постепенная раскрутка турбонасосов и разгорание факела двигателей F-1 ступени S-IC 
    # По техническим характеристикам на это уходило 2-3 секунды

    turning_engines_on = time.time()
    while time.time() - turning_engines_on < 2.5:
        if time.time() - turning_engines_on < 2.5:
            vessel.control.throttle = (time.time() - turning_engines_on) / 2.5
        else:
            vessel.control.throttle = 1
            break

    # Вес (P = m * g)
    weight = vessel.mass * vessel.orbit.body.surface_gravity

    # Отношение силы тяги при взлете ракеты к её весу по технической договоренности оставили 1,2 : 1
    # После тестирования выяснилось, ракета в KSP не способна развить такую тягу до взлёта, поэтому я уменьшил её до 1,16
    while vessel.thrust / weight < 1.16:
        pass

    print(f"Time after turning the engines on: {round(time.time() - turning_engines_on, 1)}")
    print(f"Launch thrust: {vessel.thrust / 10**6} MN")
    print(f"Launch weight: {weight / 10**6} MN")
    print(f"TWR: {vessel.thrust / weight}")

    vessel.control.activate_next_stage()

# Работа 1 ступени (S-IC)
def S_IC():
    global flight
    global time_passed

    stage_block()

    # Первые 10 секунд Аполлон летел строго вертикально
    # Т+0 - Т+10
    while time_passed < 10:
        processing_data()

    # Ступень работает, пока тяга ненулевая
    while  vessel.thrust > 0:

        # Изменение тангажа: тангаж = 90 - 90 * отношение текущей высоты к высоте орбиты
        # Изменение азимута: азимут = 90 - отношение времени от начала roll-программы к продолжительности поворота
        # Поворот (по азимуту) завершился на 73 градусах к 20-30 секундам после старта
        # Я взял конкретно к 30, но предварительно обнулил время для удобства 
        # Т+30 - Т+10 = 20 с

        target_pitch = 90 - 90 * (flight.mean_altitude - start_altitude) / (orbit_altitude - start_altitude)
        if time_passed < 20:
            target_roll = 90 - (time_passed - 10 / 20) * (90 - 73)
        else:
            target_roll = 73
        vessel.auto_pilot.target_pitch_and_heading(target_pitch, target_roll)
        processing_data()
    
    # Топливо в 1 ступени закончилось - отстыковка S-IC
    stage_block()
    vessel.control.activate_next_stage()

# Работа 2 ступени (S-II)
def S_II():
    global flight
    global time_passed
    global earth

    stage_block()

    # Надо дать время, чтобы ракета набрала ненулевую тягу
    time.sleep(1)

    # Ступень работает, пока не нулевая тяга
    while vessel.thrust > 0 :

        # Изменение тангажа: тангаж = 90 - 90 * отношение текущей высоты к высоте орбиты
        target_pitch = 90 - 90 * (flight.mean_altitude - start_altitude) / (orbit_altitude - start_altitude)
        vessel.auto_pilot.target_pitch_and_heading(target_pitch, 73)
        processing_data()

    # Топливо в 1 ступени закончилось - отстыковка S-II
    stage_block()
    vessel.control.activate_next_stage()
    vessel.control.activate_next_stage()
    stage_block()

    # Надо дать время, чтобы ракета набрала ненулевую тягу
    time.sleep(1)


    while flight.mean_altitude < orbit_altitude:

        # Изменение тангажа: тангаж = 90 - 90 * отношение текущей высоты к высоте орбиты
        target_pitch = 90 - 90 * (flight.mean_altitude - start_altitude) / (orbit_altitude - start_altitude)
        vessel.auto_pilot.target_pitch_and_heading(target_pitch, 73)
        processing_data()

    while flight.speed < earth.gravitational_parameter / (earth.equatorial_radius + flight.mean_altitude):
        vessel.auto_pilot.target_pitch_and_heading(0, 73)
        processing_data()


    reaching_orbit = time.time()

    while time.time() - reaching_orbit < 3:
        if time() - reaching_orbit < 3:
            vessel.control.throttle = (3 - time.time()) / 3
        else:
            vessel.control.throttle = 0
            break
        processing_data()
  

# Работа 3 ступени (S-IVB)
def S_IVB(*args):
    
    flight, orbit_altitude = args

    stage_block()

    target_pitch = flight.pitch

    # На момент работы 3 ступени Сатурн 5 примет горизонтальное положение
    while target_pitch > 0:

        # Изменение тангажа: тангаж = 90 - 90 * отношение текущей высоты к высоте орбиты
        target_pitch = (1 -  flight.mean_altitude / orbit_altitude) * 90
        vessel.auto_pilot.target_pitch_and_heading(target_pitch, 90)

        time.sleep(1)
        processing_data()

    # Выход на околоземную орбиту
    vessel.auto_pilot.target_pitch_and_heading(0, 90)

    # Разгон ракеты до космической скорости
    '''while flight.speed < (earth.gravitational_parameter / (earth.equatorial_radius + flight.mean_altitude))**0.5:
        time.sleep(1)
        processing_data()

    # Заглушка двигателей'''
    vessel.control.throttle = 0
    

# print(earth.angular_velocity(earth.orbital_reference_frame))

pre_launch()

launch_time = time.time()
time_passed = 0
flight = vessel.flight(vessel.orbit.body.reference_frame)
start_altitude = flight.mean_altitude

S_IC()
S_II()
S_IVB()

# Чтобы знать космическую скорость на орбите перед завершением программы
print(flight.speed)

# Печать собранных данных в json файл (временно здесь)
with open('orbit_entry.json', 'w') as f:
    json.dump(data, f, indent=2)
exit()

# Намек на продолжение программы
while True:
    pass