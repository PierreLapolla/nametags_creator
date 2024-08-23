from pathlib import Path
from typing import List

import yaml
from reportlab.lib.utils import simpleSplit


def load_config(config_file: Path) -> dict:
    """
    Charge la configuration à partir d'un fichier YAML.
    Si le fichier n'existe pas, il est créé avec un contenu par défaut.
    """
    if not config_file.exists():
        print(
            f"Le fichier de configuration '{config_file}' est introuvable. Création d'un fichier de configuration par défaut.")
        default_config = {
            'chemin_vers_le_fichier_de_noms': 'noms.txt',
            'largeur_cellule_cm': 4.0,
            'hauteur_cellule_cm': 2.5,
            'police': 'Helvetica-Bold'
        }
        try:
            with config_file.open('w') as file:
                yaml.safe_dump(default_config, file)
            print(f"Fichier de configuration par défaut créé à : {config_file}")
        except Exception as e:
            raise Exception(f"Erreur lors de la création du fichier de configuration : {str(e)}")
        return default_config
    else:
        try:
            with config_file.open('r') as file:
                config = yaml.safe_load(file)
            return config
        except Exception as e:
            raise Exception(f"Erreur lors du chargement de la configuration : {str(e)}")


def load_names_from_file(file_path: Path) -> List[str]:
    """
    Charge les noms à partir d'un fichier texte.
    Si le fichier n'existe pas, il est créé avec un contenu par défaut.
    """
    if not file_path.exists():
        print(f"Le fichier '{file_path}' est introuvable. Création d'un fichier de noms par défaut.")
        default_names = [
            "Alice Dupont",
            "Théo Leblanc",  # Example with accent
            "Claire Leblanc",
            "David Petit",
            "Emma Moreau"
        ]
        try:
            with file_path.open('w', encoding='utf-8') as file:
                file.write("\n".join(default_names))
            print(f"Fichier de noms par défaut créé à : {file_path}")
        except Exception as e:
            raise Exception(f"Erreur lors de la création du fichier des noms : {str(e)}")
        return default_names
    else:
        try:
            with file_path.open('r', encoding='utf-8') as file:
                names = [line.strip() for line in file if line.strip()]
            return names
        except Exception as e:
            raise Exception(f"Erreur lors du chargement des noms : {str(e)}")


def calculate_font_size(text: str, max_width: float, max_height: float, font_name: str) -> int:
    """
    Calcule la taille de police maximale pour que le texte tienne dans les dimensions spécifiées.
    """
    font_size = 24

    while font_size > 1:
        lines = simpleSplit(text, font_name, font_size, max_width)
        text_width = max(len(line) * (font_size / 2) for line in lines)
        text_height = len(lines) * font_size * 1.2

        if text_width <= max_width and text_height <= max_height:
            break
        font_size -= 1

    return font_size
