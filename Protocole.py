# -*- coding: utf-8 -*-
"""
Created on Fri Apr  7 09:10:29 2023

@author: Nathanaël
"""
import PIL
from PIL import Image
import numpy as np

#########################################

# Code de hamming
def encode_hamming(bits):
    G = np.array([[1,0,0,0,1,1,0],
                  [0,1,0,0,1,0,1],
                  [0,0,1,0,1,1,1],
                  [0,0,0,1,0,1,1]])
    p = np.mod(np.dot(bits,G),2)
    return np.concatenate((bits,p))

print(encode_hamming("01"))

def message_to_bits(message):
    bits = ""
    for c in message:
        bits += bin(ord(c))[2:].zfill(8)
    return bits

##print(message_to_bits('lundi'))

"""def bits_to_colors(bits):
    colors = ""
    for i in range(0, len(bits), 2):
        if bits[i:i+2] == "00":
            colors += "blanc "
        elif bits[i:i+2] == "01":
            colors += "noir "
        elif bits[i:i+2] == "11":
            colors += "rouge "
        elif bits[i:i+2] == "10":
            colors += "vert "
    return colors
"""
#colors = []
"""def bits_to_rgb(bits):

    for i in range(0, len(bits), 2):
        if bits[i:i+2] == "00":
            colors.append((255, 255, 255))  # Blanc
        elif bits[i:i+2] == "01":
            colors.append((0, 0, 0))        # Noir
        elif bits[i:i+2] == "11":
            colors.append((255, 0, 0))      # Rouge
        elif bits[i:i+2] == "10":
            colors.append((0, 255, 0))      # Vert
    return colors
"""

def bits_to_colors(bits):
    colors = []
    for i in range(0, len(bits), 2):
        if bits[i:i+2] == "00":
            colors.append( "FFFFFF") # blanc
        elif bits[i:i+2] == "01":
            colors.append("000000") # noir
        elif bits[i:i+2] == "11":
            colors.append("FF0000") # rouge
        elif bits[i:i+2] == "10":
            colors.append("00FF00") # vert
    return colors

colors1 = bits_to_colors(message_to_bits('lundi'))
print(colors1)
#print(bits_to_colors(message_to_bits('lundi')))
#print(colors1)
###########################

# Facteur d'agrandissement de l'image
scale = 50

# Taille de la matrice
x = 8
y = 8

taille = len(colors1)

# Initialisation de la matrice avec la couleur blanche (0xFFFFFF)
code = [[0x606060 for j in range(y)] for i in range(x)]

n = 0

"""for m in range(0, 8):
    for i in range(0, taille):
        code[n][m] = int(colors1[i], 16)
"""
i = 0
# Liste des cases à remplir avec les couleurs de colors1
cases = [(0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), 
         (1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6),
         (2, 1), (2, 2), (2, 3), (2, 4), (2, 5), (2, 6),
         (3, 1), (3, 2)]

for n, m in cases:
    code[n][m] = int(colors1[i], 16)
    i = i+1
        
#code[0][2] = int(colors1[1], 16)
#code[0][3] = int(colors1[2], 16)
#code[0][4] = int(colors1[3], 16)

# ajout d'un pixel rouge sur le coin en haut à droite de l'image
#code[0][7] = 0xff0000
# ajout d'un pixel vert sur l'image
#code[6][6] = 0x00FF00

# Déclaration de notre image.
image = Image.new('RGB', [x, y], 255)

# Aplatissement de la matrice (PIL prend un tableau 1D en entrée)
code = [item for sublist in code for item in sublist]

# Conversion des valeurs de RGB vers BGR (PIL utilise le format BGR)
code = [((n & 0x0000FF) << 16) | n & 0x00FF00 | ((n & 0xFF0000) >> 16) for n in code]

# Ajout des données à l'image
image.putdata(code)
image = image.resize((image.size[0]*scale, image.size[1]*scale), Image.NEAREST)

# Enregistrer l'image dans un fichier
image.save("image.png")

# Afficher l'image à l'écran
image.show()

