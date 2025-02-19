# -*- coding: utf-8 -*-
"""
Created on Fri May  5 14:56:09 2023

@author: Nathanael
"""

from PIL import Image, ImageDraw
import numpy as np
import hamming as ham
##import libhamming as hamming
 

"""
Data encoding: x
    we need to define how the message data will be encoded into the matrix cells. 
    This can be done using various encoding schemes, such as binary, decimal, hexadecimal, or ASCII.

Error detection and correction: x 
    we need to add some redundancy to the data to detect and correct errors that may occur during transmission. 
    One common method for error correction is Reed-Solomon codes.

Positioning and timing patterns:x
    we need to include some special patterns in the matrix to help with aligning and decoding the data. 
    The most common patterns are the positioning patterns and the timing patterns.

Color encoding: x 
    we can also use different colors to encode the data to increase the amount of information 
    that can be transmitted in the matrix.

Size and orientation: x
    we need to define the size and orientation of the matrix to ensure 
    that it can be printed and read correctly.
"""
 # Facteur d'agrandissement de l'image
scale = 25

def encode_string_to_pixels(string):
    # Define the color mapping
    colors = {'00': (255, 255, 255), '01': (0, 0, 0), '10': (0, 255, 0), '11': (255, 0, 0)}
    # Initialize the list of pixels
    pixels = []
    # Convert the string to binary representation
    binary_string = ''
    for c in string:
        binary_string += ham.encoding_hamming(bin(ord(c))[2:].zfill(8))
    #hamming sur 12bits pour chaque lettre
    
    # Iterate over the binary string two bits at a time and map them to colors
    for i in range(0, len(binary_string), 2):
        bits = binary_string[i:i+2]
        pixels.append(colors[bits])
        
    return pixels
#------------------------------------------ Main -----------------------------------
phrase = "LUImmmmmmmm"

## choisir un caractere pour la fin non utlise dans le msg
## mettre dzn sle rapport unexemple de décodage

# Récupération de l'encodage de la phrase en pixels
colors = encode_string_to_pixels(phrase)

# Récupère la taille du message
taille = int(len(colors) ** 0.5) + 1
print(taille)


# Définition de la couleur du timing pattern
timing_color = (255, 255, 0)

#-----------------------------------------------------------#
#Revoir le timing pattern et le mettre à l'extérieur
# Ajout du timing pattern horizontal


for i in range(taille):
    colors[i] = timing_color
        

# Ajout du timing pattern vertical
for i in range(taille):
    colors[i*taille] = timing_color

#-----------------------------------------------------------#

# (taille)Pixels non utilisés
pix = taille**2 - len(colors)

# Ajout du noir aux pixels restants
for i in range(pix):
    colors.append((0, 0, 0))

# Déclaration de notre image.
image = Image.new('RGB', [taille, taille], (100, 100, 100))

# Ajout des données à l'image
image.putdata(colors)
image = image.resize((image.size[0]*scale, image.size[1]*scale), Image.NEAREST)

# Enregistrer l'image dans un fichier
image.save("image.png")

# Afficher l'image à l'écran
image.show()

# Inclinaison image
img = Image.open("image.png")

# Récupérer la taille de l'image
width, height = img.size

# Créer une nouvelle image vide avec la taille d'un losange
losange_size = (height, height)
losange_img = Image.new('RGBA', losange_size, (255, 255, 255, 0))

# Calculer les coordonnées de l'angle supérieur gauche du carré qui contiendra le losange
square_top_left = ((width - height) // 2, 0)

# Copier l'image carrée dans le losange
losange_img.paste(img, square_top_left)

# Faire pivoter l'image de 45 degrés pour obtenir un losange
rotated_img = losange_img.rotate(45, expand=True)

# Enregistrer l'image
rotated_img.save("losange.png")

# Afficher l'image
rotated_img.show()



