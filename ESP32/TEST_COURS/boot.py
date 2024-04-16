import network

NEED_WIFI = False

def connect_wifi(ssid, password):
    wlan = network.WLAN(network.STA_IF)  # Crée un objet WLAN en mode STA
    if not wlan.isconnected():  # Vérifie si déjà connecté
        wlan.active(True)  # Active l'interface STA
        wlan.connect(ssid, password)  # Tente de se connecter au réseau
        print('Connexion au réseau', ssid)
        while not wlan.isconnected():
            pass  # Attendre jusqu'à la connexion
    print('Configuration réseau :', wlan.ifconfig())

if NEED_WIFI:
    connect_wifi('S23 Manu', 'Kibishi47')
