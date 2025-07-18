from PIL import Image

image_path = "./input.png"

img = Image.open(image_path).convert("RGB")
width, height = img.size

rgb_matrix = [[img.getpixel((x, y)) for x in range(width)] for y in range(height)]

color_to_value = {
    (255, 0, 0): 1, # UP GROUND
    (255, 0, 255): 2, # DOWN GROUND
    (255, 255, 255): 0, # AIR
    (255, 255, 0): 3, # WIN FLAG
    (200, 200, 0): 4, # UP SIDE OF THE WIN FLAG (changed color to avoid duplicate key)
}

result = [
    [color_to_value.get(pixel, -1) for pixel in row]
    for row in rgb_matrix
]

print("[")
for row in result:
    print(row, end=',')
    print()
print("]")