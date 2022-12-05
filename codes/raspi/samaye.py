from gtts import gTTS
from playsound import playsound
import datetime
import os

def get_time():

    # morning_template = "अहिले बिहानको बजेर मिनेट गएको छ"
    # afternoon_template = "अहिले दिउँसोको बजेर मिनेट गएको छ"
    # evening_template = "अहिले साँझको बजेर मिनेट गएको छ"
    # night_template = "अहिले रातको बजेर मिनेट गएको छ"

    time = datetime.datetime.now()

    current_time = time.strftime("%I:%M %p")
    hour_minute = current_time.split(" ")[0].split(":")
    meredian = current_time.split(" ")[-1]
    # print("Meredian: ",meredian)
    # print("Hour minutte",hour_minute)

    hour = int(hour_minute[0])
    minute = int(hour_minute[-1])
    quarter = None
    
    if meredian=="AM":
        if(hour<12 and hour>3):
            quarter = "बिहानको"
        else:
            quarter = "रातको"
    elif meredian=="PM":
        if(hour==12 or hour<5):
            quarter = "दिउँसोको"
        elif(hour>4 and hour<8):
            quarter = "साँझको"
        else:
            quarter = "रातको"

    samaye = "अहिले " + quarter + str(hour) + " बजेर " + str(minute) + "मिनेट गएको छ"

    return samaye


def main():
    samaye = get_time()
    speak = gTTS(text=samaye, lang="ne", slow= False) 
    file = "samaya.mp3"
    speak.save(file)
    playsound(file)
    os.remove(file)


if __name__ == "__main__":
    main()
