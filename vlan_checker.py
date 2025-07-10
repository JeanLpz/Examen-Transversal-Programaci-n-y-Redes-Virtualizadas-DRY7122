
def verificar_vlan():
    try:
        vlan = int(input("Ingrese el número de VLAN: "))
        
        if 1 <= vlan <= 1005:
            print(f"VLAN {vlan} pertenece al rango NORMAL (1-1005)")
        elif 1006 <= vlan <= 4094:
            print(f"VLAN {vlan} pertenece al rango EXTENDIDO (1006-4094)")
        else:
            print("¡Error! El número de VLAN debe estar entre 1 y 4094")
            
    except ValueError:
        print("¡Debe ingresar un número válido!")


if __name__ == "__main__":
    verificar_vlan()