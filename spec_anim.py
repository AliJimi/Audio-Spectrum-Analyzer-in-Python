'''
pip install pyAudio may not work
Instead download and install a wheel from here:
https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio

or use: 

pip install pipwin
pipwin install pyaudio

pipwin is like pip, but it installs precompiled Windows binaries provided by Christoph Gohlke.
'''

# to display in separate Tk window
import matplotlib
import pyaudio
import os
import struct
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
from scipy.fftpack import fft
import time
from tkinter import TclError

import settings
from audio_input import microphone_stream

matplotlib.use('TkAgg')


# Counts the frames
# why the list? https://stackoverflow.com/questions/25040323/unable-to-reference-one-particular-variable-declared-outside-a-function
count = [0]

# ------------ Audio Setup ---------------
# constants

# pyaudio class instance
pyaudio_instance = pyaudio.PyAudio()

# stream object to get data from microphone
stream = microphone_stream(pyaudio_instance)

# ------------ Plot Setup ---------------
fig, (ax1, ax2) = plt.subplots(2, figsize=(15, 7))
# variable for plotting
x = np.arange(0, 2 * settings.CHUNK, 2)  # samples (waveform)
xf = np.linspace(0, settings.RATE, settings.CHUNK)  # frequencies (spectrum)

# create a line object with random data
line, = ax1.plot(x, np.random.rand(settings.CHUNK), '-', lw=2)

# create semilogx line for spectrum, to plot the waveform as log not lin
line_fft, = ax2.semilogx(xf, np.random.rand(settings.CHUNK), '-', lw=2)

# format waveform axes
ax1.set_title('AUDIO WAVEFORM')
ax1.set_xlabel('samples')
ax1.set_ylabel('volume')
ax1.set_ylim(-settings.AMPLITUDE_LIMIT, settings.AMPLITUDE_LIMIT)
ax1.set_xlim(0, 2 * settings.CHUNK)
plt.setp(ax1, xticks=[0, settings.CHUNK, 2 * settings.CHUNK], yticks=[-settings.AMPLITUDE_LIMIT, 0, settings.AMPLITUDE_LIMIT])

# format spectrum axes
ax2.set_xlim(20, settings.RATE / 2)
print('stream started')


def on_close(evt):
    print("Closing")
    # calculate average frame rate
    frame_rate = count[0] / (time.time() - start_time)

    # Close the stream and terminate pyAudio
    stream.stop_stream()
    stream.close()
    pyaudio_instance.terminate()
    print('stream stopped')
    print('average frame rate = {:.0f} FPS'.format(frame_rate))
    quit()


def animate(i):
    # binary data
    data = stream.read(settings.CHUNK)
    # Open in numpy as a buffer
    data_np = np.frombuffer(data, dtype='h')

    # Update the line graph
    line.set_ydata(data_np)

    # compute FFT and update line
    yf = fft(data_np)
    # The fft will return complex numbers, so np.abs will return their magnitude

    line_fft.set_ydata(np.abs(yf[0:settings.CHUNK]) / (512 * settings.CHUNK))

    # Update the number of frames
    count[0] += 1


if __name__ == '__main__':
    start_time = time.time()

    anim = animation.FuncAnimation(fig, animate, blit=False, interval=1)
    fig.canvas.mpl_connect('close_event', on_close)
    plt.show()
