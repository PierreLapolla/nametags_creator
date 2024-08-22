import math
from typing import List
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm, inch
from reportlab.platypus import Paragraph, SimpleDocTemplate, Table, TableStyle
from reportlab.lib.utils import simpleSplit


def load_names_from_file(file_path: Path) -> List[str]:
    """
    Charge les noms à partir d'un fichier texte.
    """
    while not file_path.exists():
        print(f"Erreur : le fichier '{file_path}' est introuvable.")
        file_path = Path(input("Veuillez entrer le chemin correct pour le fichier des noms : "))

    try:
        with file_path.open('r') as file:
            names = [line.strip() for line in file if line.strip()]
        return names
    except Exception as e:
        raise Exception(f"Erreur lors du chargement des noms : {str(e)}")


def calculate_font_size(text: str, max_width: float, max_height: float) -> int:
    font_size = 24  # Start with a default large font size

    while font_size > 1:  # Loop until we find a font size that fits or reach the minimum size
        lines = simpleSplit(text, 'Helvetica-Bold', font_size, max_width)
        text_width = max(len(line) * (font_size / 2) for line in lines)  # Estimate width
        text_height = len(lines) * font_size * 1.2  # Estimate height, including line spacing

        if text_width <= max_width and text_height <= max_height:
            break  # If it fits, stop the loop
        font_size -= 1  # Reduce font size and try again

    return font_size


def generate_nametags(names: List[str], cell_width_cm: float, cell_height_cm: float) -> None:
    """
    Génère un fichier PDF de badges nominatifs avec les noms fournis.
    """
    cell_width = cell_width_cm * cm
    cell_height = cell_height_cm * cm

    columns = int((letter[0] - inch) // cell_width)
    rows = int((letter[1] - inch) // cell_height)

    tags_per_page = columns * rows
    total_tags = len(names)
    total_pages = math.ceil(total_tags / tags_per_page)

    pdf_file = "badges_nominatifs.pdf"
    document = SimpleDocTemplate(pdf_file, pagesize=letter)
    elements = []
    styles = getSampleStyleSheet()
    name_style = styles['Title']

    for page in range(total_pages):
        start_index = page * tags_per_page
        end_index = min(start_index + tags_per_page, total_tags)
        data = []

        for i in range(start_index, end_index):
            full_name = names[i]
            font_size = calculate_font_size(full_name, cell_width // 2, cell_height // 2)
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
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))

        elements.append(table)
        if page < total_pages - 1:
            elements.append(Paragraph("<br/>", styles['Normal']))

    try:
        document.build(elements)
        print(f"PDF de badges nominatifs généré : {pdf_file}")
    except Exception as e:
        raise Exception(f"Erreur lors de la génération du PDF : {str(e)}")


if __name__ == "__main__":
    try:
        file_path = Path('noms.txt')
        names = load_names_from_file(file_path)
        generate_nametags(names, cell_width_cm=4, cell_height_cm=2.5)
    except Exception as e:
        print(f"Erreur : {str(e)}")
