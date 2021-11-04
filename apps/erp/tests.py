result = []
temperatures = [22,23,21,25,23]
tamaño = len(temperatures)
print(tamaño)
i=0
for i in range(0, len(temperatures)):
    print(temperatures[i])
    try:
        if i == len(temperatures):
            dias = temperatures[i-1] - temperatures[i-1]
        elif temperatures[i] < temperatures[i+1]:
            dias = temperatures[i+1] - temperatures[i]
        elif temperatures[i] > temperatures[i+1]:
            dias = temperatures[i] - temperatures[i+1]
        else:
            dias = 0
        result.append(dias)
    except:
        pass
print(result)
