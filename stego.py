import cv2
import math
import re
import os


def encrypt():
    text = None
    while True:
        text = input("Input text to insert into the image:\n")
        if len(text) > 0:
            break
        else:
            print("Please enter text to continue!")

    image, image_file = load_image()

    output_file = None
    pattern = re.compile("([^\\s]+(\\.(?i)png)$)")
    while True:
        output_file = input("Output image file:\n")
        if pattern.findall(output_file):
            break
        else:
            print(
                "Please enter a valid output image file with extension (.png,.jpeg,.jpg)!")

    # transforma texto em binario
    text = [format(ord(i), '08b') for i in text]
    _, width, _ = image.shape
    # calcula qtd de pixels necessarios para o texto
    qtd_pix = len(text) * 3
    # calcula qtd de linhas necessarias para o texto baseado na largura da imagem
    rows = qtd_pix/width
    rows = math.ceil(rows)

    # conta os bits incluidos de 3 em 3
    count = 0
    # conta caracteres incluidos na imagem
    char_included = 0
    # percorre as linhas necessarias para incluir o texto
    for i in range(rows):
        # insere o texto na linha
        while(count < width and char_included < len(text)):
            char = text[char_included]
            char_included += 1
            # percorre os bits de cada caracter
            for index_c, c in enumerate(char):
                # caso o bit for 1, garante que o valor na imagem eh nao divisivel
                # caso o bit for 0, garante que o valor na imagem eh divisivel
                if c == '1' and image[i][count][index_c % 3] % 2 == 0:
                    image[i][count][index_c % 3] -= 1
                elif c == '0' and image[i][count][index_c % 3] % 2 == 1:
                    image[i][count][index_c % 3] = round_by_two(
                        image[i][count][index_c % 3])
                # contabiliza cada RGB preenchido
                if(index_c % 3 == 2):
                    count += 1
                # insere EOF (nao divisivel) caso texto tenha terminado
                if(index_c == 7):
                    # se nao finalizou de inserir texto, garante divisivel
                    if(char_included*3 < qtd_pix and image[i][count][2] % 2 == 1):
                        image[i][count][2] = round_by_two(image[i][count][2])
                    # se finalizou de inserir texto, garante nao divisivel (EOF)
                    if(char_included*3 >= qtd_pix and image[i][count][2] % 2 == 0):
                        image[i][count][2] -= 1
                    count += 1
        count = 0

    # escreve imagem com texto escondido
    cv2.imwrite(output_file, image)
    original_size = os.path.getsize(image_file)
    original_formatted = ' '.join(format_bytes(original_size))
    
    encrypted_size = os.path.getsize(output_file)
    encrypted_formatted = ' '.join(format_bytes(encrypted_size))

    diff_formatted = ' '.join(format_bytes(encrypted_size - original_size))
    print(f"The size of original file is {original_formatted}")
    print(f"The size of encrypted file is {encrypted_formatted}")
    print(f"The size difference is {diff_formatted}")


def format_bytes(size):
    # 2**10 = 1024
    power = 2**10
    n = 0
    power_labels = {0 : '', 1: 'kilo', 2: 'mega', 3: 'giga', 4: 'tera'}
    while size > power:
        size /= power
        n += 1
    return f"{size:.2f}", power_labels[n]+'bytes'


def round_by_two(x):
    return 2 * round(x/2)


def even_process(number):
    if number % 2 == 0:
        return '0'
    else:
        return '1'


def decrypt():
    # carrega imagem com texto escondido
    image = load_image()[0]
    text = []
    stop = False
    # percorre linha da imagem
    for _, i in enumerate(image):
        # percorre coluna da imagem
        for index_j, j in enumerate(i):
            # caso ultima camada, verifica por EOF
            if index_j % 3 == 2:
                # primeiro pixel
                text.append(even_process(j[0]))
                # segundo pixel
                text.append(even_process(j[1]))
                # terceiro pixel
                if(j[2] % 2 == 1):
                    stop = True
                    break
            else:
                # primeiro pixel
                text.append(even_process(j[0]))
                # segundo pixel
                text.append(even_process(j[1]))
                # terceiro pixel
                text.append(even_process(j[2]))
        if stop:
            break

    message = []
    # agrupa os bits em grupos de 8
    for i in range(int((len(text)+1)/8)):
        message.append(text[i*8:(i*8+8)])
    # transforma os bits em char
    message = [chr(int(''.join(i), 2)) for i in message]
    # une mensagem final
    message = ''.join(message)
    print("Decrypted message is: " + message)


def load_image():
    image = None
    while True:
        image_file = input("Input image file with extension:\n")
        image = cv2.imread(image_file)
        if image is not None and image.size != 0:
            break
        else:
            print("Please enter valid image file with extension to continue!")
    return image, image_file


if __name__ == '__main__':
    option = None
    while True:
        option = int(
            input("Please select an option:\n""1. Encrypt\n2. Decrypt\n"))
        if option == 1 or option == 2:
            break
        else:
            print("Please enter valid option!")

    if option == 1:
        encrypt()
    else:
        decrypt()


# Refs.:
# https://www.section.io/engineering-education/steganography-in-python/
# https://betterprogramming.pub/image-steganography-using-python-2250896e48b9
# https://stackoverflow.com/questions/12523586/python-format-size-application-converting-b-to-kb-mb-gb-tb/63839503
