from csv import reader
from os import walk
import pygame

def load_map_layout(file_path):
    """
    Carrega um arquivo CSV contendo o layout do mapa e retorna como matriz
    
    Args:
        file_path (str): Caminho para o arquivo CSV do mapa
        
    Returns:
        list: Matriz bidimensional representando o layout do mapa
    """
    map_layout = []
    
    try:
        with open(file_path) as map_file:
            map_data = reader(map_file, delimiter=',')
            for row in map_data:
                # Converte cada linha do CSV em uma lista de strings
                map_layout.append(list(row))
                
    except FileNotFoundError:
        print(f"Erro: Arquivo de mapa não encontrado em {file_path}")
        return []
    
    return map_layout

def load_image_assets(folder_path):
    """
    Carrega todas as imagens de um diretório como superfícies Pygame
    
    Args:
        folder_path (str): Caminho para a pasta contendo as imagens
        
    Returns:
        list: Lista de superfícies Pygame convertidas com alpha
    """
    image_surfaces = []
    
    try:
        # Percorre todos os arquivos no diretório
        for root, dirs, files in walk(folder_path):
            for file_name in files:
                # Constrói o caminho completo do arquivo
                full_path = f"{folder_path}/{file_name}"
                
                try:
                    # Carrega a imagem com preservação de transparência
                    image = pygame.image.load(full_path).convert_alpha()
                    image_surfaces.append(image)
                    
                except pygame.error as e:
                    print(f"Erro ao carregar imagem {file_name}: {e}")
    
    except FileNotFoundError:
        print(f"Erro: Diretório não encontrado em {folder_path}")
        return []
    
    return image_surfaces
