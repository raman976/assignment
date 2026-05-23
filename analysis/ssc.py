import numpy as np


def compute_ssc(psd1, psd2, freqs, center_frequency=0.0, receiver_bandwidth=None):
    if freqs is None or len(freqs) == 0:
        return 0.0


    freqs = np.asarray(freqs)
    psd1 = np.asarray(psd1)
    psd2 = np.asarray(psd2)


    if receiver_bandwidth is not None and receiver_bandwidth > 0:
        lower_frequency = center_frequency - receiver_bandwidth / 2
        upper_frequency = center_frequency + receiver_bandwidth / 2
        mask = (freqs >= lower_frequency) & (freqs <= upper_frequency)
        freqs = freqs[mask]
        psd1 = psd1[mask]
        psd2 = psd2[mask]

    if len(freqs) < 2:
        return 0.0


    if freqs[0] > freqs[-1]:
        freqs = freqs[::-1]
        psd1 = psd1[::-1]
        psd2 = psd2[::-1]

    integral = np.trapezoid(psd1 * psd2, freqs)
    return float(integral)

