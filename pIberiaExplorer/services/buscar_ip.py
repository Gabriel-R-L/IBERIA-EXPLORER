import urllib
def buscar_ip():
    try:
        with urllib.request.urlopen('https://ident.me') as response:
            return response.read().decode('utf8')
    except Exception as e:
        print(f"Error al intentar obtener la IP: {e}")