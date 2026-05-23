import numpy as np

from signals.boc import generate_boc




def normalize_power(signal):
    power=np.sqrt(np.mean(signal**2))
    normalized_signal=signal/power
    return normalized_signal

def generate_mboc(components,num_bits,fs,carrier_frequency=0.0):
    mboc_signal=None
    for component in components:
        m=component['m']
        n=component['n']
        weight=component['weight']
        boc_signal=generate_boc(m,n,num_bits,fs)
        boc_signal=normalize_power(boc_signal)
        weighted_boc_signal=weight*boc_signal
        if mboc_signal is None:
            mboc_signal=weighted_boc_signal
        else:
            mboc_signal+=weighted_boc_signal
    mboc_signal=normalize_power(mboc_signal)
    return mboc_signal

# fs = 100e6
# num_bits = 1000
# components = [
#     {
#         "m":1,
#         "n":1,
#         "weight":1/11
#     },
#     {
#         "m":6,
#         "n":1,
#         "weight":10/11
#     }
# ]

# signal = generate_mboc(
#     components=components,
#     num_bits=num_bits,
#     fs=fs,
#     carrier_frequency=1575.42e6
# )

