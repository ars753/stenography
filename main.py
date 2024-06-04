from PIL import Image
import argparse

def hide_message(image_path, message, output_path):
    img = Image.open(image_path)

    #Вывод сообщения перед его скрытием
    print("Сообщение для скрытия:", message)

    #Преобразование текста сообщения в бинарный формат
    binary_message = ''.join(format(ord(char), '08b') for char in message)

    #Проверка, достаточно ли места в изображении для скрытия сообщения
    if len(binary_message) > img.width * img.height * 3:
        raise ValueError("Слишком длинное сообщение для данного изображения")

    data_index = 0

    #Проход по каждому пикселю изображения
    for y in range(img.height):
        for x in range(img.width):
            pixel = list(img.getpixel((x, y)))

            #Замена младших битов пикселя на биты сообщения
            for i in range(3):
                if data_index < len(binary_message):
                    pixel[i] = pixel[i] & ~1 | int(binary_message[data_index])
                    data_index += 1

            img.putpixel((x, y), tuple(pixel))

            #Если весь текст уже был скрыт, сохраняем изображение и завершаем
            if data_index >= len(binary_message):
                img.save(output_path)
                return

    raise ValueError("Изображение слишком маленькое для данного сообщения")

def reveal_message(image_path):
    img = Image.open(image_path)
    binary_message = ''

    #Проход по каждому пикселю изображения
    for y in range(img.height):
        for x in range(img.width):
            pixel = img.getpixel((x, y))

            #Извлечение младших битов каждой цветовой компоненты пикселя
            for color in pixel:
                binary_message += str(color & 1)  #Только младший бит

    #Преобразование бинарного текста в ASCII
    message = ''.join(chr(int(binary_message[i:i+8], 2)) for i in range(0, len(binary_message), 8))
    return message

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Скрыть или извлечь сообщение из изображения')
    parser.add_argument('mode', choices=['hide', 'reveal'], help='Режим работы: hide для скрытия, reveal для извлечения')
    parser.add_argument('image', type=str, help='Путь к изображению')
    parser.add_argument('--message', type=str, help='Сообщение для скрытия (только в режиме hide)')
    parser.add_argument('--output', type=str, help='Путь для сохранения изображения с встроенным сообщением (только в режиме hide)')
    args = parser.parse_args()

    if args.mode == 'hide':
        if not args.message or not args.output:
            parser.error("Необходимо указать сообщение и путь для сохранения изображения")
        hide_message(args.image, args.message, args.output)
        print("Сообщение успешно скрыто в изображении.")
    elif args.mode == 'reveal':
        hidden_message = reveal_message(args.image)
        print("Извлеченное сообщение:", hidden_message)





