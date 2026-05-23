import numpy as np
from scipy.signal import welch


def compute_psd(signal,fs,center_frequency=0.0):
    signal=np.asarray(signal)
    if len(signal)==0:
        return np.array([]),np.array([])

    nperseg=min(1024,len(signal))
    freqs,psd=welch(
        signal,
        fs=fs,
        window="hann",
        nperseg=nperseg,
        scaling="density",
        return_onesided=False,
    )

    freqs=np.fft.fftshift(freqs)
    psd=np.fft.fftshift(psd)
    freqs=freqs+center_frequency

    area=np.trapezoid(psd,freqs)
    if area>0:
        psd=psd/area

    return freqs,psd


def apply_bandwidth(freqs,psd,center_frequency,bandwidth):
    if bandwidth is None or bandwidth<=0:
        return freqs,psd

    lower_frequency=center_frequency-bandwidth/2
    upper_frequency=center_frequency+bandwidth/2
    frequency_mask=(freqs>=lower_frequency)&(freqs<=upper_frequency)
    return freqs[frequency_mask],psd[frequency_mask]


def align_spectra(freqs1,psd1,freqs2,psd2):
    if len(freqs1)==0 or len(freqs2)==0:
        return freqs1,psd1,freqs2,psd2

    lower_frequency=max(freqs1[0],freqs2[0])
    upper_frequency=min(freqs1[-1],freqs2[-1])

    if upper_frequency<=lower_frequency:
        return np.array([]),np.array([]),np.array([]),np.array([])

    spacing1=np.median(np.diff(freqs1)) if len(freqs1)>1 else 0.0
    spacing2=np.median(np.diff(freqs2)) if len(freqs2)>1 else 0.0
    step=max(abs(spacing1),abs(spacing2))

    if step<=0:
        common_freqs=freqs1[(freqs1>=lower_frequency)&(freqs1<=upper_frequency)]
        common_mask2=(freqs2>=lower_frequency)&(freqs2<=upper_frequency)
        return common_freqs,psd1[(freqs1>=lower_frequency)&(freqs1<=upper_frequency)],freqs2[common_mask2],psd2[common_mask2]
    count=int(np.floor((upper_frequency-lower_frequency)/step))+1
    common_freqs=lower_frequency+np.arange(count)*step

    if len(common_freqs)==0:
        return np.array([]),np.array([]),np.array([]),np.array([])

    aligned_psd1=np.interp(common_freqs,freqs1,psd1)
    aligned_psd2=np.interp(common_freqs,freqs2,psd2)
    return common_freqs,aligned_psd1,common_freqs,aligned_psd2


