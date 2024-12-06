import os
import pdfplumber
import pandas as pd
import json
import sys
import bleach
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

def procesar_lineas(page, x_tol, y_tol, table_bboxes, page_indicada_from, page_indicada_to, i, all_lines):
    """
    Procesa las líneas de una página y las agrega a la lista all_lines.

    :param page: Objeto de la página del PDF.
    :param x_tol: Tolerancia horizontal para agrupar caracteres en palabras.
    :param y_tol: Tolerancia vertical para agrupar líneas de texto.
    :param table_bboxes: Lista de bounding boxes de las tablas en la página.
    :param page_indicada_from: Número de página a partir de la cual considerar las líneas.
    :param page_indicada_to: Número de página hasta la cual considerar las líneas.
    :param i: Número actual de página en el bucle.
    :param all_lines: Lista donde se almacenan todas las líneas procesadas.
    """
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

    for index, (_, line_words) in enumerate(sorted_lines):
        # Construir el texto de la línea
        line_text = ' '.join([w['text'] for w in line_words])

        # Obtener bounding box de la línea
        x0 = min(w['x0'] for w in line_words)
        y0 = min(w['top'] for w in line_words)
        x1 = max(w['x1'] for w in line_words)
        y1 = max(w['bottom'] for w in line_words)
        line_bbox = (x0, y0, x1, y1)
        table_count = -1

        # Verificar si la línea está dentro de alguna tabla
        en_tabla = False
        index_table = 0
        for table_bbox in table_bboxes:
            index_table += 1
            if bbox_overlap(line_bbox, table_bbox):
                en_tabla = True
                table_count = index_table
                break

        # Almacenar la línea con su información
        is_last_line = index == len(sorted_lines) - 1
        if page_indicada_from is not None and page_indicada_to is not None:
            is_first_line_of_page_indicada = index == 0 and i >= page_indicada_from and i <= page_indicada_to
        else:
            is_first_line_of_page_indicada = False    

        if not is_last_line and not is_first_line_of_page_indicada:
            all_lines.append({
                'page': i,
                'text': line_text,
                'x0': x0,
                'en_tabla': en_tabla,
                'number_of_table': table_count
            })

