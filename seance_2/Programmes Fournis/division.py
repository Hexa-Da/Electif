

def division(dividende, diviseur): 
	quotien = 0
	while(dividende > diviseur):
		dividende -= diviseur
		quotien += 1
	return (quotien, dividende)
