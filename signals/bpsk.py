import numpy as np

def bit_generator(num_bits):
    return np.random.randint(0,2,num_bits)


def modulate(bits):
    bits=2*bits-1 
    return bits

def upsample(bits, sample_per_bit):
    k=np.repeat(bits,sample_per_bit)
    return k 




def generate_bpsk_signal(num_bits,chip_rate,fs,carrier_frequency=0.0):
    bits=bit_generator(num_bits)
    bpsk_signal=modulate(bits)
    sample_per_bit=int(fs/chip_rate)

    if sample_per_bit<1:
        raise ValueError("sampling freq should be greater than chip rate")

    upsampled_signal=upsample(bpsk_signal,sample_per_bit)
    return upsampled_signal