import math
import time
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Table, TableStyle

from helpers import load_config, load_names_from_file, calculate_font_size


def generate_nametags(names, cell_width_cm, cell_height_cm, font_name):
    """
    Génère un fichier PDF de badges nominatifs avec les noms fournis.
    """
    cell_width = cell_width_cm * cm
    cell_height = cell_height_cm * cm

    columns = int((letter[0]) // cell_width)
    rows = int((letter[1]) // cell_height)

    tags_per_page = columns * rows
    total_tags = len(names)
    total_pages = math.ceil(total_tags / tags_per_page)

    pdf_file = "badges_nominatifs.pdf"
    document = SimpleDocTemplate(
        pdf_file,
        pagesize=letter,
        leftMargin=0,
        rightMargin=0,
        topMargin=0,
        bottomMargin=0
    )
    elements = []
    styles = getSampleStyleSheet()
    name_style = styles['Title']

    for page in range(total_pages):
        start_index = page * tags_per_page
        end_index = min(start_index + tags_per_page, total_tags)
        data = []

        for i in range(start_index, end_index):
            full_name = names[i]
            font_size = calculate_font_size(full_name, cell_width // 2, cell_height // 2, font_name)
            name_style.fontSize = font_size
            name_paragraph = Paragraph(full_name, name_style)
            data.append(name_paragraph)

        data_reshaped = [data[i:i + columns] for i in range(0, len(data), columns)]

        table = Table(data_reshaped, colWidths=[cell_width] * columns, rowHeights=[cell_height] * len(data_reshaped))
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.white),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('FONTNAME', (0, 0), (-1, -1), font_name),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))

        elements.append(table)

    try:
        document.build(elements)
        print(f"PDF de badges nominatifs généré : {pdf_file}")
    except Exception as e:
        raise Exception(f"Erreur lors de la génération du PDF : {str(e)}")


if __name__ == "__main__":
    try:
        config = load_config(Path('config.yaml'))
        file_path = Path(config['chemin_vers_le_fichier_de_noms'])
        names = load_names_from_file(file_path)
        cell_width_cm = float(config['largeur_cellule_cm'])
        cell_height_cm = float(config['hauteur_cellule_cm'])
        font_name = config['police']
        generate_nametags(names, cell_width_cm, cell_height_cm, font_name)
    except Exception as e:
        print(f"Erreur : {str(e)}")
    finally:
        time.sleep(10)