def calcular_indentacion(x0, min_x0, pixels_per_space, formato):
    """
    Calcula la cantidad de espacios de indentación basada en la posición x0.

    :param x0: Posición horizontal de la línea.
    :param min_x0: Mínima posición horizontal para establecer la base de indentación.
    :param pixels_per_space: Número de píxeles que representan un espacio de indentación.
    :return: Cadena de espacios para la indentación.
    """
    indent_pixels = x0 - min_x0
    if indent_pixels < 0:
        indent_pixels = 0  # Evitar valores negativos

    num_spaces = int(indent_pixels // pixels_per_space)
    return ' ' * num_spaces if formato == 'texto' else '&nbsp;' * num_spaces

def extraer_texto_con_marcado_e_indentacion(pdf_path, output_dir, x_tol=2, y_tol=3, pixels_per_space=5, page_indicada_from=None, page_indicada_to=None, formato='texto'):
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

    dict_of_tables = {}

    with pdfplumber.open(pdf_path) as pdf:
        table_count = 0

        for i, page in enumerate(pdf.pages, start=1):
            # Extraer tablas y sus bounding boxes
            tables = page.find_tables()
            table_bboxes = [table.bbox for table in tables]

            # Llamar a la función para procesar las líneas
            procesar_lineas(page, x_tol, y_tol, table_bboxes, page_indicada_from, page_indicada_to, i, all_lines)

            # Extraer y guardar tablas en CSV y en el texto plano
            for table in tables:
                table_count += 1
                # Obtener los datos de la tabla
                table_data = table.extract()
                if table_data:
                    df = pd.DataFrame(table_data[1:], columns=table_data[0])  # Asumiendo que la primera fila es el encabezado
                    table_filename = os.path.join(output_dir, f"tabla_{i}_{table_count}.csv")
                    df.to_csv(table_filename, index=False, encoding='utf-8')

                    # Formatear la tabla para el texto plano
                    tabla_texto = formatear_tabla(table_data, 'texto')
                    tabla_html = formatear_tabla(table_data, 'html')
                    dict_of_tables[table_count] = tabla_html if formato == 'html' else tabla_texto

    # Determinar el mínimo x0 para establecer la base de indentación
    min_x0 = min(line['x0'] for line in all_lines if not line['en_tabla'] and line['x0'] > 0)  # Excluir líneas sin texto

    text = ""
    for line in all_lines:
        if line['en_tabla']:
            # Insertar el número de la tabla
            if line['number_of_table'] in dict_of_tables:
                if formato == 'html':
                    text += f"{dict_of_tables[line['number_of_table']]}\n"
                else:
                    text += f"{dict_of_tables[line['number_of_table']]}\n"
                # Eliminar la tabla del diccionario
                del dict_of_tables[line['number_of_table']]
        else:
            # Usar la nueva función para calcular la indentación
            spaces = calcular_indentacion(line['x0'], min_x0, pixels_per_space, formato)

            # Agregar la línea con indentación al texto
            if formato == 'html':
                text += f"{spaces}{line['text']}\n"
            else:
                text += f"{spaces}{line['text']}\n"

    # Escribir el texto al archivo de salida
    if formato == 'texto':
        with open(f"{output_dir}/texto_pdf.txt", 'w', encoding='utf-8') as f:
            f.write(text)

    if formato == 'html':
        return text
    else:
        return text

def formatear_tabla(table_data, formato='texto'):
    """
    Formatea los datos de la tabla en un formato especificado: texto plano o HTML.

    :param table_data: Lista de listas con los datos de la tabla.
    :param formato: Formato de salida, 'texto' para texto plano o 'html' para HTML.
    :return: Cadena de texto formateada en el formato especificado.
    """
    if not table_data:
        return ""

    if formato == 'html':
        # Iniciar la tabla HTML con bordes más gruesos
        html = "<table style='border: 2px solid black; border-collapse: collapse;'>"

        # Formatear el encabezado de la tabla
        header = table_data[0]
        html += "<thead><tr>"
        for cell in header:
            html += f"<th style='border: 1px solid black; padding: 5px;'>{bleach.clean(cell)}</th>"
        html += "</tr></thead>"

        # Formatear las filas de la tabla
        html += "<tbody>"
        for row in table_data[1:]:
            html += "<tr>"
            for cell in row:
                html += f"<td style='border: 1px solid black; padding: 5px;'>{bleach.clean(cell)}</td>"
            html += "</tr>"
        html += "</tbody>"

        # Cerrar la tabla HTML
        html += "</table>"

        return html

    elif formato == 'texto':
        # Obtener el ancho máximo de cada columna
        num_columns = len(table_data[0])
        col_widths = [0] * num_columns
        for row in table_data:
            for i, cell in enumerate(row):
                col_widths[i] = max(col_widths[i], len(str(cell)))

        # Crear el separador de columnas con barras horizontales gruesas
        separador = '┼'.join(['─' * round(w*0.75) for w in col_widths])
        separador = f"┌{separador}┐"

        # Formatear cada fila con barras verticales gruesas
        filas_formateadas = [separador]
        for idx, row in enumerate(table_data):
            fila = ' │ '.join([f" {str(cell).ljust(col_widths[i])} " for i, cell in enumerate(row)])
            filas_formateadas.append(f"│{fila}│")
            if idx == 0:
                filas_formateadas.append(separador.replace('┌', '├').replace('┐', '┤'))  # Agregar separador después del encabezado

        filas_formateadas.append(separador.replace('┌', '└').replace('┐', '┘'))  # Agregar el cierre de la tabla

        return '\n'.join(filas_formateadas)

    else:
        raise ValueError("Formato no soportado. Use 'texto' o 'html'.")