# Script para mostrar nombres de integrantes
integrantes = [
    "Juan Pérez",
    "María Gómez",
    "Carlos Rodríguez"
]

print("=== Integrantes del Grupo ===")
for i, nombre in enumerate(integrantes, 1):
    print(f"{i}. {nombre}")