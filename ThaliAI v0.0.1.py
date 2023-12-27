import openai
import speech_recognition as sr
import time
import elevenlabs
listener = sr.Recognizer()

elevenAPI = open('C:\\ElevenAPI.txt', 'r')
OpenAPI = open('C:\\OpenAPI.txt', 'r')
elevenlabs.set_api_key(elevenAPI.readline())

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

def generate_response(prompt):
    print("generating response...")
    threadID = "thread_CIMOum2xecJC630nFnvEMczS"
    client = openai.OpenAI(api_key = OpenAPI.readline())
    message = client.beta.threads.messages.create(
       thread_id = threadID,
       role = "user",
       content = prompt,
    )
    run = client.beta.threads.runs.create(
       thread_id = threadID,
       assistant_id = "asst_2aYchGnmsC3BOLunvPknErbE",
    )
    time.sleep(5)
    runStatus = client.beta.threads.runs.retrieve(
       thread_id = threadID,
       run_id = run.id,
    )
    if runStatus.status == "completed":
         messages = client.beta.threads.messages.list(
             thread_id = threadID,
            )
         for mesg in (messages.data):
             print(mesg.role + ": " + mesg.content[0].text.value)
             return (mesg.content[0].text.value)

def talk(text):
   audio = elevenlabs.generate(
      text = text,
      voice = "Dorothy"
   )
   elevenlabs.play(audio)

def main():
    while True:
        command = take_command()
        if 'thalia' in command:
          talk('how can I help you?')
          while True:
            command = take_command()
            if 'quit' in command:
               break
            else:
             response = generate_response(command)
             talk(response)
        elif 'quit' in command:
           break

if __name__ == "__main__":
   main()

