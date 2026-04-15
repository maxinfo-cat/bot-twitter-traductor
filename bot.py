import time
import os
import requests
import tweepy

# =========================
# CONFIGURACIÓN (RAILWAY)
# =========================

BEARER_TOKEN = os.getenv("BEARER_TOKEN")
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_SECRET = os.getenv("ACCESS_SECRET")

USERNAME_OBJETIVO = "AQUI_EL_USUARIO"

# =========================
# CLIENTE X (TWITTER)
# =========================

client = tweepy.Client(
    bearer_token=BEARER_TOKEN,
    consumer_key=API_KEY,
    consumer_secret=API_SECRET,
    access_token=ACCESS_TOKEN,
    access_token_secret=ACCESS_SECRET
)

# =========================
# TRADUCCIÓN (LIBRETRANSLATE)
# =========================

def traducir(texto):
    try:
        url = "https://libretranslate.de/translate"

        payload = {
            "q": texto,
            "source": "auto",
            "target": "ca",
            "format": "text"
        }

        response = requests.post(url, data=payload, timeout=10)
        return response.json()["translatedText"]

    except Exception as e:
        print("Error traducción:", e)
        return texto  # si falla, publica el original

# =========================
# BOT LOOP
# =========================

ultimo_tweet_id = None

print("Bot iniciado...")

while True:
    try:
        user = client.get_user(username=USERNAME_OBJETIVO)

        tweets = client.get_users_tweets(
            id=user.data.id,
            max_results=5
        )

        if tweets.data:
            for tweet in reversed(tweets.data):

                if ultimo_tweet_id is None or tweet.id > ultimo_tweet_id:

                    print("Tweet encontrado:", tweet.text)

                    texto_traducido = traducir(tweet.text)

                    print("Publicando:", texto_traducido)

                    client.create_tweet(text=texto_traducido)

                    ultimo_tweet_id = tweet.id

        time.sleep(60)

    except Exception as e:
        print("Error general:", e)
        time.sleep(120)
