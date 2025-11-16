### Analyse spectrale (FFT)

- **But**: savoir quelles fréquences (les « notes ») composent un son.
- **Idée**: on passe du domaine temporel (amplitude vs temps) au domaine fréquentiel (amplitude vs fréquence). Les pics du spectre = fréquences présentes.

### Étapes simples
1) Tu as un `signal` avec `N` échantillons, pris à `freq_echantillonnage` (44100 Hz).
2) On calcule la FFT pour obtenir l'énergie par fréquence. L'énergie est une mesure de l'intensité de chaque fréquence dans le signal - plus l'énergie est élevée à une fréquence donnée, plus cette fréquence est présente/forte dans le signal. Mathématiquement, c'est le carré de l'amplitude de la FFT.
3) On construit l'axe des fréquences pour savoir à quelle fréquence correspond chaque valeur du tableau :
   - La fonction `fftfreq(N, 1/freq_echantillonnage)` crée un tableau de N fréquences
   - Les fréquences sont espacées de `freq_echantillonnage/N` Hz

4) On ne garde que les fréquences positives (0 → Nyquist = 22050 Hz) car :
   - La FFT produit des fréquences positives et négatives symétriques
   - Pour un signal réel, les fréquences négatives sont redondantes
   - La fréquence de Nyquist (22050 Hz) est la fréquence max qu'on peut représenter
     (= fréquence d'échantillonnage/2)
5) On prend la magnitude (module) pour tracer l'amplitude des pics :
   - La FFT retourne des nombres complexes (partie réelle + imaginaire)
   - Le module |z| = √(Re(z)² + Im(z)²) donne l'amplitude de chaque fréquence
   - On divise par N/2 pour normaliser (N = nombre d'échantillons)
   - Plus le pic est haut, plus la fréquence est présente dans le signal

### Recette prête à l’emploi
```python
from scipy.fft import fft, fftfreq
import numpy as np

N = len(signal)
F = fft(signal)                              # 1) FFT
freqs = fftfreq(N, 1/freq_echantillonnage)   # 2) Axe des fréquences
max_n = N // 2                               # 3) Positif seulement
freqs_pos = freqs[:max_n]
mag = (2.0 / N) * np.abs(F[:max_n])          # 4) Magnitude normalisée simple
```
