from flask import Flask, jsonify, request
from flask_cors import CORS
from ServerLibs.PdfToText import extraer_texto_con_marcado_e_indentacion
from ServerLibs.ScrappingPDF import PDFScrapper
import json
import re

app = Flask(__name__)
CORS(app)

global_text = ""
global_pdf_scrapper = None

@app.route('/api/pdf_to_text_tables_text', methods=['POST'])
def pdf_to_text_tables_text():
    global global_text
    data = request.get_json()
    text = extraer_texto_con_marcado_e_indentacion(
        data['pdf_path'], data['output_dir'], x_tol=2, y_tol=3, pixels_per_space=5, 
        page_indicada_from=data['page_indicada_from'], page_indicada_to=data['page_indicada_to'], formato='texto')
    global_text = text.split('\n')
    return jsonify({"text": text})

@app.route('/api/pdf_to_text_tables_html', methods=['POST'])
def pdf_to_text_tables_html():
    global global_text
    data = request.get_json()
    text = extraer_texto_con_marcado_e_indentacion(
        data['pdf_path'], data['output_dir'], x_tol=2, y_tol=3, pixels_per_space=5, 
        page_indicada_from=data['page_indicada_from'], page_indicada_to=data['page_indicada_to'], formato='html')
    global_text = text.split('\n')
    return jsonify({"text": text})

@app.route('/api/get_index_tree', methods=['POST'])
def get_index_tree():
    global global_pdf_scrapper
    global global_text
    data = request.get_json()
    global_pdf_scrapper = PDFScrapper(data['pdf_path'], data['output_dir'], data['mapping_path'], global_text, data['index_to_search'])
    global_pdf_scrapper.preparing_paragraphs()
    return jsonify({
        "paragraphs": global_pdf_scrapper.paragraphs,
        "paragraphs_descarted": global_pdf_scrapper.paragraphs_descarted
    })

def replace_functions_in_paragraphs(paragraphs, paragraphs_reusable):
    # Crear un diccionario para acceder rápidamente a los elementos reutilizables por su título sin el índice numérico
    reusable_dict = {}
    for pr in paragraphs_reusable:
        new_title = re.sub(r'^\d+\.\d+\s+', '', pr['title'])
        reusable_dict[new_title] = pr['element']

    # Expresión regular para encontrar patrones como "Step FUNCTION_NAME () (page NUMBER)"
    pattern = re.compile(r'Step\s+(\w+)\s*\(\)\s*\(page\s+\d+\)', re.IGNORECASE)

    for paragraph in paragraphs:
        # Revisar las secciones donde pueden estar las referencias
        for section in ['Preparation', 'Main Part', 'Completion']:
            if section in paragraph['element']:
                original_text = paragraph['element'][section]
                nuevo_texto = original_text

                while True:
                    # Función de reemplazo
                    def reemplazar(match):
                        function_name = match.group(1)
                        elemento_reusable = reusable_dict.get(function_name)
                        if elemento_reusable:
                            return elemento_reusable.get('Main Part', '')  # Reemplazar con el contenido reutilizable
                        else:
                            return match.group(0)  # Dejar el texto original si no se encuentra

                    # Aplicar la sustitución
                    texto_reemplazado = pattern.sub(reemplazar, nuevo_texto)

                    # Verificar si hubo cambios
                    if texto_reemplazado == nuevo_texto:
                        break  # No se encontraron más patrones, salir del bucle
                    else:
                        nuevo_texto = texto_reemplazado  # Actualizar el texto para la siguiente iteración

                # Actualizar el texto de la sección
                paragraph['element'][section] = nuevo_texto

    return paragraphs

