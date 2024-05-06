import time
import requests
import string
import random
import threading
num = int(input("How many Chars : "))
token = ""  # INSERT YOUR TOKEN INTO THE QUOTES. DO NOT SHARE THIS TOKEN.
proxya = "" # INSERT YOUR RESIDENTIAL PROXY HERE ( TO AVOID RATE LIMIT )
webhookUrl = "" # INSERT YOUR WEBHOOK URL TO GET A NOTIFICATION WHEN USERNAME IS AVAILABLE - LEAVE EMPTY TO SET NOTIFICATIONS (OFF)



headers = {"Authorization": token}
endpoint = "https://discord.com/api/v9/users/@me/pomelo-attempt"

def generate_random_username(a):
    return ''.join(random.choices(string.ascii_lowercase, k=a))

available_usernames = []
thread_lock = threading.Lock()

def check_username_availability():

    while True:
        username = generate_random_username(num)
        url = endpoint
        body = {
            "username": username
        }
        try:
            response = requests.post(url, headers=headers, json=body)  

            if response.status_code == 429:
                sleep_time = response.json()["retry_after"]

            if response.json()["taken"] == False:
                with thread_lock:
                    print(f"{username} is available")
                    payload = {
                        "content": f"{username} is not taken, Snipped by Mano. Enjoy it to the max @everyone",
                        "username": "Mano Is much better than you babe",
                        "avatar_url": "https://images-ext-2.discordapp.net/external/UNGTQ29t9HMev5cfsYW70gkWeoVTO0rOYDd2ozGAhfU/%3Fsize%3D1024/https/cdn.discordapp.com/icons/1144850550731575391/1cc1ae3f21f71cfd69b2d94576745fad.png?format=webp&quality=lossless&width=479&height=479",  # Replace with the URL of your thumbnail
                    }
                    if webhookUrl != "" and webhookUrl != None : 
                        response = requests.post(webhookUrl, json=payload)

                        if response.status_code == 204:
                            print(f"Notification sent to webhook for {username}")
                        else:
                            print(f"Failed to send notification to webhook. Status code: {response.status_code}")
            
                with thread_lock:
                    available_usernames.append(username)

            elif response.json()["taken"] == True:
                with thread_lock:
                    print(f"{username} is taken")

            # Some other error
            else:
                with thread_lock:
                    print(f"Error checking {username}: {response.json()}")
        except Exception as e:
            with thread_lock:
                print("Error Occurd Please Check The Inputs !")

threads = []

for _ in range(50):
    thread = threading.Thread(target=check_username_availability())
    thread.start()
    threads.append(thread)

for thread in threads:
    thread.join()

with open("available_usernames.txt", "w") as file:
    file.write("\n".join(available_usernames))
