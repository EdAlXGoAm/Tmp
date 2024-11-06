from TC_Common.CreateTCcommon import val_field
from typing import List, Dict
import re

class IndexTree():
    def __init__(self):
        self.active = False
        self.index_of_interest = 0
        self.index_lines = []
        self.dict_index = {}
        
    def append_if_is_index_of_interest(self, line):
        if self.index_of_interest == 0:
            self.index_lines.append(line)
            return self.index_lines
        if re.search(rf"^{self.index_of_interest}", line):
            self.index_lines.append(line)
        return self.index_lines

    def create_index_tree(self, scrapp, table_of_content=None):
        """
        Scrapp is a text from a file.
        This method, read the Table of Content from file and
        gets the index tree and the path for each deeper element.
        this method is invoked then self.active is True.
        toc = Table of Content
        """
        toc_pending = False
        toc_counter_prev = 1
        toc_counter_next = 1
        if not toc_pending and val_field(table_of_content):
            toc_pending = True
        toc_numbers = []
        for index, line in enumerate(scrapp):
            current_paragraph = ''.join(scrapp[index:])
            print(current_paragraph)
            if toc_pending:
                if re.search(r"^(?!\d{1,2}/\d{1,2}/\d{4})\b\d+(\.\d+)*\b", line):
                    toc_numbers.append(int(re.search(r"^(?!\d{1,2}/\d{1,2}/\d{4})\b\d+(\.\d+)*\b", line).group().split(".")[0]))
                    toc_counter_next = int(re.search(r"^(?!\d{1,2}/\d{1,2}/\d{4})\b\d+(\.\d+)*\b", line).group().split(".")[0])
                if toc_counter_next < toc_counter_prev:
                    toc_pending = False
                    if int(re.search(r"^(?!\d{1,2}/\d{1,2}/\d{4})\b\d+(\.\d+)*\b", line).group().split(".")[0]) in toc_numbers:
                        self.append_if_is_index_of_interest(line)
                toc_counter_prev = toc_counter_next
            else:
                if re.search(r"^(?!\d{1,2}/\d{1,2}/\d{4})\b\d+(\.\d+)*\b", line):
                    if int(re.search(r"^(?!\d{1,2}/\d{1,2}/\d{4})\b\d+(\.\d+)*\b", line).group().split(".")[0]) in toc_numbers:
                        self.append_if_is_index_of_interest(line)
        self.dict_index = self.construir_diccionario_jerarquico(self.index_lines)
        return self.dict_index

    def construir_diccionario_jerarquico(self, lineas: List[str]) -> Dict[str, List[str]]:
        """
        Construye un diccionario donde cada clave es un elemento más profundo (hoja)
        y su valor es una lista de sus ancestros jerárquicos.

        :param lineas: Lista de strings con numeración y texto.
        :return: Diccionario jerárquico.
        """
        # Expresión regular para extraer la numeración y el texto
        patron = re.compile(r"^(\d+(?:\.\d+)*)\s+(.*)$")
        
        # Lista para almacenar (numero, texto)
        elementos = []
        
        for linea in lineas:
            match = patron.match(linea)
            if match:
                numero, texto = match.groups()
                elementos.append((numero, texto))
            else:
                # Asumimos que todas las líneas cumplen con el regex
                raise ValueError(f"Línea no válida: {linea}")
        
        # Crear un diccionario para acceso rápido por número
        numero_a_texto = {numero: f"{numero} {texto}" for numero, texto in elementos}
        
        # Identificar hojas: elementos que no tienen ningún hijo
        hojas = []
        numeros = set(numero for numero, _ in elementos)
        for numero, texto in elementos:
            patron_hijo = re.compile(re.escape(numero) + r"\.\d+")
            # Si no hay ningún número que empiece con 'numero.'
            if not any(n.startswith(numero + '.') for n in numeros):
                hojas.append((numero, texto))
        
        # Construir el diccionario jerárquico
        diccionario = {}
        for hoja_numero, hoja_texto in hojas:
            partes = hoja_numero.split('.')
            ancestros = []
            for i in range(1, len(partes)):
                anc_numero = '.'.join(partes[:i])
                anc_texto = numero_a_texto.get(anc_numero)
                if anc_texto:
                    ancestros.append(anc_texto)
                else:
                    # Manejo de errores si falta algún ancestro
                    raise ValueError(f"Ancestro no encontrado para: {anc_numero}")
            # Clave es la representación completa de la hoja
            clave = f"{hoja_numero} {hoja_texto}"
            diccionario[clave] = {
                "ancestros" : ancestros,
                "texto" : None,
            }
        return diccionario