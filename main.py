# Importez le module datetime
from datetime import datetime

def afficher_date():
    # Obtenez la date actuelle
    current_date = datetime.now()

    # Affichez la date actuelle dans le format souhaité
    print(f"Today's date is {current_date.strftime('%a. %d %b. %Y')}")

if __name__ == '__main__':
    afficher_date()
