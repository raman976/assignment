import numpy as np 



from signals.bpsk import bit_generator, modulate, upsample


def generate_subcarrier(subcarrier_freq,fs,signal_length):
    t=np.arange(signal_length)/fs

    subcarrier=np.sign(np.sin(2*np.pi*subcarrier_freq*t)) 
    return subcarrier 


def generate_boc(m,n,num_bits,fs,carrier_frequency=0.0):
    chip_rate=n*1.023e6 
    subcarrier_freq=m*1.023e6
    samples_per_chip=int(fs/chip_rate)

    if samples_per_chip<1:
        raise ValueError("sampling freq should be greater than chip rate")


    bits=bit_generator(num_bits)
    bpsk_signal=modulate(bits)
    upsampled_signal=upsample(bpsk_signal,samples_per_chip)
    subcarrier=generate_subcarrier(subcarrier_freq,fs,len(upsampled_signal))
    boc_signal=upsampled_signal*subcarrier
    return boc_signal