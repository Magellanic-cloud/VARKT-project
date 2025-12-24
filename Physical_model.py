import math
import json
import matplotlib.pyplot as plt

time = 0 #Счётчик времени
t1 = 2*60+15 #Время работы 1-ой ступени (с)
t2 = 2*60+25 #Время работы 2-ой ступени (с)
t3 = 165
h0 = 0 #Начальная высота
g0 = 9.81 #начальное ускорение свободного падения
R_Kerbin = 600*10**3 #Радиус Кербина в метрах
Cx = 0.5 #коэф аэродинамического сопротивления


M1 = 516.5*10**3 #Масса 1-ой ступени ракеты (кг)
M2 = 150*10**3 #Масса 2-ой ступени ракеты (кг)
M3 = 57.7*10**3 #Масса 3-ей ступени ракеты (кг)
M_com_mod = 2.438*10**3 #Масса коммандного модуля (кг)
M_moon_mod = 1.887*10**3 #Масса лунного модуля (кг)
m0 = M1+M2+M3+M_com_mod+M_moon_mod #Общая начальная масса ракеты (кг)

I1 = 305 #Удельный импульс 1 ступени (с)
I2 = 265 #Удельный импульс 2 ступени (с)


#v1 = I1*g0*math.log((M1+M2+M3+M_com_mod+M_moon_mod)/(M2+M3+M_com_mod+M_moon_mod)) #скорость после отработки первой ступени
# v2 = I2*math.log((M2+M3+M_com_mod+M_moon_mod)/(M3+M_com_mod+M_moon_mod))
# v3 = I3*math.log((M3+M_com_mod+M_moon_mod)/(M_com_mod+M_moon_mod))
# print(v1)
F1 = 1.51*6418 * 10**3 #Сила тяги 1 ступени ракеты (Н)
F2 = 1.7*1204.5 * 10**3 #Сила тяги 2 ступени ракеты (Н)
# F3 = 1205.8 * 10**3

m_dot = F1 / (I1*g0) #Секундный массовый расход топлива для 1 ступени (кг/с)
# m_dot = (516.5 - 216.3)*10**3/t1
delta_time = 1 #Возьмём изменение времени равное 1 секунде
v0 = 0 #Начальная скорость (м/с)

# Ae = 0.1
diam = 10.1 #Диаметр (м)
P0 = 101325 #Давление атмосферы (Па)
po_0 = 1.225 #начальная плотность атмосферы (кг/м^3)
S = math.pi*diam**2/4 #Площадь поперечного сечения корабля (м^2)

array_time_first = [] #храним время для 1-ой ступени
array_speed_first = [] #храним скорость для 1-ой ступени
array_hight_first = [] #храним высоту для 1-ой ступени
M_Kerbina = 5.29*10**22
G = 6.67 * 10**(-11)
#Действие 1-ой ступени ракеты
sp = []
alpha = math.pi/2
# print(math.degrees(math.asin(math.sin(alpha))))
omega = math.pi / (3*t1)
# print(g0*m0)
# print(F1/(g0*m0))

while time <= t1:
    if time == 0:
        hi = h0
        vi = v0
        gi = g0
        mi = m0
        po_i = po_0
        time += delta_time
        delta_h = h0
        Pi = P0
        I1_i = I1
        a_s = F1/m0 - gi
        alpha_i = alpha
        v_test = 0
        vx = 0
        vy = 0
        v_prime = 0
        continue
    
    
    # #print(hi)
    # # I1_i = I1_vac - (Ae*P0/(m_dot*g0))
    time+=delta_time
    gi = g0*(R_Kerbin**2/(R_Kerbin+hi)**2)
    # # print(gi)
    # # Pi = P0*math.exp(-hi/H)
    po_i = po_0*math.exp(-po_0*gi*hi/P0) #барометрическая уравнение для плотности
    # ai = (Cx*S/2) * (po_i*(vi**2)/mi)
    # mi_prev = mi
    mi = mi - m_dot*delta_time
    # # vi = vi + I1*g0*math.log(mi_prev/mi)-ai*delta_time-gi*delta_time
    if alpha_i - omega*delta_time >= 0:
        alpha_i = alpha_i - omega*delta_time
    ax = F1*math.cos(alpha_i) / mi - (Cx*S/2) * (po_i*(v_prime**2)/mi) * math.cos(alpha_i)
    ay = F1*math.sin(alpha_i) / mi - gi - (Cx*S/2) * (po_i*(v_prime**2)/mi) * math.sin(alpha_i)
    vx += ax*delta_time
    vy += ay*delta_time
    delta_h = vy*delta_time
    hi = hi + delta_h
    v_prime = (vy**2 + vx**2)**0.5

    array_time_first.append(time)
    array_speed_first.append(v_prime)
    array_hight_first.append(hi)


