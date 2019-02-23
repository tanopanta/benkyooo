#LF/HFの計算

import math
import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as sg
from scipy.interpolate import interp1d
from scipy import integrate
 
 
fs = 250 #脈波のサンプリング周波数
hokan_fs = 8 #補間後の再サンプリング周波数
fftsize = 2 ** 14

data = np.loadtxt("PPG_250Hz_120s_male22_stress.csv")
#data = np.loadtxt("PPG_250Hz_120s_male22_relax.csv")

#前処理-------------------------------
# DC成分カット
data = sg.detrend(data) 
# ローパスフィルタ
lpf_fil = sg.firwin(33, 2.0 / (fs/2.0), window="hamming")
data = sg.lfilter(lpf_fil, 1, data)

#ピーク検出-------------------------
peak_indexes, _ = sg.find_peaks(data, height=0, distance=fs//2.2)
 
plt.subplot(311)
plt.title("Raw Wave and Peaks")
plt.plot(data)
plt.plot(peak_indexes, data[peak_indexes], "x")

#差分計算-----------------------------------------
peak_diffs = np.diff(peak_indexes) / fs #ピーク間の距離
peak_seconds = peak_indexes / fs #ピーク検出時間

#ピークの差分から波形を再サンプリング---------------
#外挿ありの3次スプライン補間
f = interp1d(peak_seconds[:-1], peak_diffs, kind="cubic", fill_value='extrapolate')
sample_len = len(data) / fs
xnew = np.linspace(0 , sample_len, sample_len * hokan_fs)

hokan = f(xnew) # y = f(x)


hokan = hokan[hokan_fs//2:-hokan_fs] #前後1秒分ぐらいをカット
xnew = xnew[hokan_fs//2:-hokan_fs]
 
plt.subplot(312)
plt.title("RRI")
plt.plot(xnew, hokan)
plt.plot(peak_seconds[:-1], peak_diffs, "x")


#fftによるパワースペクトル導出-------------------------------
hokan = sg.detrend(hokan) #基線除去

# welch法によりパワースペクトルを求める
freq, power = sg.welch(hokan, hokan_fs, nperseg=len(hokan)/2, nfft=fftsize)

# ピリオドグラム法によりパワースペクトルを求める(窓関数－＞fft)
#freq, power =sg.periodogram(hokan, hokan_fs, nfft=fftsize)

plt.subplot(337)
plt.xlim(0.04, 0.4)
plt.title("Power Spectrum")
plt.plot(freq, power)


 
#LF/HF計算------------
def hz_to_idx(hz, fs, point):
    return math.ceil(hz / (fs / (point)))

lf_min = hz_to_idx(0.04, hokan_fs, fftsize)
lf_max = hz_to_idx(0.15, hokan_fs, fftsize)
hf_min = lf_max
hf_max = hz_to_idx(0.4, hokan_fs, fftsize)


lf = integrate.trapz(power[lf_min:lf_max+1]) #台形公式による積分
hf = integrate.trapz(power[hf_min:hf_max+1]) 

plt.subplot(338)
plt.pie([lf, hf], colors=["orange", "green"],counterclock=False,startangle=90, labels=["LF", "HF"],autopct="%1.1f%%")
plt.title("LF/HF: {}".format(lf/ hf))

print("平均心拍数", np.mean(60 / peak_diffs), "bps")

plt.show()