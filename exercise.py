list = [7, 7]
repeticion = {}
respuesta = True
for n in list:
    if n in repeticion:
        repeticion[n] += 1
        if repeticion[n] == 3:                                                                                                                                            
            respuesta = False
    else:
        repeticion[n] = 1
print(repeticion)
print(respuesta)
