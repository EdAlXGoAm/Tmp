import os
import pdfplumber
import pandas as pd
import sys
os.environ["PYDEVD_WARN_SLOW_RESOLVE_TIMEOUT"] = "1.0"

def bbox_overlap(bbox1, bbox2):
    """
    Verifica si dos bounding boxes se superponen.

    :param bbox1: Tuple (x0, y0, x1, y1) del primer bbox.
    :param bbox2: Tuple (x0, y0, x1, y1) del segundo bbox.
    :return: True si se superponen, False de lo contrario.
    """
    x0_1, y0_1, x1_1, y1_1 = bbox1
    x0_2, y0_2, x1_2, y1_2 = bbox2

    return not (x1_1 < x0_2 or x1_2 < x0_1 or y1_1 < y0_2 or y1_2 < y0_1)

def extraer_texto_con_marcado_e_indentacion(pdf_path, output_dir, x_tol=2, y_tol=3, pixels_per_space=5, page_indicada=None):
    """
    Extrae texto de un PDF utilizando pdfplumber con marcadores para líneas que corresponden a tablas
    y aplica indentación basada en la posición horizontal de las líneas.

    :param pdf_path: Ruta al archivo PDF.
    :param output_dir: Ruta donde se guardará el texto extraído con marcadores e indentación.
    :param output_dir: Directorio donde se guardarán las tablas extraídas.
    :param x_tol: Tolerancia horizontal para agrupar caracteres en palabras.
    :param y_tol: Tolerancia vertical para agrupar líneas de texto.
    :param pixels_per_space: Número de píxeles que representan un espacio de indentación.
    """
    # Asegurarse de que el directorio para tablas existe
    os.makedirs(output_dir, exist_ok=True)

    all_lines = []  # Lista para almacenar todas las líneas con su información

    with pdfplumber.open(pdf_path) as pdf:
        table_count = 0

        for i, page in enumerate(pdf.pages, start=1):
            # Extraer tablas y sus bounding boxes
            tables = page.find_tables()
            table_bboxes = [table.bbox for table in tables]

            # Extraer palabras con posiciones
            words = page.extract_words(x_tolerance=x_tol, y_tolerance=y_tol)

            # Agrupar palabras por línea basándose en la coordenada y
            lines = {}
            for word in words:
                top = round(word['top'], 1)  # Redondear para agrupar líneas cercanas
                if top in lines:
                    lines[top].append(word)
                else:
                    lines[top] = [word]

            # Ordenar las líneas por posición vertical
            sorted_lines = sorted(lines.items(), key=lambda x: x[0])

            # for _, line_words in sorted_lines:
            for index, (_, line_words) in enumerate(sorted_lines):
                # Construir el texto de la línea
                line_text = ' '.join([w['text'] for w in line_words])

                # Obtener bounding box de la línea
                x0 = min(w['x0'] for w in line_words)
                y0 = min(w['top'] for w in line_words)
                x1 = max(w['x1'] for w in line_words)
                y1 = max(w['bottom'] for w in line_words)
                line_bbox = (x0, y0, x1, y1)

                # Verificar si la línea está dentro de alguna tabla
                en_tabla = False
                for table_bbox in table_bboxes:
                    if bbox_overlap(line_bbox, table_bbox):
                        en_tabla = True
                        break

                # [EDALXGOAM] !Edition!
                # Almacenar la línea con su información
                is_last_line = index == len(sorted_lines) - 1
                if page_indicada is not None:
                    is_first_line_of_page_indicada = index == 0 and i >= page_indicada
                else:
                    is_first_line_of_page_indicada = False    
                # [EDALXGOAM] !Edition!
                if not is_last_line and not is_first_line_of_page_indicada:
                    all_lines.append({
                        'page': i,
                        'text': line_text,
                        'x0': x0,
                        'en_tabla': en_tabla
                    })

            # Extraer y guardar tablas en CSV
            for table in tables:
                table_count += 1
                # Obtener los datos de la tabla
                table_data = table.extract()
                if table_data:
                    df = pd.DataFrame(table_data[1:], columns=table_data[0])  # Asumiendo que la primera fila es el encabezado
                    table_filename = os.path.join(output_dir, f"tabla_{i}_{table_count}.csv")
                    df.to_csv(table_filename, index=False, encoding='utf-8')
                    print(f"Tabla extraída y guardada en: {table_filename}")
                else:
                    print(f"Tabla {table_count} en página {i} está vacía.")

            # Agregar separador de página (opcional, puede omitirse si se prefiere)
            all_lines.append({
                'page': i,
                'text': f"--- Fin de Página {i} ---",
                'x0': 0,
                'en_tabla': False
            })

    # Determinar el mínimo x0 para establecer la base de indentación
    min_x0 = min(line['x0'] for line in all_lines if not line['en_tabla'] and line['x0'] > 0)  # Excluir líneas sin texto

    # Aplicar indentación y escribir el texto al archivo de salida
    with open(f"{output_dir}/texto_pdf.txt", 'w', encoding='utf-8') as f:
        for line in all_lines:
            if line['en_tabla']:
                # Marcar la línea como parte de una tabla
                f.write(f"[INICIO DE TABLA]\n{line['text']}\n")
            else:
                if line['text'].startswith("--- Fin de Página"):
                    # Escribir el separador de página sin indentación
                    # [EDALXGOAM] !Edition!
                    # f.write(f"{line['text']}\n\n")
                    print(f"{line['text']}\n\n")
                else:
                    # Calcular la indentación basada en x0
                    indent_pixels = line['x0'] - min_x0
                    if indent_pixels < 0:
                        indent_pixels = 0  # Evitar valores negativos

                    # Calcular el número de espacios
                    num_spaces = int(indent_pixels // pixels_per_space)

                    # Crear la cadena de espacios
                    spaces = ' ' * num_spaces

                    # Escribir la línea con indentación
                    f.write(f"{spaces}{line['text']}\n")
                        # Rewrite the text file
    text = ""
    with open(f"{output_dir}/texto_pdf.txt", 'r', encoding='utf-8') as f:
        for line in f.readlines():
            text += line
    all_lines = text.split('\n')
    return all_lines

# if __name__ == "__main__":
#     # Obtener el directorio del script
#     script_dir = os.path.dirname(os.path.abspath(__file__))
#     tmp_dir = os.path.join(script_dir, "../tmp")

#     # Nombre del archivo PDF (actualiza según tu archivo)
#     pdf_filename = "DIA 1.pdf"  # Reemplaza con el nombre de tu archivo PDF
#     pdf_path = os.path.join(tmp_dir, pdf_filename)

#     # Rutas de salida
#     output_dir = os.path.join(tmp_dir, "texto_extraido_marcado_e_indentacion.txt")
#     output_dir = os.path.join(tmp_dir, "tablas_extraidas_indentadas")


#     page_indicada = 6 # Página a partir de la cual se omiten las líneas inicia

#     # Llamar a la función de extracción con marcadores e indentación
#     extraer_texto_con_marcado_e_indentacion(pdf_path, output_dir, x_tol=2, y_tol=3, pixels_per_space=5, page_indicada=page_indicada)
