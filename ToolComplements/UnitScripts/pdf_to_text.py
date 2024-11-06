import os
import pdfplumber
import pandas as pd

def extraer_texto_y_tablas(pdf_path, output_text_path, output_tables_dir):
    """
    Extrae texto y tablas de un archivo PDF.

    :param pdf_path: Ruta al archivo PDF.
    :param output_text_path: Ruta donde se guardará el texto extraído.
    :param output_tables_dir: Directorio donde se guardarán las tablas extraídas.
    """
    # Asegurarse de que el directorio para tablas existe
    os.makedirs(output_tables_dir, exist_ok=True)

    # Abrir el PDF
    with pdfplumber.open(pdf_path) as pdf:
        all_text = ""
        table_count = 0

        # Iterar sobre cada página
        for i, page in enumerate(pdf.pages, start=1):
            # Extraer texto
            text = page.extract_text(x_tolerance=2, y_tolerance=3)
            if text:
                all_text += f"--- Página {i} ---\n{text}\n\n"

            # Extraer tablas
            tables = page.extract_tables()
            for table in tables:
                table_count += 1
                df = pd.DataFrame(table[1:], columns=table[0])  # Asumiendo que la primera fila es el encabezado
                table_filename = os.path.join(output_tables_dir, f"tabla_{i}_{table_count}.csv")
                df.to_csv(table_filename, index=False, encoding='utf-8')
                print(f"Tabla extraída y guardada en: {table_filename}")

    # Guardar todo el texto extraído en un archivo de texto
    with open(output_text_path, 'w', encoding='utf-8') as f:
        f.write(all_text)
    print(f"Texto extraído y guardado en: {output_text_path}")

if __name__ == "__main__":
    import sys

    # Obtener el directorio del script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    tmp_dir = os.path.join(script_dir, "tmp")

    # Nombre del archivo PDF (puedes cambiarlo según tu archivo)
    pdf_filename = "DIA 1.pdf"  # Reemplaza con el nombre de tu archivo PDF
    pdf_path = os.path.join(tmp_dir, pdf_filename)

    # Rutas de salida
    output_text_path = os.path.join(tmp_dir, "texto_extraido.txt")
    output_tables_dir = os.path.join(tmp_dir, "tablas_extraidas")

    # Verificar que el archivo PDF existe
    if not os.path.isfile(pdf_path):
        print(f"El archivo PDF no se encontró en: {pdf_path}")
        sys.exit(1)

    # Llamar a la función de extracción
    extraer_texto_y_tablas(pdf_path, output_text_path, output_tables_dir)