def replace_functions_in_paragraphs_as_tables(paragraphs, paragraphs_reusable):
    def re_escape_html(text):
        """
        Función auxiliar para escapar caracteres especiales en HTML.
        """
        escape_table = {
            "&": "&amp;",
            "\"": "&quot;",
            "'": "&#x27;",
            ">": "&gt;",
            "<": "&lt;",
        }
        return "".join(escape_table.get(c, c) for c in text)

    # Crear un diccionario para acceder rápidamente a los elementos reutilizables por su título sin el índice numérico
    reusable_dict = {}
    for pr in paragraphs_reusable:
        new_title = re.sub(r'^\d+\.\d+\s+', '', pr['title'])
        reusable_dict[new_title] = pr['element']

    # Expresión regular para encontrar patrones como "Step FUNCTION_NAME () (page NUMBER)"
    pattern = re.compile(r'Step\s+(\w+)\s*\(\)\s*\(page\s+\d+\)', re.IGNORECASE)

    for paragraph in paragraphs:
        # Revisar las secciones donde pueden estar las referencias
        for section in ['Preparation', 'Main Part', 'Completion']:
            if section in paragraph['element']:
                original_text = paragraph['element'][section]
                lineas = original_text.split('\n')
                
                # Crear una lista de diccionarios para rastrear las líneas y sus reemplazos
                lineas_reemplazo = [{'original': linea, 'reemplazo': ''} for linea in lineas]

                cambiaron = True
                while cambiaron:
                    cambiaron = False
                    for idx, linea_dict in enumerate(lineas_reemplazo):
                        # Determinar la línea actual: si ya hay un reemplazo, usarlo; de lo contrario, usar el original
                        linea_actual = linea_dict['reemplazo'] if linea_dict['reemplazo'] else linea_dict['original']
                        
                        def reemplazar(match):
                            nonlocal cambiaron
                            function_name = match.group(1)
                            elemento_reusable = reusable_dict.get(function_name)
                            if elemento_reusable:
                                reemplazo = elemento_reusable.get('Main Part', '')
                                cambiaron = True
                                return reemplazo  # Reemplazar con el contenido reutilizable
                            else:
                                return match.group(0)  # Dejar el texto original si no se encuentra

                        # Aplicar la sustitución en la línea actual
                        nueva_linea = pattern.sub(reemplazar, linea_actual)
                        if nueva_linea != (linea_dict['reemplazo'] if linea_dict['reemplazo'] else linea_dict['original']):
                            lineas_reemplazo[idx]['reemplazo'] = nueva_linea

                # Construir las filas de la tabla HTML con bordes gruesos
                tabla_html = '<table style="border-collapse: collapse; border: 2px solid black;">'
                for linea_dict in lineas_reemplazo:
                    original = linea_dict['original']
                    reemplazo = linea_dict['reemplazo'] if linea_dict['reemplazo'] else ''
                    if paragraph['title'] == '2.2.1.4 Start Subfunction':
                        # print(f"reemplazo: {reemplazo}")
                        print(reemplazo.replace('\n', '<br>'))
                    reemplazo = reemplazo.replace('\n', '<br>')
                    tabla_html += f'<tr><td style="border: 1px solid black;">{original}</td><td style="border: 1px solid black;">{reemplazo}</td></tr>'
                tabla_html += '</table>'

                # Actualizar el texto de la sección con la tabla
                paragraph['element'][section] = tabla_html

    return paragraphs


@app.route('/api/replaceFunctions', methods=['POST'])
def replace_functions():
    global global_pdf_scrapper
    global global_text
    data = request.get_json()
    # paragraphs = replace_functions_in_paragraphs(data['paragraphs'], data['paragraphs_reusable'])
    paragraphs = replace_functions_in_paragraphs_as_tables(data['paragraphs'], data['paragraphs_reusable'])
    return jsonify({
        "paragraphs": paragraphs
    })

if __name__ == '__main__':
    # Habilitar el modo de depuración
    app.debug = True

    # Especificar archivos adicionales para monitorear
    extra_files = ['Tmp/ToolComplements/ServerLibs/PdfToText.py', 'Tmp/ToolComplements/ServerLibs/ScrappingPDF.py']

    # Ejecutar la aplicación con recarga automática
    app.run(host='127.0.0.1', port=5000, extra_files=extra_files)
