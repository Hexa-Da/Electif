from scipy.io.wavfile import read, write
from scipy.fft import fft, fftfreq
from scipy.signal import butter, freqz, lfilter
import numpy as np
import matplotlib.pyplot as plt
import pdb

# Fréquence d'échantillonnage : 44100Hz
freq_echantillonnage=44100
# Amplitude du signal : notre amplitude max est la valeur max d'un entier 16bits
amplitude_max = np.iinfo(np.int16).max

def analyser(signal):
    N = len(signal)

    # visualiser le fichier example.wav
    fig, (ax1, ax2) = plt.subplots(2, 1)
    ax1.plot(signal, 'r+')
    ax1.plot(signal)

    # On garde les fréquences positives
    max_n = N // 2
    freqs = fftfreq(N, 1/freq_echantillonnage)[:max_n]

    # Question 1 : que fait cette ligne.
    f = fft(signal)
    ax2.plot(freqs, 2.0/N * np.abs(f[0:N//2]))

    # On affiche le graphe : 
    plt.show()

def generer_signal(frequence, duree):
    t = np.linspace(0., float(duree)/1000, num = int(freq_echantillonnage/1000 * duree))
    signal = np.sin(2. * np.pi * frequence * t) * amplitude_max
    return signal

def concatener_signaux(liste_signaux):
    signal = np.concatenate(liste_signaux)
    return signal

def superposer_signaux(liste_signaux):
    nb_signaux = len(liste_signaux)
    signal = np.sum(np.stack(liste_signaux)/nb_signaux, axis=0)
    return signal

def filtrer_passe_bas(signal, freq_cutoff, freq_sample):
    b, a = butter(1, freq_cutoff, fs=freq_sample, btype='lowpass', analog=False)
    return lfilter(b, a, signal)

def filtrer_passe_haut(signal, freq_cutoff, freq_sample):
    b, a = butter(1, freq_cutoff, fs=freq_sample, btype='highpass', analog=False)
    return lfilter(b, a, signal)

def sauvegarder(nom, signal):
    write(nom, freq_echantillonnage, signal.astype(np.int16))

def note(frequence, duree, nb_harmoniques):
    if frequence == 0:
        return generer_signal(0, duree)
    else:
        return filtrer_passe_bas(superposer_signaux([generer_signal(frequence * (i+1), duree) for i in range(nb_harmoniques)]), frequence, freq_echantillonnage)

def morceau_surprise(): 
    nb_harmoniques = 4
    duree_temps = 0.5
    signal_1 = superposer_signaux([
        concatener_signaux([
        note(660, duree_temps, nb_harmoniques),
        note(493, duree_temps/2, nb_harmoniques),
        note(523, duree_temps/2, nb_harmoniques),
        note(587, duree_temps, nb_harmoniques),
        note(523, duree_temps/2, nb_harmoniques),
        note(493, duree_temps/2, nb_harmoniques),
        note(440, duree_temps, nb_harmoniques),
        note(440, duree_temps/2, nb_harmoniques),
        note(523, duree_temps/2, nb_harmoniques),
        note(660, duree_temps, nb_harmoniques),
        note(587, duree_temps/2, nb_harmoniques),
        note(523, duree_temps/2, nb_harmoniques),
        note(493, duree_temps, nb_harmoniques),
        note(493, duree_temps/2, nb_harmoniques),
        note(523, duree_temps/2, nb_harmoniques),
        note(587, duree_temps, nb_harmoniques),
        note(660, duree_temps, nb_harmoniques),
        note(523, duree_temps, nb_harmoniques),
        note(440, duree_temps, nb_harmoniques),
        note(440, duree_temps*2, nb_harmoniques),
        ]),
        concatener_signaux([
            superposer_signaux([
                note(164, duree_temps*4, nb_harmoniques),
                note(246, duree_temps*4, nb_harmoniques),
            ]),
            superposer_signaux([
                note(220, duree_temps*4, nb_harmoniques),
                note(329, duree_temps*4, nb_harmoniques),
            ]),
            superposer_signaux([
                note(207, duree_temps*4, nb_harmoniques),
                note(329, duree_temps*4, nb_harmoniques),
            ]),
            superposer_signaux([
                note(220, duree_temps*4, nb_harmoniques),
                note(329, duree_temps*4, nb_harmoniques),
            ]),
            ])
        ])

    signal_2 = superposer_signaux([
        concatener_signaux([
            note(0, duree_temps/2, nb_harmoniques),
            note(587, duree_temps, nb_harmoniques),
            note(698, duree_temps/2, nb_harmoniques),
            note(880, duree_temps, nb_harmoniques),
            note(783, duree_temps/2, nb_harmoniques),
            note(698, duree_temps/2, nb_harmoniques),
            note(659, duree_temps*1.5, nb_harmoniques),
            note(523, duree_temps/2, nb_harmoniques),
            note(659, duree_temps, nb_harmoniques),
            note(587, duree_temps/2, nb_harmoniques),
            note(523, duree_temps/2, nb_harmoniques),
            note(493, duree_temps, nb_harmoniques),
            note(493, duree_temps/2, nb_harmoniques),
            note(523, duree_temps/2, nb_harmoniques),
            note(587, duree_temps, nb_harmoniques),
            note(659, duree_temps, nb_harmoniques),
            note(523, duree_temps, nb_harmoniques),
            note(440, duree_temps, nb_harmoniques),
            note(440, duree_temps*2, nb_harmoniques),
            ]),
        concatener_signaux([
            superposer_signaux([
                note(146, duree_temps*4, nb_harmoniques),
                note(220, duree_temps*4, nb_harmoniques),
            ]),
            superposer_signaux([
                note(220, duree_temps*4, nb_harmoniques),
                note(329, duree_temps*4, nb_harmoniques),
            ]),
            superposer_signaux([
                note(207, duree_temps*4, nb_harmoniques),
                note(329, duree_temps*4, nb_harmoniques),
            ]),
            superposer_signaux([
                note(220, duree_temps*4, nb_harmoniques),
                note(329, duree_temps*4, nb_harmoniques),
            ]),
            ])
        ])

    signal = concatener_signaux([signal_1, signal_2])
    return signal

# À décommenter à la question 5.
# signal = morceau_surprise()
# sauvegarder("sortie.wav", signal)
# analyser(signal)
