import os
import sys
import requests
import time
import json
import random
from discord_webhook import DiscordWebhook, DiscordEmbed

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

class ServerWorker:
    def __init__(self, serverip, isratelimit):
        self.serverip = serverip
        self.prevresponse = None
        self.isratelimit = isratelimit
        self.is_running = True
        self.sentnotif = False

    def stop(self):
        self.is_running = False

    def get_random_cat_image(self):
        response = requests.get("https://api.thecatapi.com/v1/images/search")
        data = response.json()
        if data and "url" in data[0]:
            return data[0]["url"]
        return None

    def run(self):
        while self.is_running:
            try:
                response = requests.get(self.serverip, timeout=3)
                result = response.text.strip()

                if result != self.prevresponse:
                    if not self.sentnotif:
                        webhook_url = "WEBHOOK_HERE"
                        if result == "ratelimit_osuweb":
                            message = "You are being rate-limited by the osu! website"
                        elif result == "ratelimit_api":
                            message = "You are being rate-limited by the API"
                        else:
                            cat_image_url = self.get_random_cat_image()
                            if cat_image_url:
                                embed = DiscordEmbed(title="osu!papamobil", color=int("b85cff", 16))
                                embed.set_image(url=cat_image_url)
                                message = "A new map has been released! Name: " + result
    
                        webhook = DiscordWebhook(url=webhook_url, content=message)
                        webhook.add_embed(embed)
    
                        response = webhook.execute()
    
                        self.sentnotif = True
                        self.prevresponse = result
                        
                    time.sleep(5)
            except requests.exceptions.Timeout:
                pass
            except requests.exceptions.RequestException as e:
                print("Error during request:", e)

def main():
    serverip = "http://localhost:5000"
    isratelimit = False
    worker = ServerWorker(serverip, isratelimit)
    worker.run()

if __name__ == "__main__":
    main()
