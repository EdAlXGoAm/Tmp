def add_at_beginning_of_dict(dictionary, key, value):
    # Agregar un par llave-valor al principio de un diccionario
    return {key: value, **dictionary}

def add_at_beginning_of_dict(dictionary, key, value): 
    # Remover la llave si ya existe para luego agregarla al principio
    dictionary.pop(key, None)  # Elimina la llave si existe
    return {key: value, **dictionary}

def move_at_beginning_of_dict(dictionary, key, default=None):
    # Mover una llave al principio del diccionario
    if key in dictionary:
        value = dictionary[key]
        del dictionary[key]
        return add_at_beginning_of_dict(dictionary, key, value)
    elif default is not None:
        return add_at_beginning_of_dict(dictionary, key, default)
    return dictionary

def copy_dict_key(dictionary, origin_key, dest_key):
    # Copiar el valor de la llave origen a la llave destino si no es None
    if origin_key in dictionary and dictionary[origin_key] is not None:
        return add_at_beginning_of_dict(dictionary, dest_key, dictionary[origin_key])
    return dictionary

def remove_dict_key(dictionary, key):
    # Eliminar la llave si existe en el diccionario
    if key in dictionary:
        del dictionary[key]
    return dictionary

def subarrays_to_dicts(data):
    new_data = {}
    for key, value in data.items():
        if value is not None:
            if isinstance(value, dict):
                new_data[key] = value
            elif isinstance(value, list) and all(isinstance(item, dict) for item in value):
                new_data[key] = {f"Item {index + 1}": item for index, item in enumerate(value)}
            else:
                new_data[key] = value
    return new_data

def elevate_key(d, key):
    """
    Eleva una llave de un diccionario si existe en el nivel superior y su valor es una cadena de texto.

    Parámetros:
    d (dict): El diccionario a procesar.
    key (str): La llave a evaluar y posiblemente elevar.

    Retorna:
    dict: El diccionario modificado con la llave elevada si se cumplen las condiciones,
          de lo contrario, retorna el diccionario original.
    """
    if key in d and isinstance(d[key], str):
        new_key = d[key]
        # Crear un nuevo diccionario sin la llave original
        new_value = {k: v for k, v in d.items() if k != key}
        # Retornar el nuevo diccionario con la llave elevada
        return {new_key: new_value}
    else:
        # Si la llave no existe o su valor no es una cadena, retorna el diccionario original
        return d

def convert_keys_to_dict(data, keys_to_convert, subkey=None):
    """
    Recursively searches for specified keys in a nested dictionary and converts
    lists of dictionaries into dictionaries with keys formatted as "Item {index}".

    Args:
        data (dict): The input dictionary to process.
        keys_to_convert (list): List of keys to search and convert.

    Returns:
        dict: A new dictionary with the specified conversions applied.
    """
    if not isinstance(data, dict):
        return data  # Base case: if data is not a dict, return as is

    new_data = {}
    for key, value in data.items():
        if isinstance(value, dict):
            # Recursively process sub-dictionaries
            new_data[key] = convert_keys_to_dict(value, keys_to_convert)
        elif isinstance(value, list):
            # Check if the current key needs to be converted
            if key in keys_to_convert and all(isinstance(item, dict) for item in value):
                # Convert list of dicts to a dict with "Item {index}" keys
                converted_list = {f"Step {index + 1}": convert_keys_to_dict(item, keys_to_convert, subkey)
                                  for index, item in enumerate(value)}
                new_data[key] = converted_list
            else:
                # Otherwise, process each item in the list recursively
                new_data[key] = [convert_keys_to_dict(item, keys_to_convert) if isinstance(item, dict) else item
                                 for item in value]
        else:
            # For other data types, assign the value directly
            new_data[key] = value
    if subkey:
        return elevate_key(new_data, subkey)
    return new_data

