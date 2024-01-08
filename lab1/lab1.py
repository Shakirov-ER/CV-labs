import zipfile
import os
from PIL import Image
import io
import sys

# Функция для классификации изображений светофоров
def classify_traffic_lights(images):
    green, red, yellow, unclassified = [], [], [], []

    for image_name, image_data in images.items():
        try:
            image = Image.open(io.BytesIO(image_data))
            image = image.convert("RGB")

            colors = image.getcolors(maxcolors=1000000)

            red_color = sum(1 for count, color in colors if color[0] > 150 and color[1] < 100 and color[2] < 100)
            green_color = sum(1 for count, color in colors if color[0] < 100 and color[1] > 150 and color[2] < 100)
            yellow_color = sum(1 for count, color in colors if color[0] > 150 and color[1] > 150 and color[2] < 100)

            if green_color > red_color and green_color > yellow_color:
                green.append(image_name)
            elif red_color > green_color and red_color > yellow_color:
                red.append(image_name)
            elif yellow_color > green_color and yellow_color > red_color:
                yellow.append(image_name)
            else:
                unclassified.append(image_name)
        except Exception as e:
            unclassified.append(image_name)

    return green, red, yellow, unclassified

# Сохранение списка в файл
def save_list_to_file(file_list, file_name):
    with open(file_name, 'w') as file:
        for item in file_list:
            file.write("%s\n" % item)

# Основная функция программы
def main():
    if len(sys.argv) != 3:
        print("Использование: python lab1.py [path_to_zip] [output_directory]")
        sys.exit(1)

    zip_file_path = sys.argv[1]
    output_directory = sys.argv[2]

    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    images = {}
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        for file in zip_ref.namelist():
            if file.endswith('.jpg'):
                images[file] = zip_ref.read(file)

    green, red, yellow, unclassified = classify_traffic_lights(images)

    save_list_to_file(green, os.path.join(output_directory, 'green_lights.txt'))
    save_list_to_file(red, os.path.join(output_directory, 'red_lights.txt'))
    save_list_to_file(yellow, os.path.join(output_directory, 'yellow_lights.txt'))
    save_list_to_file(unclassified, os.path.join(output_directory, 'unclassified_lights.txt'))

    print("Классификация завершена. Результаты сохранены в", output_directory)

if __name__ == "__main__":
    main()