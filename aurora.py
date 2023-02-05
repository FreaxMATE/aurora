#!/usr/bin/python3

from PIL import Image
import matplotlib.pyplot as plt
import sys
import pandas as pd
from matplotlib.dates import DateFormatter
from datetime import datetime, date, time, timezone, timedelta
import numpy as np
import matplotlib.dates as mdates
from matplotlib.axis import Axis  

class Aurora:

    starttime = time(15, 0)
    endtime = time(8, 40)
    duration = datetime.combine(date(2021, 11, 2), endtime) - datetime.combine(date(2021, 11, 1), starttime)
    #totaltime = timedelta()
    x_start = 690 # 14:00
    x_end = 4450  # 7:40
    y_start = 220
    y_end = 18350
    # x_start = 100
    # x_end = 660
    # y_start = 31
    # y_end = 2550
    x_range = range(x_start, x_end)
    y_range = range(y_start, y_end)
    n_green_pixels = [0]

    def __init__(self, filepath):
        print(self.x_range)
        self._analyze(filepath)

    def _analyze(self, filepath):
        image = Image.open(filepath)
        pixels = image.load()
        for i, x in enumerate(self.x_range):
            for y in self.y_range:
                if self._green_enough(pixels[x, y]):
                    self.n_green_pixels[i] += 1
            self.n_green_pixels.append(0)
        self.n_green_pixels.pop(-1)

        # plotting code
        # time equivalent for one pixel
        # t_pixel = (60*self.duration.hours + self.duration.minutes)/(x_end-x_start)
        timerange = np.linspace(0, self.duration.seconds/60, len(self.n_green_pixels))
        t = [datetime.combine(date(2021, 11, 1), self.starttime) + timedelta(minutes=i) for i in timerange]
        print(t)
        fig, axes = plt.subplots()
        plt.title('Aurora occurrences in November 2021')
        axes.plot(t, self.n_green_pixels, color='tab:green', lw=1)
        xformatter = mdates.DateFormatter('%H:%M')
        Axis.set_major_formatter(axes.xaxis, xformatter)
        plt.gcf().autofmt_xdate()
        axes.set_xlabel(r'$Time$ ' + r'$t$')
        axes.set_ylabel(r'Aurora Density Coefficient (Number of green pixels)')
        plt.savefig('green.png', dpi=600)

    def _green_enough(self, pixel):
        if pixel[0] < 120 and pixel[1] > 100 and pixel[2] < 120:
            if pixel[1] > 1.1*(pixel[0]+pixel[2])/2:
                return True
        return False



if __name__=="__main__":
    aurora = Aurora(sys.argv[1])

