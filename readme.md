# Esteganografia de Texto em Imagem

Este repositório implementa um algoritmo de esteganografia LSB (Bit Menos Significativo, do inglês Least Significant Bit) escondendo um texto dentro de uma imagem.

## Requisitos

Para rodar o programa é necessário possuir:
- Python > 3.6
- cv2

## Execução

O programa pode ser executado de maneira interativa:

```bash
python stego.py
```

Ou com uma entrada pré-definida:

```bash
cat input.txt | python stego.py
```

```bash
cat longinput.txt | python stego.py
```

```bash
cat input-dec.txt | python stego.py
```

## Limitações

Dentre as limitações do programa, destacam-se:
- Funciona apenas com o formato png, pois outros podem comprimir a imagem e distorcer o bit menos significativo

## Referências

As seguintes referências nortearam a implementação deste programa:
- https://www.section.io/engineering-education/steganography-in-python/
- https://betterprogramming.pub/image-steganography-using-python-2250896e48b9
- https://stackoverflow.com/questions/12523586/python-format-size-application-converting-b-to-kb-mb-gb-tb/63839503