def convert_keys_to_strings(obj, target_keys, indent_level=0):
    """
    Recorre recursivamente un objeto (diccionario o lista) y convierte
    las ocurrencias de 'target_keys' que sean listas o diccionarios en listas de strings formateados.

    Args:
        obj: El objeto a procesar (puede ser dict, list o cualquier otro tipo).
        target_keys: El nombre de la clave que se busca para convertir su valor.
        indent_level: Nivel de indentación actual para el formateo de strings.

    Returns:
        El objeto procesado con las ocurrencias de 'target_keys' convertidas en listas de strings.
    """
    if isinstance(obj, dict):
        new_dict = {}
        for key, value in obj.items():
            if key in target_keys:
                if isinstance(value, dict):
                    # Convertir el diccionario en una lista de strings formateados
                    formatted = format_dict(value, indent=indent_level)
                    new_dict[key] = formatted
                elif isinstance(value, list):
                    if is_deepest_list(value):
                        # Convertir la lista en una lista de strings formateados
                        formatted_list = []
                        for item in value:
                            if isinstance(item, dict):
                                formatted = format_dict(item, indent=indent_level)
                                formatted_list.extend(formatted)
                            else:
                                formatted_list.append(str(item))
                            formatted_list.append("")
                        new_dict[key] = formatted_list
                    else:
                        # Si la lista no es la más profunda, procesarla recursivamente
                        new_dict[key] = [convert_keys_to_strings(item, target_keys, indent_level) for item in value]
                else:
                    # Si el valor no es ni dict ni list, dejarlo tal cual
                    new_dict[key] = value
            else:
                # Para otras claves, seguir recorriendo recursivamente
                new_dict[key] = convert_keys_to_strings(value, target_keys, indent_level)
        return new_dict
    elif isinstance(obj, list):
        return [convert_keys_to_strings(item, target_keys, indent_level) for item in obj]
    else:
        return obj

def convert_keys_arrays_to_strings(obj, target_keys, indent_level=0):
    """
    Recorre recursivamente un objeto (diccionario o lista) y convierte las listas
    asociadas a una clave específica en listas de strings formateados.

    Args:
        obj: El objeto a procesar (puede ser dict, list o cualquier otro tipo).
        target_key: El nombre de la clave cuya lista asociada se desea convertir.
        indent_level: Nivel de indentación actual para el formateo de strings.

    Returns:
        El objeto procesado con las listas específicas convertidas en listas de strings.
    """
    if isinstance(obj, dict):
        # Si es un diccionario, procesar cada clave y valor
        new_dict = {}
        for key, value in obj.items():
            if key in target_keys and isinstance(value, list):
                # Si la clave coincide y el valor es una lista, convertirla
                new_dict[key] = convert_list_to_formatted_strings(value, indent_level)
            else:
                # De lo contrario, aplicar recursión
                new_dict[key] = convert_keys_arrays_to_strings(value, target_keys, indent_level)
        return new_dict
    elif isinstance(obj, list):
        # Si es una lista, procesar cada elemento
        return [convert_keys_arrays_to_strings(item, target_keys, indent_level) for item in obj]
    else:
        # Si no es ni dict ni list, devolver el objeto tal cual
        return obj

def convert_list_to_formatted_strings(lst, indent_level=0):
    """
    Convierte una lista de diccionarios en una lista de strings formateados.

    Args:
        lst: La lista a convertir.
        indent_level: Nivel de indentación actual para el formateo de strings.

    Returns:
        Una lista de strings representando los elementos formateados.
    """
    if not is_deepest_list(lst):
        # Si la lista no es la más profunda, no la convertimos
        return lst

    result = []
    for item in lst:
        if isinstance(item, dict):
            formatted = format_dict(item, indent=indent_level)
            result.extend(formatted)
        else:
            # Si el elemento no es un diccionario, simplemente convertirlo a string
            result.append(str(item))
    return result

def convert_deepest_arrays_to_strings(obj, indent_level=0):
    """
    Recorre recursivamente un objeto (diccionario o lista) y convierte los arrays más profundos
    en arrays de strings formateados.

    Args:
        obj: El objeto a procesar (puede ser dict, list o cualquier otro tipo).
        indent_level: Nivel de indentación actual para el formateo de strings.

    Returns:
        El objeto procesado con los arrays más profundos convertidos en arrays de strings.
    """
    if isinstance(obj, dict):
        # Si es un diccionario, procesar cada clave y valor
        new_dict = {}
        for key, value in obj.items():
            new_dict[key] = convert_deepest_arrays_to_strings(value, indent_level)
        return new_dict
    elif isinstance(obj, list):
        if is_deepest_list(obj):
            # Si es el array más profundo, convertir cada diccionario en strings formateados
            result = []
            for item in obj:
                if isinstance(item, dict):
                    formatted = format_dict(item, indent=indent_level)
                    result.extend(formatted)
                else:
                    # Si el elemento no es un diccionario, simplemente convertirlo a string
                    result.append(str(item))
            return result
        else:
            # Si no es el array más profundo, seguir recorriendo sus elementos
            return [convert_deepest_arrays_to_strings(item, indent_level) for item in obj]
    else:
        # Si no es ni dict ni list, devolver el objeto tal cual
        return obj

