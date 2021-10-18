from gtts import gTTS
from playsound import playsound

if __name__ == '__main__':
    while 1:
        fileN_String=input("Nombre del archivo :")
        fileN=fileN_String+".mp3"

        fileT_String=input("Texto de la oración:")
        tts = gTTS(fileT_String, lang='es-us')

        with open(fileN, "wb") as file:
            tts.write_to_fp(file)

        print("Playing: "+fileN)
        playsound(fileN)
        print("\n")