m_dot = F2 / (I2*g0) #Обновляем секундный массовый расход топлива, теперь для 2-ой ступени (кг/с)
alpha_i = 90- 90*(hi/80_000)

m0 -= M1 #1-ая ступень отработала, вычитаем её массу
g1 = gi
omega = 0



array_transfer_time = []
array_transfer_speed = []
array_transfer_hight = []
time_transfer = 0
while vy >= 0 and time < 235:
    
    time+=delta_time
    ax = - (Cx*S/2) * (po_i*(v_prime**2)/mi) * math.cos(alpha_i)
    ay = - gi - (Cx*S/2) * (po_i*(v_prime**2)/mi) * math.sin(alpha_i)
    vx = vx
    vy += ay*delta_time
    delta_h = vy*delta_time
    hi = hi + delta_h
    v_prime = (vy**2 + vx**2)**0.5

    array_time_first.append(time)
    array_transfer_hight.append(hi)
    array_transfer_speed.append(v_prime)



array_speed_second = [] #храним скорость для 2-ой ступени
array_time_second = [] #храним время для 2-ой ступени
array_hight_second = [] #храним высоту для 2-ой ступени


#Действие 2-ой ступени ракеты
while time <= 310:
    time+=delta_time
    gi = g0*(R_Kerbin**2/(R_Kerbin+hi)**2)
    alpha_i = math.radians(90 - 90*(hi/80_000))
    po_i = po_0*math.exp(-po_0*gi*hi/P0)
    mi = mi - m_dot*delta_time
    ax = F2*math.cos(alpha_i) / mi#- (Cx*S/2) * (po_i*(v_prime**2)/mi) * math.cos(alpha_i)
    ay = F2*math.sin(alpha_i) / mi - gi#- (Cx*S/2) * (po_i*(v_prime**2)/mi) * math.sin(alpha_i)
    
    vx += ax*delta_time
    if hi < 70_000:
        vy += (ay*delta_time)
    print(vx, vy)
    # if vy > 0:
    #     vy += ay*delta_time
    # else:
        
    # print(vy)
    # print(vx)
    delta_h = vy*delta_time+ay*delta_time**2/2
    hi = hi + delta_h
    v_prime = (vy**2 + vx**2)**0.5

    #Сохранение данных
    array_speed_second.append(v_prime)
    array_time_second.append(time)
    array_hight_second.append(hi)


# print(math.degrees(math.asin(math.sin(alpha_i))))

# h0 = array_hight_second[-1] #Обновляем начальную высоту, делая ее равной последней достигрнутой при работе 1-ой ступени
# v0 = array_speed_second[-1] #Обновляем начальную скорость, делая ее равной последней достигрнутой при работе 1-ой ступени
# m_dot = F3 / I3 #Обновляем секундный массовый расход топлива, теперь для 2-ой ступени (кг/с)
# m0-=M2
# array_speed_third = [] #храним скорость для 2-ой ступени
# array_time_third = [] #храним время для 2-ой ступени
# array_hight_third = [] #храним высоту для 2-ой ступени
  
# while time < t1+t2+t3:
#     if time == t1+t2+1:
#         hi = h0
#         vi = v0
#         time += delta_time
#         mi = m0
#         gi = g0
#         continue
#     hi = hi + delta_h
#     time+=delta_time
#     gi = g0 * (R_Kerbin**2)/(R_Kerbin + hi)**2
#     #alpha_i = alpha_i + omega*delta_time
#     mi_prev = mi
#     mi = mi - m_dot*delta_time
#     vi = vi + I3*math.log(mi_prev/mi)-gi*delta_time#*math.cos(alpha_i)
#     delta_h = vi*delta_time
#     #Сохранение данных
#     array_speed_third.append(vi)
#     array_time_third.append(time)
#     array_hight_third.append(hi)


#Сохранение данных в json файл
data = {
    "time": array_time_first+array_transfer_time+array_time_second,#+array_time_third,
    "altitude": array_hight_first+array_transfer_hight+array_hight_second,#+array_hight_third,
    "speed": array_speed_first+array_transfer_speed+array_speed_second#+array_speed_third,
    }

with open("data.json", "w") as file:
    json.dump(data, file)

#Вывод графиков
# plt.subplot(2, 1, 1)
# plt.plot(array_time_first+array_time_second+array_time_third, array_hight_first+array_hight_second+array_hight_third)
# plt.title('Высота график')

# plt.subplot(2, 1, 2)
# plt.plot(array_time_first+array_time_second+array_time_third, array_speed_first+array_speed_second+array_speed_third)
# plt.title('Скорость график')

# plt.tight_layout()
# plt.show()