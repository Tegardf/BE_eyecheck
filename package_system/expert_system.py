import numpy as np
#               G01  G02  G03  G04  G05  G06  G07  G08  G09  G10  G11  G12  G13  G14  G15  G16  G17  
K01 = np.array([0.8, 0.2, 0.0, 0.8, 0.0, 0.0, 0.8, 0.8, 0.0, 0.0, 0.0, 0.0, 0.0, 0.8, 0.0, 0.0, 1.0]) #mature
K02 = np.array([0.6, 1.0, 0.4, 0.0, 0.0, 0.4, 0.0, 1.0, 0.8, 0.6, 0.8, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0]) #Traumatik
K03 = np.array([0.4, 0.4, 0.8, 0.6, 0.6, 0.8, 0.0, 0.0, 0.6, 0.0, 0.0, 0.6, 0.8, 0.0, 0.0, 0.0, 1.0]) #komplikata
K04 = np.array([0.8, 0.6, 0.6, 0.2, 0.4, 0.0, 0.8, 0.0, 0.4, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0]) #senilis
K05 = np.array([0.0, 0.8, 0.0, 0.6, 0.0, 0.6, 0.0, 0.0, 0.8, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 1.0]) #Juvenile

def CF(gejalas = []):
    delIndex = []
    for i in range(0,17):
        if gejalas[i] == 0.0:
            delIndex.append(i)
    gejalas = np.delete(gejalas,delIndex)
    gejalas = np.sort(gejalas)
    symtopms_old = CFplus(gejalas[0],gejalas[1])
    for i in range(2,len(gejalas)-1):
        symtopms_old = CFplus(symtopms_old,gejalas[i])
    return symtopms_old

def CFplus(CFsymtomps1, CFsymtomps2):
    return CFsymtomps1 + (CFsymtomps2 * (1-CFsymtomps1))

def CFbeda(CFsymtomps1, CFsymtomps2):
    return (CFsymtomps1 + CFsymtomps2)/(1-min(CFsymtomps1,CFsymtomps2))
