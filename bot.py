import time
import os
import tweepy
from openai import OpenAI

# --- VARIABLES DE ENTORNO ---
BEARER_TOKEN = os.getenv("BEARER_TOKEN")
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_SECRET = os.getenv("ACCESS_SECRET")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

USERNAME_OBJETIVO = "maxinfo_"

client_openai = OpenAI(api_key=OPENAI_API_KEY)

client = tweepy.Client(
    bearer_token=BEARER_TOKEN,
    consumer_key=API_KEY,
    consumer_secret=API_SECRET,
    access_token=ACCESS_TOKEN,
    access_token_secret=ACCESS_SECRET
)

ultimo_tweet_id = None

def traducir(texto):
    respuesta = client_openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Traduce al catalán de forma natural"},
            {"role": "user", "content": texto}
        ]
    )
    return respuesta.choices[0].message.content

while True:
    try:
        user = client.get_user(username=USERNAME_OBJETIVO)
        tweets = client.get_users_tweets(id=user.data.id)

        if tweets.data:
            for tweet in tweets.data:
                global ultimo_tweet_id

                if ultimo_tweet_id is None or tweet.id > ultimo_tweet_id:
                    texto_traducido = traducir(tweet.text)
                    client.create_tweet(text=texto_traducido)
                    ultimo_tweet_id = tweet.id

        time.sleep(60)

    except Exception as e:
        print("Error:", e)
        time.sleep(120)
