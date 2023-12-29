import openai
import speech_recognition as sr
import time
import elevenlabs
from elevenlabs import set_api_key
import os
from tkinter import *
from PIL import ImageTk, Image

listener = sr.Recognizer()
root = Tk()
root.title('ThaliAI')
root.iconbitmap('ThaliaExpressions\\ThaliAIIcon.ico')
my_img = ImageTk.PhotoImage(Image.open('ThaliaExpressions\\ThaliaNorm.png'))
my_label = Label(image=my_img)

happywords = ['happy','thrilled','excited','excitment']
sarcasticwords = ['sarcastic','sarcasm']

OpenAPI = ''
ElevenAPI = ''



def take_command():
    command = ''
    with sr.Microphone() as source:
        print('listening...')
        voices = listener.listen(source)
        try:
         command = listener.recognize_google(voices, language = 'en-IN')
         command = command.lower()
        except Exception as e:
            print(e)
    return command

def change_image(emo):
    global my_img
    global my_label

    my_label.grid_forget()
    my_img = ImageTk.PhotoImage(Image.open('ThaliaExpressions\\' + emo + '.png'))
    my_label = Label(image=my_img)
    my_label.grid(row=0,column=0,columnspan=3)
    root.update()

def talk(text):
    audio = elevenlabs.generate (
        text = text,
        voice = "Dorothy",
    )
    for word in happywords:
        if word in text:
            print('changing expression happy')
            change_image('ThaliaHappy')
        else:
            print('changing expression norm')
            change_image('ThaliaNorm')
    for word in sarcasticwords:
        if word in text:
            print('changing expression annoyed')
            change_image('ThaliaAnnoyed')
        else:
            print('changing expression norm')
            change_image('ThaliaNorm')
    elevenlabs.play(audio)

def generate_response(client, prompt, thread):
    print("generating response...")
    message = client.beta.threads.messages.create(
       thread_id = thread.id,
       role = "user",
       content = prompt,
    )
    run = client.beta.threads.runs.create(
       thread_id = thread.id,
       assistant_id = "asst_2aYchGnmsC3BOLunvPknErbE",
    )
    time.sleep(5)
    runStatus = client.beta.threads.runs.retrieve(
       thread_id = thread.id,
       run_id = run.id,
    )
    if runStatus.status == "completed":
         messages = client.beta.threads.messages.list(
             thread_id = thread.id,
            )
         for mesg in (messages.data):
             print(mesg.role + ": " + mesg.content[0].text.value)
             return (mesg.content[0].text.value)

def main():
        my_label.grid(row=0,column=0,columnspan=3)
        root.update()
        set_api_key(api_key=ElevenAPI)
        client = openai.OpenAI(api_key=OpenAPI)
        thread = client.beta.threads.create()
        while True:
            command = take_command()
            if 'thalia' in command:
                talk('how can I help you?')
                while True:
                    command = take_command()
                    if 'quit' in command:
                        response = generate_response( client, command, thread)
                        talk(response)
                        client.beta.threads.delete()
                        break
                    else:
                        response = generate_response(client, command, thread)
                        talk(response)
            elif 'quit' in command:
                break
 
if __name__ == "__main__":
   main()

