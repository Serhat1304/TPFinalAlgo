import schedule
import time
import datetime
from app.models import entrainer_depuis_bdd

# Fonction de job
def job():
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print("Début de l'entraînement du modèle...")
    
    try:
        entrainer_depuis_bdd()
    except Exception as e:
        message = f"[{now}] Erreur lors de l'entraînement : {str(e)}\n"

    print(message)

schedule.every().monday.at("02:00").do(job)

print("Cron en cours d'exécution... (CTRL+C pour arrêter)")

while True:
    try:
        schedule.run_pending()
        time.sleep(60)
    except KeyboardInterrupt:
        print("Cron arrêté manuellement.")
        break
    except Exception as e:
        print(f"Erreur : {e}")
