import matplotlib.pyplot as plt
import matplotlib as mpl
import math
import pandas as pd
import numpy as np
import openpyxl
import random
# 엑셀 파일 오픈
wb = openpyxl.load_workbook('trackresult.xlsx')
# 맨 앞 시트 추출
sheet = wb.worksheets[0]
# 입출력 데이터 선언
time_data = []


class dataset:
    def __init__(self):
        self.input = []
        self.output = []
        self.noise = []
        self.noise_output = []
        self.velocity = []

    def make_noise_output(self):
        for i in range(len(self.noise)):
            self.noise_output.append(self.noise[i] + self.output[i])


def draw_plot(x, y, x_limit, y_limit, x_label, y_label):
    flg, ax = plt.subplots()
    x = np.array(x)
    y = np.array(y)
    ax.plot(x, y)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    plt.show()


def data_setting(x, y):
    global sheet, time_data
    data = []
    for row in sheet.rows:
        data.append([row[0].value, row[1].value,
                     row[2].value, row[3].value, row[4].value])
    del data[0]
    past_data = [0, 0, 0]  # 속도, x,y
    for row in data:
        time_data.append(row[0])
        x.output.append(row[1])
        y.output.append(row[2])
        y.input.append(row[3])
        x.input.append(row[4])

        if len(time_data) == 1:
            x.velocity.append(0)
            y.velocity.append(0)
        else:
            v = math.sqrt(pow((row[1] - past_data[1]), 2) +
                          pow((row[2] - past_data[2]), 2))/(row[0] - past_data[0])
            x.velocity.append(v)
            y.velocity.append(v)
            past_data = [row[0], row[1], row[2]]
    return


def movement_error(v):
    # 조사가 부족해서 임의로 줘 보도록 하겠다.  0m/s 5m/s 까지는 최대 0.1의 오차를 선형으로 준다고 하고, 5m/s를 넘어가면 오차의 제곱만큼 늘려보자
    mean = 0
    given_error = 0.1
    if v <= 5:
        mean = given_error*v/5
    elif v > 5:
        mean = 0.1 + pow(((v-5)*0.1), 2)
    error = np.random.normal(0, 0.1, 1)
    error = error[0] * mean
    return error


def make_noise(now_data):
    global time_data
    # 절대위치정보 기반 Lidar-INS 센서의 외부 파라미터 캘리브레이션 기법 홍 범 진1) · 나 수 현2) · 백 승 호*2) · 박 상 덕2) UST 로보틱스 및 가상공학1)·한국생산기술연구원2)
    # 캘리브레이션 결과 정밀측량한 기준점과 Lidar 센서를 통해 획득한 데이터간 오차는 평균 0.09m이고, 표준편차 4.2임을 확인하였다
    # 다만 현 조건에서 4.2는 너무 가혹한 수치이다. (참고로 논문에서의 실험은 실외에서 이루어졌다.)  실내에서 주행한다고 생각하고 표준편차를 5배정도 줄여 0.84로 데이터 셋을 만들어보겠다.
    calibrate_errors = np.random.normal(0.09, 0.84, len(time_data))
    # 또한 이동 속도가 빨라질 수록 오차가 더 커진다고 하니, 최대 측정 속도를 5m/s 로 두고 이동속에 따른 가중치를 줘보자.

    for i in range(len(time_data)):
        move_error = movement_error(now_data.velocity[i])
        now_data.noise.append(move_error + calibrate_errors[i])
    now_data.make_noise_output()
    return


if __name__ == "__main__":
    x = dataset()
    y = dataset()
    data_setting(x, y)
    make_noise(x)
    make_noise(y)
    draw_plot(time_data, x.input, 0, 0, "time(sec)", "x-axis(m)")
    draw_plot(time_data, y.input, 0, 0, "time(sec)", "y-axis(m)")
    draw_plot(time_data, x.output, 0, 0, "time(sec)", "x-axis(m)")
    draw_plot(time_data, y.output, 0, 0, "time(sec)", "y-axis(m)")
    draw_plot(time_data, x.noise_output, 0, 0, "time(sec)", "x-axis(m)")
    draw_plot(time_data, y.noise_output, 0, 0, "time(sec)", "y-axis(m)")
