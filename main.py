import numpy as np
import matplotlib.pyplot as plt 



def compute_psd(signal,fs):
    length=len(signal)
    fft_values=np.fft.fft(signal)
    fft_freq=np.fft.fftfreq(length,1/fs)
    fft_values=np.fft.fftshift(fft_values)
    fft_freq=np.fft.fftshift(fft_freq)
    psd=np.abs(fft_values)**2
    normalised_psd=psd/np.max(psd)
    return fft_freq,normalised_psd


def plot(fft_freq,normalised_psd):
    plt.plot(fft_freq,normalised_psd)
    plt.show()
    return



