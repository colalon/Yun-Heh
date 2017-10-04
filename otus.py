import numpy as np

def otus(histograme):
    histo = np.reshape(histograme,256)
    total = histo.sum()
    sumB=0
    wB=0
    maximum = 0.0

    sum1 = np.dot(np.arange(256),histo)
    
    for i in range (0,256):
        wB = wB + histo[i]
        wF = total - wB
        if (wB == 0 or wF == 0):
            continue
        sumB = sumB + i * histo[i]
        mF = (sum1 - sumB) / wF
        between = wB * wF * ((sumB / wB) - mF) * ((sumB / wB) - mF)
        if ( between >= maximum ):
            level = i
            maximum = between
    return level
