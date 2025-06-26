# telegramcorobot

Aquest és un bot de Telegram per a la coral, que permet:
- Sol·licitar partitures i rebre-les en privat.
- Veure el catàleg de partitures disponibles.
- Capturar file_id de fitxers (PDF, àudio, imatges) enviats en privat per afegir-los al catàleg.

## Comandes principals

- `/cataleg` : Mostra la llista de partitures disponibles.
- `/partitura <nom>` : Envia la partitura sol·licitada en privat.
- Enviar fitxers en privat per obtenir el `file_id` i afegir-los al catàleg.

## Desplegament

El bot es pot desplegar a Railway (https://railway.app) amb aquestes instruccions:

1. Crear un projecte a Railway i connectar-lo amb aquest repositori GitHub.
2. Afegir la variable d'entorn `BOT_TOKEN` amb el token del bot.
3. Configurar UptimeRobot per fer ping a `/ping` cada 5 minuts per mantenir el bot actiu 24/7.
4. Afegir el bot al grup de Telegram amb permisos d'administrador per esborrar missatges.

## Afegir partitures

1. Enviar el fitxer en privat al bot per obtenir el `file_id`.
2. Afegir el `file_id` i el nom al diccionari `PARTITURES` dins del fitxer `main.py`.
3. Fer un commit i pujar els canvis a GitHub perquè Railway faci el desplegament automàtic.

---

Per a més informació o ajuda, contacta amb l'autor del projecte.
