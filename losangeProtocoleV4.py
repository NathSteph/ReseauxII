from PIL import Image, ImageDraw
import numpy as np

# Facteur d'agrandissement de l'image
scale = 50
# ------------------------------------ FONCTIONS -----------------------------------------
def encode_string_to_pixels(string):
    # Define the color mapping
    colors = {'00': (255, 255, 255), '01': (0, 0, 0), '10': (0, 255, 0), '11': (255, 0, 0)}
    # Initialize the list of pixels
    pixels = []
    # Convert the string to binary representation
    binary_string = ''.join(format(ord(char), '08b') for char in string)
    # Iterate over the binary string two bits at a time and map them to colors
    for i in range(0, len(binary_string), 2):
        bits = binary_string[i:i+2]
        pixels.append(colors[bits])
    return pixels

def show_pixels(colors):
    # Create an image from the pixel list
    size = (len(colors), 1)
    img = Image.new('RGB', size)
    img.putdata(colors)
    img = img.resize((img.size[0]*scale, img.size[1]*scale), Image.NEAREST)
    # Enregistrer l'image dans un fichier
    img.save("image.png")
    # Show the image
    img.show()


def show_diamond_matrix(colors, x, y):
    image_width = x * scale + scale // 2
    image_height = y * scale + scale // 2
    image = Image.new('RGB', (image_width, image_height), (100, 100, 100))
    draw = ImageDraw.Draw(image)
    
    for i, color in enumerate(colors):
        row = i // x
        col = i % x
        
        offset_x = col * scale + (row % 2) * scale // 2
        offset_y = row * scale // 2
        
        diamond_points = [
            (offset_x + scale // 2, offset_y),
            (offset_x + scale, offset_y + scale // 2),
            (offset_x + scale // 2, offset_y + scale),
            (offset_x, offset_y + scale // 2)
        ]
        draw.polygon(diamond_points, fill=color)
        
    image.save("diamond_matrix.png")
    image.show()



def print_2D_matrix(matrix):
    for row in matrix:
        print(row)
        
def show_image_from_matrix(matrix, scale=1):
    height = len(matrix)
    width = len(matrix[0])

    img = Image.new('RGB', (width, height))

    for row in range(height):
        for col in range(width):
            img.putpixel((col, row), matrix[row][col])

    img = img.resize((img.size[0] * scale, img.size[1] * scale), Image.NEAREST)
    img.show()

def init_middle_lines(matrix):
    if len(matrix) % 2 == 0 or len(matrix[0]) % 2 == 0:
        raise ValueError("Matrix must be square and have an odd size.")
    
    size = len(matrix)
    mid = size // 2

    yellow = (255, 255, 0)

    for i in range(size):
        matrix[mid][i] = yellow
        matrix[i][mid] = yellow

    return matrix


def list_to_2D_matrix(matrix, colors, width, height):
    color_index = 0

    for i in range(width * height):
        row = i // width
        col = i % width

        if matrix[row][col] != (255, 255, 0):
            matrix[row][col] = colors[color_index]
            color_index += 1
            if color_index >= len(colors):
                break

    return matrix

def _2D_matrix_to_list(matrix, width, height):
    colors = []

    for i in range(width * height):
        row = i // width
        col = i % width
        colors.append(matrix[row][col])

    return colors


#------------------------------------------ Main -----------------------------------
phrase = "lundi"
x = 9
y = 9

colors = encode_string_to_pixels(phrase)
print("RGB code color = ", colors)  
print("\n\n\n")

show_pixels(colors)

# --------------------- AFFICHAGE SOUS FORME DE MATRICE DE PIXELS (show à parir d'une liste) -------------------
# Déclaration de notre image.
image = Image.new('RGB', [x, y], (100, 100, 100))

# Ajout des données à l'image
image.putdata(colors)
image = image.resize((image.size[0]*scale, image.size[1]*scale), Image.NEAREST)

# Enregistrer l'image dans un fichier
image.save("image.png")

# Afficher l'image à l'écran
image.show()


#show_diamond_matrix(colors, x, y)

# -------------------------------------------- show à parir d'une matric 2D -------------------------------------------
# Create an empty 7x7 matrix
matrix = [[(0, 0, 0) for _ in range(x)] for _ in range(x)]

# Initialize middle column and middle row with yellow
init_middle_lines(matrix)


colors = encode_string_to_pixels(phrase)
colors_2D = list_to_2D_matrix(matrix, colors, x, y)
print_2D_matrix(colors_2D)
print("print 2D matrix = \n", colors_2D)


show_image_from_matrix(colors_2D, scale=50)

# --------------------------------------------------------------------------------------------------------------------
show_diamond_matrix(_2D_matrix_to_list(colors_2D, x, y), x, y)


"""
from PIL import Image
import numpy as np
import math

# charger l'image carrée
img = Image.open('image.png')

# récupérer les dimensions de l'image
width, height = img.size

# calculer les coordonnées des coins du losange
x1, y1 = 0, height/2
x2, y2 = width/2, 0
x3, y3 = width, height/2
x4, y4 = width/2, height

# calculer la longueur du côté du losange
side = math.sqrt((width/2)**2 + (height/2)**2)

# calculer l'angle de rotation
angle = -45

# créer la transformation affine
matrix = (math.cos(math.radians(angle)), math.sin(math.radians(angle)), 0, 
          -math.sin(math.radians(angle)), math.cos(math.radians(angle)), 0)

# appliquer la transformation affine
img = img.transform((int(side), int(side)), Image.AFFINE, matrix, resample=Image.BICUBIC)

# afficher l'image
img.show()

"""