def is_deepest_list(lst):
    """
    Determina si una lista es el array más profundo, es decir, que ninguno de sus elementos
    contiene a su vez una lista.

    Args:
        lst: La lista a verificar.

    Returns:
        True si es el array más profundo, False de lo contrario.
    """
    for item in lst:
        if isinstance(item, dict):
            for value in item.values():
                if isinstance(value, list):
                    return False
        elif isinstance(item, list):
            return False
    return True

def format_dict(d, indent=0):
    """
    Formatea un diccionario en una lista de strings con indentación.

    Args:
        d: El diccionario a formatear.
        indent: Nivel de indentación actual.

    Returns:
        Una lista de strings representando el diccionario formateado.
    """
    lines = []
    indent_str = '\t' * indent  # Dos espacios por nivel de indentación
    for key, value in d.items():
        if isinstance(value, dict):
            lines.append(f"{indent_str}{key}:")
            lines.extend(format_dict(value, indent + 1))
        else:
            lines.append(f"{indent_str}{key}: {value}")
    return lines

def convert_keys_to_strings_new(obj, target_keys, indent_level=0):
    """
    Recorre recursivamente un objeto (diccionario o lista) y convierte
    las ocurrencias de 'target_keys' que sean listas o diccionarios en listas de strings formateados.
    Omite cualquier clave cuyo valor sea None.

    Args:
        obj: El objeto a procesar (puede ser dict, list o cualquier otro tipo).
        target_keys: El nombre de la clave que se busca para convertir su valor.
        indent_level: Nivel de indentación actual para el formateo de strings.

    Returns:
        El objeto procesado con las ocurrencias de 'target_keys' convertidas en listas de strings.
    """
    if isinstance(obj, dict):
        new_dict = {}
        for key, value in obj.items():
            if value is None:
                # Omitir claves con valor None
                continue

            if key in target_keys:
                if isinstance(value, dict):
                    # Convertir el diccionario en una lista de strings formateados
                    formatted = format_dict_new(value, indent=indent_level)
                    new_dict[key] = formatted
                elif isinstance(value, list):
                    if is_deepest_list_new(value):
                        # Convertir la lista en una lista de strings formateados
                        formatted_list = []
                        for item in value:
                            if isinstance(item, dict):
                                formatted = format_dict_new(item, indent=indent_level)
                                formatted_list.extend(formatted)
                            else:
                                if item is not None:
                                    formatted_list.append(str(item))
                        new_dict[key] = formatted_list
                    else:
                        # Si la lista no es la más profunda, procesarla recursivamente
                        processed_list = []
                        for item in value:
                            processed_item = convert_keys_to_strings_new(item, target_keys, indent_level)
                            if processed_item is not None:
                                processed_list.append(processed_item)
                        new_dict[key] = processed_list
                else:
                    # Si el valor no es ni dict ni list, dejarlo tal cual si no es None
                    new_dict[key] = value
            else:
                # Para otras claves, seguir recorriendo recursivamente
                processed_value = convert_keys_to_strings_new(value, target_keys, indent_level)
                if processed_value is not None:
                    new_dict[key] = processed_value
        return new_dict
    elif isinstance(obj, list):
        processed_list = []
        for item in obj:
            processed_item = convert_keys_to_strings_new(item, target_keys, indent_level)
            if processed_item is not None:
                processed_list.append(processed_item)
        return processed_list if processed_list else None
    else:
        return obj

def format_dict_new(d, indent=0):
    """
    Formatea un diccionario en una lista de strings con indentación.
    Omite cualquier clave cuyo valor sea None.

    Args:
        d: El diccionario a formatear.
        indent: Nivel de indentación actual.

    Returns:
        Una lista de strings representando el diccionario formateado.
    """
    lines = []
    indent_str = '\t' * indent  # Dos espacios por nivel de indentación
    for key, value in d.items():
        if value is None:
            # Omitir claves con valor None
            continue

        if isinstance(value, dict):
            lines.append(f"{indent_str}{key}:")
            lines.extend(format_dict_new(value, indent + 1))
        elif isinstance(value, list):
            if is_list_of_strings_new(value):
                # Si la lista es una lista de strings formateados previamente
                lines.append(f"{indent_str}{key}:")
                for item in value:
                    lines.append(f"{indent_str}{indent_str}{item}")
            else:
                # Si la lista no es una lista de strings, formatearla normalmente
                lines.append(f"{indent_str}{key}:")
                for item in value:
                    if isinstance(item, dict):
                        lines.extend(format_dict_new(item, indent + 1))
                    elif item is not None:
                        lines.append(f"{indent_str}{indent_str}{item}")
        else:
            lines.append(f"{indent_str}{key}: {value}")
    return lines

