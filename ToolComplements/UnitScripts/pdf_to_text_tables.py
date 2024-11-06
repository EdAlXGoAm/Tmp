import os
import pdfplumber
import pandas as pd
import sys

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

def extraer_texto_con_marcado_tablas(pdf_path, output_text_path, output_tables_dir, x_tol=3, y_tol=4):
    """
    Extrae texto de un PDF utilizando pdfplumber con marcadores para líneas que corresponden a tablas.

    :param pdf_path: Ruta al archivo PDF.
    :param output_text_path: Ruta donde se guardará el texto extraído con marcadores.
    :param output_tables_dir: Directorio donde se guardarán las tablas extraídas.
    :param x_tol: Tolerancia horizontal para agrupar caracteres en palabras.
    :param y_tol: Tolerancia vertical para agrupar líneas de texto.
    """
    # Asegurarse de que el directorio para tablas existe
    os.makedirs(output_tables_dir, exist_ok=True)

    with pdfplumber.open(pdf_path) as pdf:
        all_text = ""
        table_count = 0

        for i, page in enumerate(pdf.pages, start=1):
            # Extraer tablas y sus bounding boxes
            tables = page.find_tables()
            table_bboxes = [table.bbox for table in tables]  # Corregido aquí

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

            for _, line_words in sorted_lines:
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

                if en_tabla:
                    # Marcar la línea como parte de una tabla
                    all_text += f"[INICIO DE TABLA]\n{line_text}\n"
                else:
                    # Agregar la línea como texto normal
                    all_text += f"{line_text}\n"

            # Extraer y guardar tablas en CSV
            for table in tables:
                table_count += 1
                # Obtener los datos de la tabla
                table_data = table.extract()
                if table_data:
                    df = pd.DataFrame(table_data[1:], columns=table_data[0])  # Asumiendo que la primera fila es el encabezado
                    table_filename = os.path.join(output_tables_dir, f"tabla_{i}_{table_count}.csv")
                    df.to_csv(table_filename, index=False, encoding='utf-8')
                    print(f"Tabla extraída y guardada en: {table_filename}")
                else:
                    print(f"Tabla {table_count} en página {i} está vacía.")

            # Agregar separador de página
            all_text += f"\n--- Fin de Página {i} ---\n\n"

    # Guardar el texto extraído con marcadores en un archivo de texto con codificación UTF-8
    with open(output_text_path, 'w', encoding='utf-8') as f:
        f.write(all_text)
    print(f"Texto extraído con marcadores y guardado en: {output_text_path}")

if __name__ == "__main__":
    # Obtener el directorio del script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    tmp_dir = os.path.join(script_dir, "tmp")

    # Nombre del archivo PDF (actualiza según tu archivo)
    pdf_filename = "DIA 1.pdf"  # Reemplaza con el nombre de tu archivo PDF
    pdf_path = os.path.join(tmp_dir, pdf_filename)

    # Rutas de salida
    output_text_path = os.path.join(tmp_dir, "texto_extraido_marcado.txt")
    output_tables_dir = os.path.join(tmp_dir, "tablas_extraidas_marcado")

    # Verificar que el archivo PDF existe
    if not os.path.isfile(pdf_path):
        print(f"El archivo PDF no se encontró en: {pdf_path}")
        sys.exit(1)

    # Parámetros de tolerancia ajustados
    x_tolerance = 2  # Puedes experimentar con valores entre 2 y 5
    y_tolerance = 3  # Puedes experimentar con valores entre 3 y 6

    # Llamar a la función de extracción con marcadores para tablas
    extraer_texto_con_marcado_tablas(pdf_path, output_text_path, output_tables_dir, x_tol=x_tolerance, y_tol=y_tolerance)
