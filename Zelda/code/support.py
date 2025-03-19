from csv import reader
from os import walk
import pygame

def import_csv_layout(path):
    """
    Importa um layout de mapa a partir de um arquivo CSV.

    :param path: Caminho do arquivo CSV.
    :return: Lista de listas representando o layout do mapa.
    """
    terrain_map = []
    try:
        with open(path, 'r') as level_map:
            layout = reader(level_map, delimiter=',')
            for row in layout:
                terrain_map.append(list(row))
    except FileNotFoundError:
        print(f"Erro: Arquivo CSV não encontrado em {path}")
    return terrain_map

def import_folder(path):
    """
    Importa todas as imagens de uma pasta e as converte em superfícies Pygame.

    :param path: Caminho da pasta contendo as imagens.
    :return: Lista de superfícies Pygame.
    """
    surface_list = []
    try:
        for _, _, img_files in walk(path):
            for image in img_files:
                full_path = f"{path}/{image}"
                try:
                    image_surf = pygame.image.load(full_path).convert_alpha()
                    surface_list.append(image_surf)
                except pygame.error:
                    print(f"Erro: Não foi possível carregar a imagem {full_path}")
    except FileNotFoundError:
        print(f"Erro: Pasta não encontrada em {path}")
    return surface_list