def is_list_of_strings_new(lst):
    """
    Verifica si una lista está compuesta únicamente por cadenas de caracteres.

    Args:
        lst: La lista a verificar.

    Returns:
        True si todos los elementos son strings, False de lo contrario.
    """
    return all(isinstance(item, str) for item in lst)

def is_deepest_list_new(lst):
    """
    Verifica si una lista es la más profunda (no contiene diccionarios ni listas).

    Args:
        lst: La lista a verificar.

    Returns:
        True si la lista no contiene diccionarios ni listas, False de lo contrario.
    """
    return all(not isinstance(item, (dict, list)) for item in lst)

def obtener_llaves_primer_nivel(lista_diccionarios):
    """
    Recorre una lista de diccionarios y extrae todas las llaves de primer nivel.

    Args:
        lista_diccionarios (list): Lista que contiene diccionarios.

    Returns:
        list: Lista de cadenas con todas las llaves de primer nivel encontradas.
    """
    llaves = []

    for diccionario in lista_diccionarios:
        if isinstance(diccionario, dict):
            llaves.extend(diccionario.keys())

    # Si deseas eliminar duplicados, descomenta la siguiente línea:
    llaves = list(set(llaves))

    return llaves

def evaluar_llaves(lista_diccionarios):
    """
    Recorre una lista de diccionarios y evalúa si los valores de cada llave de primer nivel
    son cadenas de texto o listas de cadenas de texto. Devuelve una lista de diccionarios
    con el resultado de la evaluación para cada llave, sin duplicados.

    Args:
        lista_diccionarios (list): Lista que contiene diccionarios.

    Returns:
        list: Lista de diccionarios con la evaluación de cada llave.
    """
    from collections import defaultdict

    # Diccionario para almacenar la evaluación de cada llave
    evaluaciones = defaultdict(lambda: True)

    for diccionario in lista_diccionarios:
        if isinstance(diccionario, dict):
            for llave, valor in diccionario.items():
                if evaluaciones[llave]:  # Solo evalúa si aún es True
                    if isinstance(valor, str):
                        continue  # Es una cadena, cumple la condición
                    elif isinstance(valor, list):
                        # Verifica que todos los elementos en la lista sean cadenas
                        if not all(isinstance(item, str) for item in valor):
                            evaluaciones[llave] = False
                    else:
                        # Si no es string ni lista de strings, no cumple
                        evaluaciones[llave] = False

    # Convertir el diccionario de evaluaciones a una lista de diccionarios
    resultado = [{llave: valor} for llave, valor in evaluaciones.items()]
    return resultado

def transform_single_key_lists(data):
    if isinstance(data, dict):
        new_dict = {}
        for key, value in data.items():
            # Verificar si el valor es una lista de diccionarios con una única clave de tipo cadena
            if (isinstance(value, list) and 
                all(isinstance(item, dict) and 
                    len(item) == 1 and 
                    all(isinstance(v, str) for v in item.values()) 
                    for item in value)):
                # Extraer los valores de las únicas claves presentes en cada diccionario
                new_dict[key] = [next(iter(item.values())) for item in value]
            else:
                # Recursivamente procesar el valor
                new_dict[key] = transform_single_key_lists(value)
        return new_dict
    elif isinstance(data, list):
        return [transform_single_key_lists(item) for item in data]
    else:
        return data

def transform_values(data):
    if isinstance(data, dict):
        new_dict = {}
        for key, value in data.items():
            # Caso 1: Valor es una lista de diccionarios con una única clave de tipo cadena
            if (isinstance(value, list) and 
                all(isinstance(item, dict) and 
                    len(item) == 1 and 
                    all(isinstance(v, str) for v in item.values()) 
                    for item in value)):
                new_dict[key] = [next(iter(item.values())) for item in value]
            
            # Caso 2: Valor es un diccionario con una única clave de tipo cadena
            elif (isinstance(value, dict) and 
                  len(value) == 1 and 
                  all(isinstance(v, str) for v in value.values())):
                new_dict[key] = next(iter(value.values()))
            
            else:
                # Recursivamente procesar el valor
                new_dict[key] = transform_values(value)
        return new_dict
    
    elif isinstance(data, list):
        return [transform_values(item) for item in data]
    
    else:
        return data

def join_string_arrays(data):
    if isinstance(data, dict):
        return {k: join_string_arrays(v) for k, v in data.items()}
    elif isinstance(data, list) and all(isinstance(i, str) for i in data):
        return "\n".join(data)
    elif isinstance(data, list):
        return [join_string_arrays(item) for item in data]
    else:
        return data

def recursive_evaluation_keys(element, keys):
    for key in keys:
        if element.get(key):
            element = element[key]
        else:
            return None
    return True