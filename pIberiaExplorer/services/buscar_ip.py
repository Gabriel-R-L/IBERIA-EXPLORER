import socket


# Función que busca la IP del usuario
def buscar_ip():
    try:
        return socket.gethostbyname(socket.gethostname())
    except Exception as e:
        print(f"Error al intentar obtener la IP: {e}")