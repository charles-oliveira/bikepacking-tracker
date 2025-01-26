import geocoder

# Capturar localização atual com base no IP
def get_current_location():
    try:
        g = geocoder.ip('me')  # Captura a localização com base no IP
        if g.ok:
            return {
                "latitude": g.latlng[0],
                "longitude": g.latlng[1],
                "cidade": g.city or "Desconhecida",
            }
        else:
            raise ValueError("Erro ao capturar a localização.")
    except Exception as e:
        raise RuntimeError(f"Erro ao obter localização atual: {e}")
