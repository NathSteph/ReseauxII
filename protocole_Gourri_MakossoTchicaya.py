# -*- coding: utf-8 -*-
"""
Created on Fri Apr 28 14:50:38 2023

@author: Nathanaël MAKOSSO TCHICAYA / Amal GOURRI
"""
# Bibliothèques utilisées
from PIL import Image
import hamming as ham

# Facteur d'agrandissement de l'image
scale = 25

""" Fonction permettant d'encoder un message/mot donné
    sous forme de pixels. """
def encode_string_to_pixels(string):
    # Couleurs de pixels
    colors = {'00': (255, 255, 255), '01': (0, 0, 0), '10': (0, 255, 0), '11': (255, 0, 0)}
    # Initialisation de la liste de pixels
    pixels = []
    # Conversion en representation binaire
    binary_string = ''
    for c in string:    #hamming sur 12bits pour chaque lettre
        binary_string += ham.encoding_hamming(bin(ord(c))[2:].zfill(8))
    # Conversion de bits en code couleurs
    for i in range(0, len(binary_string), 2):
        bits = binary_string[i:i+2]
        pixels.append(colors[bits])
        
    return pixels

""" Fonctions qui permettent d'alterner 
    les couleurs jaune, noir pour le timing pattern."""
def alternance():
    if not hasattr(alternance, 'counter'):
        alternance.counter = 0
    result = (255, 255, 0) if alternance.counter % 2 == 0 else (0, 0, 0)
    alternance.counter += 1
    
    return result

def alternance2():
    if not hasattr(alternance, 'counter'):
        alternance.counter = 0
    result = (0, 0, 0) if alternance.counter % 2 == 0 else (255, 255, 0)
    alternance.counter += 1
    
    return result
    
#------------------------------------------ Main -----------------------------------
# Mot/message à encoder
phrase = "µ"


# Définition des couleurs
timing_color = (255, 255, 0)
timing_color2 = (0, 0, 0)

# Récupération de l'encodage de la phrase en pixels
colors = encode_string_to_pixels(phrase)


# Récupère la taille du message
taille = int(len(colors) ** 0.5) + 1

# Calcule le nbre de pixels qui manque pour compléter une matrice carrée
for i in range(len(colors), taille*taille):
    colors.append((0, 0, 0))
    
indices = []

for i in range(len(colors)):
    if i % taille == 0:
        indices.append(i)
        
for i in range(len(indices)):
    indices[i] = indices[i]+i
#

# Génère l'alternance de couleurs pour le timing pattern
for i in indices:
    colors.insert(i, alternance())

for i in range(taille+1):
    colors = ([alternance2()]) + colors

# Incrémentation de la taille
taille = taille+1

# Déclaration de notre image.
image = Image.new('RGB', [taille, taille], (100, 100, 100))

# Ajout des données à l'image
image.putdata(colors)
image = image.resize((image.size[0]*scale, image.size[1]*scale), Image.NEAREST)

# Enregistrer l'image dans un fichier
image.save("image.png")

# Afficher l'image (sous forme carrée) à l'écran
#image.show()

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