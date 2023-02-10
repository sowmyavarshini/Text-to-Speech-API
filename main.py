import requests
import fitz
from tkinter import *
from tkinter import filedialog
pdf_path = None
API_KEY = "YOUR-API-KEY"


def choose_file():
    global pdf_path
    pdf_path = filedialog.askopenfilename()
    file_entry.insert(0, pdf_path)


def convert():
    global pdf_path
    if pdf_path.endswith('.pdf'):
        doc = fitz.open(pdf_path)
        text = ''
        for page in doc:
            text += page.get_text()

        url = "https://cloudlabs-text-to-speech.p.rapidapi.com/synthesize"

        payload = f"voice_code=en-US-1&text={text}&speed=1.00&pitch=1.00&output_type=audio_url"
        headers = {
            "content-type": "application/x-www-form-urlencoded",
            "X-RapidAPI-Key": API_KEY,
            "X-RapidAPI-Host": "cloudlabs-text-to-speech.p.rapidapi.com"
        }

        response = requests.request("POST", url, data=payload, headers=headers)

        result = response.json()
        url = result['result']['audio_url']
        audio = requests.get(url)
        with open("output.mp3", "wb") as out:
            out.write(audio.content)
            print('Audio content written to file "output.mp3"')
    else:
        result_label.config(text='Please choose a PDF file.')


window = Tk()
window.title('Text-to-Audio')
window.minsize(width=450, height=300)
window.config(padx=20, pady=20)

title_label = Label(text='Text to Audio Converter', font=('Arial', 15, 'bold'))
title_label.place(x=50, y=0)
title_label.config(padx=20, pady=10)

pdf_label = Label(text='Choose a PDF file:', font=('Arial', 12))
pdf_label.place(x=10, y=60)
pdf_label.config(padx=10, pady=10)

file_entry = Entry(width=40)
file_entry.place(x=10, y=100)

file_button = Button(text='Choose file', command=choose_file)
file_button.place(x=290, y=95)

convert_button = Button(text='Convert', command=convert)
convert_button.place(x=160, y=160)

result_label = Label(text='', font=('Arial', 12, 'bold'))
result_label.place(x=120, y=210)

window.mainloop()
