import time
import os
from TC_Common.SelectorCmd import CMDSelector

def save_screen():
    print("\033[?1049h", end="")  # Cambia al buffer alternativo

def restore_screen():
    print("\033[?1049l", end="")  # Restaurar el buffer original

def temporary_screen():
    print("Esta es una pantalla temporal.")
    print("Aquí puedes mostrar lo que quieras...")
    time.sleep(3)  # Espera 3 segundos antes de restaurar

input("hola:")

# Selector que probablemente esté causando el problema
selector = CMDSelector()
selector.title = "Select an option:"
selector.options = ["Option 1", "Option 2", "Option 3"]
selected_option = selector.select()

# Guardar el estado de la pantalla actual
save_screen()

# Mostrar algo en la pantalla temporal
temporary_screen()

# Restaurar la pantalla original
restore_screen()

# Mensaje final después de la restauración
print("La pantalla original ha sido restaurada.")
