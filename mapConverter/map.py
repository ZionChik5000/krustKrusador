from PIL import Image

# Заменяем путь на свой
image_path = "input.png"

# Открываем изображение и конвертируем в RGB
img = Image.open(image_path).convert("RGB")
width, height = img.size

# Получаем двумерный список с RGB значениями
rgb_matrix = [[img.getpixel((x, y)) for x in range(width)] for y in range(height)]

# Преобразуем в матрицу с цифрами по цвету
color_to_value = {
    (255, 0, 0): 1,       # Красный
    (255, 255, 255): 0,   # Белый
    (255, 255, 0): 2      # Жёлтый
}

# Итоговая матрица
result = [
    [color_to_value.get(pixel, -1) for pixel in row]
    for row in rgb_matrix
]

# Печатаем результат
for row in result:
    print(row)
