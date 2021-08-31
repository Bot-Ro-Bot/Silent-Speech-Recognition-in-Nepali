import os
import vlc
import socket
from gtts import gTTS
from playsound import playsound

from samaye import get_time
from mausam import get_weather

import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
from time import sleep # Import the sleep function from the time module
GPIO.setwarnings(False) # Ignore warning for now
GPIO.setmode(GPIO.BOARD) # Use physical pin numbering

SENTENCES = ["अबको समय सुनाउ",
             "एउटा सङ्गित बजाउ",
             "आजको मौसम बताउ",
             "बत्तिको अवस्था बदल",
             "पङ्खाको स्तिथी बदल"]

PORT = 5050
# SERVER = socket.gethostbyname(socket.gethostname())
SERVER = "192.168.0.112"
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)


class IOT:
    def __init__(self):
        
        self.BATTI = 8
        self.PANKHA = 10
        self.BATTI_FLAG = False
        self.PANKHA_FLAG = False
        GPIO.setup(self.BATTI, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.PANKHA, GPIO.OUT, initial=GPIO.LOW)
		
        self.PLAYLIST = [os.path.join("sangeet",song) for song in os.listdir("sangeet") if song[-3:]=="mp3"]
        # print(self.PLAYLIST)
        global player
        player = vlc.MediaListPlayer()
        VLC = vlc.Instance("--loop")
        media_list = VLC.media_list_new()
        for song in self.PLAYLIST:
            media = VLC.media_new(song)
            media_list.add_media(media)
        player.set_media_list(media_list)

    def sangeet(self):
        if(player.is_playing()):
            player.pause()
            return
        player.play()

    def samaye(self):
        if(player.is_playing()):
            player.pause()
            samaye = get_time()
            self.__speak(samaye)
            player.play()
        else:
            samaye = get_time()
            self.__speak(samaye)

    def mausam(self):
        if(player.is_playing()):
            player.pause()
            mausam = get_weather()
            self.__speak(mausam)
            player.play()
        else:
            mausam = get_weather()
            self.__speak(mausam)

    def batti(self):
        self.BATTI_FLAG = not self.BATTI_FLAG
        GPIO.output(self.BATTI, self.BATTI_FLAG)
        print("Batti status: ",self.BATTI_FLAG)
        pass

    def pankha(self):
        self.PANKA_FLAG = not self.PANKA_FLAG
        GPIO.output(self.BATTI, self.PANKA_FLAG)
        print("Pankha status: ",self.PANKA_FLAG)
        pass

    def __speak(self, text):
        speak = gTTS(text=text, lang="ne", slow=False)
        file = "audio.mp3"
        speak.save(file)
        playsound(file)
        os.remove(file)


def start_server():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")

def receive():
    conn, addr = server.accept()
    # print("[STARTING] server is starting...")
    # print(f"[NEW CONNECTION] {addr} connected.")

    message = conn.recv(1024).decode(FORMAT)
    conn.close()
    return str(message)

def main():
    automate = IOT()
    # automate.sangeet()
    # automate.samaye()
    # automate.mausam()


if __name__ == "__main__":
    automate = IOT()
    start_server()
    tasks = {
        "0": automate.samaye,
        "1": automate.sangeet,
        "2": automate.mausam,
        "3": automate.batti,
        "4": automate.pankha,
        "5": player.next,
        "6": player.previous
    }

    while True:
        # prediction = input("Enter prediction: ")
        prediction = receive()
        print("Action: ",SENTENCES[int(prediction)])
        # print(type(prediction))
        # break
        try:
            tasks[prediction]()
        except Exception as ex:
            print("Please Enter valid prediction key or check your internet connection")
            print("Error: ", ex)
