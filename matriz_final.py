import numpy as np
import os

i=0
lista = []

def matriz_features():
    for base, dis, files in os.walk('dataset/features'):
        a = base
        if (i>1):
            lista.extend(np.loadtxt(a + '/features.txt', delimiter=' ',dtype='str'))
        if (i == 21):
            print("llegaste aquí", i)
            i=0
        i=i+1

    mat = np.array(lista)
    variable1=mat[0:20000]
    variable2=mat[20000:40000]
    variable3=mat[40000:60000]
    mat0= np.insert(variable1, 26, values=0, axis=1)
    mat1= np.insert(variable2, 26, values=1, axis=1)
    mat2= np.insert(variable3, 26, values=2, axis=1)
    matriz_final = np.concatenate((mat0,mat1,mat2), axis=0)
    return(matriz_final)


   