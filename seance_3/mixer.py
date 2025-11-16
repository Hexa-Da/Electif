from scipy.io.wavfile import read, write
from scipy.fft import fft, fftfreq
from scipy.signal import butter, freqz, lfilter
import numpy as np
import matplotlib.pyplot as plt
import pdb

# Fréquence d'échantillonnage : 44100Hz
freq_echantillonnage = 44100
# Amplitude du signal : notre amplitude max est la valeur max d'un entier 16bits
amplitude_max = np.iinfo(np.int16).max

"""analyse un signal"""
def analyser(signal):
    N = len(signal)

    #crée un graphe avec deux axes
    fig, (ax1, ax2) = plt.subplots(2, 1) 
    # Afficher une petite fenêtre temporelle (lisible)
    win = min(N, 16*44100) #5000 échantillons = 0.113s
    ax1.plot(np.arange(win) / freq_echantillonnage, np.asarray(signal[:win], dtype=float), linewidth=1.0)
    ax1.set_xlabel("Temps (s)")
    ax1.set_ylabel("Amplitude")
    ax1.set_title("Signal (fenêtre courte)")
    ax1.grid(True, alpha=0.3)

    # On garde les fréquences positives
    max_n = N // 2
    freqs = fftfreq(N, 1/freq_echantillonnage)[:max_n]

    f = fft(signal) #transformée de Fourier
    mag = (2.0/N) * np.abs(f[:max_n])
    ax2.plot(freqs, mag)
    ax2.set_xlim(0, min(4000, freq_echantillonnage/2))  # focus sur le bas du spectre
    ax2.set_xlabel("Fréquence (Hz)")
    ax2.set_ylabel("Amplitude")
    ax2.set_title("Spectre")
    ax2.grid(True, alpha=0.3)

    # On affiche le graphe : 
    plt.tight_layout()
    plt.show()

"""crée un fichier wav à partir d'un signal"""
def sauvegarder(nom, signal):
    write(nom, freq_echantillonnage, signal)

"""crée un signal sinusoïdal à partir d'une fréquence et d'une durée"""
def generer_signal(frequence, duree):
    n = int(duree * freq_echantillonnage) #nombre d'échantillons
    t = np.arange(n) / freq_echantillonnage #temps
    s = np.sin(2 * np.pi * frequence * t) #signal sinusoïdal
    #arrondit le signal à l'amplitude max et le convertit en entiers 16 bits
    return np.round(amplitude_max * s).astype(np.int16)

"""concatène une liste de signaux"""
def concatener_signaux(liste_signaux):
    if not liste_signaux:
        #si la liste est vide, retourne un tableau vide
        return np.array([], dtype=np.int16) 
    return np.concatenate(liste_signaux) 

"""superpose une liste de signaux"""
def superposer_signaux(liste_signaux):
    if not liste_signaux:
        return np.array([], dtype=np.int16)
    max_len = max(len(s) for s in liste_signaux)
    acc = np.zeros(max_len, dtype=np.int64) #tableau de zéros
    for s in liste_signaux:
        #convertit le signal en tableau d'entiers 64 bits
        a = np.asarray(s, dtype=np.int64) #convertit le signal en tableau d'entiers 64 bits
        if len(a) < max_len: #si le signal est plus court que le plus long, ajoute des zéros
            tmp = np.zeros(max_len, dtype=np.int64)
            tmp[:len(a)] = a
            a = tmp
        acc += a
    # nomalisation douce pour éviter la saturation
    peak = np.max(np.abs(acc)) if acc.size else 1.0
    if peak > amplitude_max:
        acc = acc * (amplitude_max / peak)
    #coupe le signal aux bornes de l'amplitude max
    return np.clip(acc, -amplitude_max, amplitude_max - 1).astype(np.int16) 

"""crée une note à partir d'une fréquence, d'une durée et d'un nombre d'harmoniques"""
def note(frequence, duree, nb_harmoniques):
    if frequence <= 0:
        n = int(duree * freq_echantillonnage)
        return np.zeros(n, dtype=np.int16)
    signaux = [generer_signal(frequence, duree)]  # fondamentale
    for k in range(1, nb_harmoniques + 1):
        # harmoniques pondérées par 1/(k+1) pour éviter la saturation
        harm = generer_signal((k + 1) * frequence, duree).astype(np.float64)
        signaux.append(harm / (k + 1))
    mix = superposer_signaux(signaux)
    # atténue les harmoniques au-dessus de la fondamentale via passe-bas du 1er ordre
    cutoff = min(int(frequence * 1.5), (freq_echantillonnage // 2) - 1)
    return filtrer_passe_bas(mix, cutoff, freq_echantillonnage)

"""filtre un signal passe bas"""
def filtrer_passe_bas(signal, freq_cutoff, freq_sample):   
    w = freq_cutoff / (freq_sample / 2)  # fréquence normalisée (Nyquist)
    b, a = butter(1, w, btype='low', analog=False) #crée le filtre passe bas
    y = lfilter(b, a, np.asarray(signal, dtype=np.float64)) #applique le filtre
    #coupe le signal aux bornes de l'amplitude max
    return np.clip(np.round(y), -amplitude_max, amplitude_max - 1).astype(np.int16)

"""filtre un signal passe haut"""
def filtrer_passe_haut(signal, freq_cutoff, freq_sample):
    w = freq_cutoff / (freq_sample / 2)  # fréquence normalisée (Nyquist)
    b, a = butter(1, w, btype='high', analog=False) #crée le filtre passe haut
    y = lfilter(b, a, np.asarray(signal, dtype=np.float64)) #applique le filtre
    #coupe le signal aux bornes de l'amplitude max
    return np.clip(np.round(y), -amplitude_max, amplitude_max - 1).astype(np.int16)

"""crée un morceau surprise"""
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

if __name__ == "__main__":
    signal = morceau_surprise()
    analyser(signal)
    sauvegarder("sortie.wav", signal)



