from playsound import playsound 
import speech_recognition as sr 
from googletrans import Translator 
from gtts import gTTS 
import os 
flag = 0

import os
import pdfplumber
import appdirs
from tkinter import *
import tkinter
from tkinter import ttk
from tkinter import messagebox
from tktooltip  import ToolTip
from tkinter import filedialog as fd
from tkinter import Toplevel
from os import path
from pydub import AudioSegment
from PIL import Image, ImageTk
import speech_recognition as sr
import pyttsx3 
import ffmpeg
from googletrans import Translator
from gtts import gTTS
import pyperclip
import subprocess
from fpdf import FPDF
global download_dir,file_dir,dest,src
# A tuple containing all the language and 
# codes of the language will be detcted 
dic = ('afrikaans', 'af', 'albanian', 'sq', 
    'amharic', 'am', 'arabic', 'ar', 
    'armenian', 'hy', 'azerbaijani', 'az', 
    'basque', 'eu', 'belarusian', 'be', 
    'bengali', 'bn', 'bosnian', 'bs', 'bulgarian', 
    'bg', 'catalan', 'ca', 'cebuano', 
    'ceb', 'chichewa', 'ny', 'chinese (simplified)', 
    'zh-cn', 'chinese (traditional)', 
    'zh-tw', 'corsican', 'co', 'croatian', 'hr', 
    'czech', 'cs', 'danish', 'da', 'dutch', 
    'nl', 'english', 'en', 'esperanto', 'eo', 
    'estonian', 'et', 'filipino', 'tl', 'finnish', 
    'fi', 'french', 'fr', 'frisian', 'fy', 'galician', 
    'gl', 'georgian', 'ka', 'german', 
    'de', 'greek', 'el', 'gujarati', 'gu', 
    'haitian creole', 'ht', 'hausa', 'ha', 
    'hawaiian', 'haw', 'hebrew', 'he', 'hindi', 
    'hi', 'hmong', 'hmn', 'hungarian', 
    'hu', 'icelandic', 'is', 'igbo', 'ig', 'indonesian', 
    'id', 'irish', 'ga', 'italian', 
    'it', 'japanese', 'ja', 'javanese', 'jw', 
    'kannada', 'kn', 'kazakh', 'kk', 'khmer', 
    'km', 'korean', 'ko', 'kurdish (kurmanji)', 
    'ku', 'kyrgyz', 'ky', 'lao', 'lo', 
    'latin', 'la', 'latvian', 'lv', 'lithuanian', 
    'lt', 'luxembourgish', 'lb', 
    'macedonian', 'mk', 'malagasy', 'mg', 'malay', 
    'ms', 'malayalam', 'ml', 'maltese', 
    'mt', 'maori', 'mi', 'marathi', 'mr', 'mongolian', 
    'mn', 'myanmar (burmese)', 'my', 
    'nepali', 'ne', 'norwegian', 'no', 'odia', 'or', 
    'pashto', 'ps', 'persian', 'fa', 
    'polish', 'pl', 'portuguese', 'pt', 'punjabi', 
    'pa', 'romanian', 'ro', 'russian', 
    'ru', 'samoan', 'sm', 'scots gaelic', 'gd', 
    'serbian', 'sr', 'sesotho', 'st', 
    'shona', 'sn', 'sindhi', 'sd', 'sinhala', 'si', 
    'slovak', 'sk', 'slovenian', 'sl', 
    'somali', 'so', 'spanish', 'es', 'sundanese', 
    'su', 'swahili', 'sw', 'swedish', 
    'sv', 'tajik', 'tg', 'tamil', 'ta', 'telugu', 
    'te', 'thai', 'th', 'turkish', 
    'tr', 'ukrainian', 'uk', 'urdu', 'ur', 'uyghur', 
    'ug', 'uzbek', 'uz', 
    'vietnamese', 'vi', 'welsh', 'cy', 'xhosa', 'xh', 
    'yiddish', 'yi', 'yoruba', 
    'yo', 'zulu', 'zu') 




home_dir = os.path.expanduser("~")   #to get the path of the images
if os.name == "nt":
    # Windows
    file_dir = os.path.join(home_dir, "Downloads")
    download_dir = os.path.join(home_dir, "Downloads/images")
elif os.name == "posix":
    # Linux or macOS
    file_dir = os.path.join(home_dir, "Downloads")
    download_dir = os.path.join(home_dir, "Downloads/images")
else:
    # Unknown operating system
    file_dir=None
    download_dir = None

file_name=''
filenamedest = "wav" 
source='English'
destination='English'
filetype='wav'
translator=Translator()
r = sr.Recognizer()
center = tkinter.Tk()

center.title("Audio Converter")
#bg = ImageTk.PhotoImage(file="c:/users/pranay/desktop/geometric-pattern-purple-technol.jpg")
#bg = ImageTk.PhotoImage(file=download_dir+"/"+"th.jpg")
bg = ImageTk.PhotoImage(file=download_dir+"/"+"sound.jpg")
# Create a canvas

canvas = tkinter.Canvas(center,width= 900, height= 500)
canvas.pack(fill= "both", expand=True)
# Display image
canvas.create_image(0, 0, image=bg, anchor="nw")
# Code to add widgets will go here...
# Creating a photoimage object to use image

#photoml = ImageTk.PhotoImage(file = download_dir+ "/" + "speaker_img.png")
photoml = ImageTk.PhotoImage(file = download_dir+ "/" + "sound.jpg")
masterlable=tkinter.Label(center,text="Speech To Text Converter",image=photoml,width=430,height=90)
#masterlable=tkinter.Label(center,text="Speech To Text Converter",width=20,height=5)
masterlable.place(x=100,y=50)

#for the uploading of the pdf file
photomic = ImageTk.PhotoImage(file = download_dir+ "/" + "mic.png")
bphotomic=tkinter.Button(center, text ='Audio Converter',image=photomic,width=60,height=60,command = lambda:microphone_capture())
bphotomic.place(x=680,y=80)
ToolTip(bphotomic,msg='Audio Translator')



#photo = ImageTk.PhotoImage(file = download_dir+ "/" + "uploadnew.png")
photo = ImageTk.PhotoImage(file = download_dir+ "/" + "general-upload-file.png")
bUpload = tkinter.Button(center, text ='Upload File',image=photo,width=60,height=60,command = lambda:upload_file())  #uploading button
bUpload.place(x=560,y=160)
ToolTip(bUpload,msg='Select the file')
fileLabel=tkinter.Label(center,text="")

#for the uploading of the pdf file
photou = ImageTk.PhotoImage(file = download_dir+ "/" + "pdf.png")
bFileTextUpload=tkinter.Button(center, text ='Upload File',image=photou,width=60,height=60,command = lambda:convert_file())
bFileTextUpload.place(x=680,y=160)
ToolTip(bFileTextUpload,msg='PDF To Text Converter')

#photon = ImageTk.PhotoImage(file = download_dir+ "/" + "Notepad.png")
photon = ImageTk.PhotoImage(file = download_dir+ "/" + "pdf2.png")
bViewTextFile=tkinter.Button(center,text='View the File',image=photon,width=60,height=60,command=lambda:view_file())
bViewTextFile.place(x=800,y=160)
ToolTip(bViewTextFile,msg='Pdf File Viewer')
#fileLabel.place(x=560,y=450)

# def selectionfrom():
#    for i in fromlist.curselection():
#     print(fromlist.get(i))
      
# def selectionto():
#    for i in tolist.curselection():
#       print(tolist.get(i))

#photol = ImageTk.PhotoImage(file = "language.jpg")
fromLabel_sl=tkinter.Label(center,text="  Source Language     ")
fromLabel_sl.configure(bg='steel blue')
fromLabel_sl.place(x=560,y=260)
# combo_sl = ttk.Combobox(values=['English', 'Chinese', 'Spanish','Japanese'])
# combo_sl.configure(width=16, height=200)
# combo_sl.set("English")
# combo_sl.place(x=559,y=280)
radio = IntVar()
r1 = Radiobutton(center, text=" English                ", variable=radio, value=1,command=lambda:sourcelanguageselection())
r1.configure(bg="steel blue")
r1.place(x=560,y=280)

r2 = Radiobutton(center, text="Chinese                ", variable=radio, value=2,command=lambda:sourcelanguageselection())
r2.configure(bg="steel blue")
r2.place(x=560,y=300)

r3 = Radiobutton(center, text=" Spanish               ", variable=radio, value=3,command=lambda:sourcelanguageselection())
r3.configure(bg="steel blue")
r3.place(x=560,y=320)
r4 = Radiobutton(center, text="Japanese              ", variable=radio, value=4,command=lambda:sourcelanguageselection())
r4.configure(bg="steel blue")
r4.place(x=560,y=340)

fromLabel_dl=tkinter.Label(center,text="Destination Language")
fromLabel_dl.configure(bg='steel blue')
fromLabel_dl.place(x=700,y=260)
# combo_dl = ttk.Combobox(values=['English', 'Chinese', 'Spanish','Japanese'],postcommand=lambda:languageselection())
# combo_dl.configure(width=17, height=200)
# combo_dl.set("English")
# combo_dl.place(x=699,y=280)
CheckVar1 = IntVar()
CheckVar2 = IntVar()
CheckVar3 = IntVar()
CheckVar4 = IntVar()
C1 = Checkbutton(center, text = "English", variable = CheckVar1, 
                 onvalue = 1, offvalue = 0, height=1, width = 13,command=lambda:languageselection1())
C1.configure(bg='steel blue')
C2 = Checkbutton(center, text = "Chinese", variable = CheckVar2, 
                 onvalue = 1, offvalue = 0, height=1, width = 13,command=lambda:languageselection2())
C2.configure(bg='steel blue')
C3 = Checkbutton(center, text = "Spanish", variable = CheckVar3, 
                 onvalue = 1, offvalue = 0, height=1, width = 13,command=lambda:languageselection3())
C3.configure(bg='steel blue')
C4 = Checkbutton(center, text = "Japanese", variable = CheckVar4, 
                 onvalue = 1, offvalue = 0, height=1, width = 13,command=lambda:languageselection4())
C4.configure(bg='steel blue')
C1.place(x=700,y=280)
C2.place(x=700,y=300)
C3.place(x=700,y=320)
C4.place(x=700,y=340)
v=tkinter.Scrollbar(center, orient='vertical')
v.pack(side=tkinter.RIGHT, fill='y')

#outputLabel=tkinter.Label(center,text="Result")
#outputLabel.place(x=100,y=100)

Output =tkinter.Text(center, height = 12,width = 53,bg = "light cyan",yscrollcommand=v.set)
Output.place(x=100,y=160)
v.config(command=Output.yview)
photoC = ImageTk.PhotoImage(file =download_dir+ "/" + "play-button2.png")
bConvert = tkinter.Button(center, text ="Convert",state = "normal",image=photoC, width=60,height=60,command = lambda:convert())  #uploading button
bConvert.place(x=270,y=380)
ToolTip(bConvert,msg='Play')

photoCopy = ImageTk.PhotoImage(file = download_dir+ "/"+ "copy2.png")
bCopy = tkinter.Button(center, text ="Copy To Clipboard",state = "normal",image=photoCopy, width=60,height=60,command = lambda:copytoclipboard())  #uploading button
bCopy.place(x=340,y=380)
ToolTip(bCopy,msg='Copy the Text')

#photoEx = ImageTk.PhotoImage(file = "fileextensions.jpg")
#fromExtension=tkinter.Button(center,text='Source file Extension',state = "disabled" ,image=photoEx , command = lambda:fileextensionblock())

#fromExtension=tkinter.Label(center,text='Source file Extension')
#fromExtension.configure(bg='steel blue')
#fromExtension.place(x=700,y=160)
#combo = ttk.Combobox(values=["wav", "mp3", "OGG"],postcommand=lambda:fileextensionblock())

# combo = ttk.Combobox(values=["wav", "mp3", "OGG"])
# combo.configure(width=16, height=200)
# combo.set("wav")
# combo.place(x=699, y=180)

#inputtxt = tkinter.Text(center,height = 1,width = 14)
#inputtxt.configure(bg='steel blue')
#inputtxt.place(x=700,y=180)
  


center.configure(bg="deep sky blue")
center.geometry("900x500")

def convert():
   filenamesource=""
   if fileextensionblock()==True :
     global filenamedest 
     global source,destination   
     sourcelanguageselection()
     if str(filetype)=='.mp3':
          filenamesource=fileLabel.cget("text")
          filenamedest=filenamesource.replace("mp3","wav")
          print(filenamedest)
          input_file = ffmpeg.input(filenamesource)
          audio = input_file.audio
          output_file=filenamedest
          output_audio = ffmpeg.output(audio, output_file)
          ffmpeg.run(output_audio)
          output_segment = AudioSegment.from_file(output_file)
          output_segment.export(filenamedest, format="wav")
         # sound.export(filenamedest, format="wav")
     if str(filetype)=='.ogg':
          filenamesource=fileLabel.cget("text")
          filenamedest=filenamesource.replace("ogg","wav")
          print(filenamedest)
          print(filenamesource)
          input_file = ffmpeg.input(filenamesource)
          audio = input_file.audio
          output_file=filenamedest
          output_audio = ffmpeg.output(audio, output_file)
          ffmpeg.run(output_audio)
          output_segment = AudioSegment.from_file(output_file)
          #sound = AudioSegment.from_mp3(filenamesource)
          sound = AudioSegment.from_ogg(filenamesource)
          output_segment.export(filenamedest, format="wav")
          #output_segment.export(filenamedest, format="wav")
          #sound = AudioSegment.from_ogg(filenamesource)
          #sound.export(filenamedest, format="wav")
     if str(filetype)=='.wav':
          filenamedest=fileLabel.cget("text")
     if source=='English':
          src='en'
     
     if source=='Chinese':
          src='zh-CN'
     
     if source=='Spanish':
          src='es'
     
     if source=='Japanese':
          src='ja'
     
     # for i in tolist.curselection():
     #    destination=tolist.get(i)
     print(source)
          
     if str(destination)=='English':
          dest='en'
     
     if str(destination)=='Chinese':
          dest='zh-CN'
     
     if str(destination)=='Spanish':
          dest='es'
     
     if str(destination)=='Japanese':
          dest='ja'
     print(destination)  
     
     with sr.AudioFile(filenamedest) as source:
          audio_text = r.listen(source)
     
     # recoginize_() method will throw a request error if the API is unreachable, hence using exception handling
     
          # using google speech recognition
          text = r.recognize_google(audio_text,language=str(src))
          resultStr = ""
          print('Converting audio transcripts into text ...')
          for character in text:
           if character.isalnum():
               resultStr = resultStr + character
          text=text.encode("UTF-8")
          print(text)
          trans1=translator.translate(resultStr,dest=str(dest))
          #trans1=translator.translate(text,dest=str(dest))
          print(trans1)
          Output.delete('1.0','end-1c')
          Output.update()
          Output.insert('end',str(trans1.text))
          f =fd.asksaveasfile(initialfile = 'Translated.txt',
          defaultextension=".txt",filetypes=[("Text Documents","*.txt")])     
          if f is None: # asksaveasfile return `None` if dialog closed with "cancel".
               print("No Save File Location selected")
          else :
               text2save = str(trans1.text) # starts from `1.0`, not `0.0`
               f.write(text2save)
               f.close()


          print("Performing Audio Translation..........")
          #text_to_translate = translator.translate(query, dest=to_lang)
          #text = text_to_translate.text

          # Using Google-Text-to-Speech ie, gTTS() method
          # to speak the translated text into the
          # destination language which is stored in to_lang.
          # Also, we have given 3rd argument as False because
          # by default it speaks very slowly
          speak = gTTS(text=trans1.text, lang=dest, slow=False)

          # Using save() method to save the translated
          # speech in capture_voice.mp3
          # filenamesource=fileLabel.cget("text")
          # filenamesource.replace(".mp3","_"+str(destination))
          # filenamesource.replace(".wav","_"+str(destination))
          # filenamesource.replace(".ogg","_"+str(destination))
          f =fd.asksaveasfile(initialfile = "translated"+"_"+str(destination)+".mp3",
          defaultextension=".mp3",filetypes=[("Audio Files","*.mp3")])     
          if f is None: # asksaveasfile return `None` if dialog closed with "cancel".
               print("No Save File Location selected")
          else :
               # text2save = str(trans1.text) # starts from `1.0`, not `0.0`
               # f.write(text2save)
               # f.close()
               #print(os.path.abspath(f.name))
               speak.save(os.path.abspath(f.name))
               print("Done...")


def convert_file():
     global filename
     print(file_dir) 
     global file_name
     file_name= fd.askopenfilename()
     translated_text=''
     tempTuple = os.path.splitext(file_name)
     filename=tempTuple[0]+".txt"
     #filename=tempTuple[0]+".pdf"
     print(filename)
     with open(filename, "w+") as file2:
      with pdfplumber.open(file_name) as pdf:
       totalpages = len(pdf.pages)
       for i in range(0,totalpages):
        first_page = pdf.pages[i]
        result = translator.translate(first_page.extract_text(),src='es', dest='en')
        translated_text=result.text        
        file2.write(translated_text)
        file2.write("\n")
        print(result)
      file2.close()    
     

def view_file():
     #subprocess.Popen(['notepad.exe', filename],shell=True)
     pdf = FPDF()

     # Add a page
     pdf.add_page()

     # set style and size of font
     # that you want in the pdf
     pdf.set_font("Arial", size = 10)

     # open the text file in read mode
     f = open(filename, "r")

     # insert the texts in pdf
     for x in f:
          pdf.cell(180, 10, txt = x, ln = 1, align = 'L')

     # save the pdf with name .pdf
     filenamenew=filename.replace(".txt","_")
     pdf.output(filenamenew+"translated.pdf")
     
     
     
     subprocess.Popen([filenamenew+"translated.pdf"],shell=True)
     #subprocess.Popen([filename],shell=True)
def copytoclipboard():
     pyperclip.copy(Output.get("1.0","end-1c"))
     spam = pyperclip.paste()



def upload_file():
    global file_name
    file_name= fd.askopenfilename(initialdir="C:\\audiofiles",title= "Please select a file:") 
    #file_name.lower().endswith(('.wav', '.mp3', '.ogg'))
    
    print(file_name)
    
    fileLabel.config(text =file_name )
    #fromExtension['state']="normal"




def fileextensionblock():
     global filetype
     ext = os.path.splitext(file_name)[-1].lower()
     filetype=ext
     print(ext) 
     
     #filetype=inputtxt.get(1.0, "end-1c")
     if (filetype!=".wav" and filetype!=".mp3" and filetype!='.ogg') :
         tkinter.messagebox.showerror('Auto Translater','Error:Wrong Extension')
         return False         
     print(filetype)
     return True

def sourcelanguageselection():
     global source
     if radio.get()==1:
        source="English"
     if radio.get()==2:
        source="Chinese"
     if radio.get()==3:
        source="Spanish"
     if radio.get()==4:
        source="Japanese"


def languageselection1():
   #fileextensionblock()
   global source,destination
  # source =combo_sl.get()   
  # source=str(radio.get())
   if CheckVar1.get()==1:
     destination="English"
     CheckVar2.set(0)
     CheckVar3.set(0)
     CheckVar4.set(0) 
   #bConvert['state']='normal'

def languageselection2():
   #fileextensionblock()
   global source,destination
  # source =combo_sl.get()  
   if CheckVar2.get()==1:
     destination='Chinese'
     CheckVar1.set(0)
     CheckVar3.set(0)
     CheckVar4.set(0)

def languageselection3():
    #fileextensionblock()
    global source,destination
    # source =combo_sl.get()   
    #source=str(radio.get())
    if CheckVar3.get()==1:
          destination='Spanish'
          CheckVar1.set(0)
          CheckVar2.set(0)
          CheckVar4.set(0)

def languageselection4():
   #fileextensionblock()
   global source,destination
  # source =combo_sl.get()   
   #source=str(radio.get())
   if CheckVar4.get()==1:
     destination='Japanese'
     CheckVar1.set(0)
     CheckVar2.set(0)
     CheckVar3.set(0) 


# Code Block for microphone capture and sentence translation 
# Capture Voice   
# takes command through microphone 
def takecommand(): 
    print('in')
    r = sr.Recognizer() 
    with sr.Microphone() as sound: 
        print("listening.....") 
        r.pause_threshold = 1
        audio = r.listen(sound) 

    try: 
        print("Recognizing.....") 
        if source=='English':
          src='en'
     
        if source=='Chinese':
            src='zh-CN'
        
        if source=='Spanish':
            src='es'
        
        if source=='Japanese':
            src='ja'
        
        print(src)

        query = r.recognize_google(audio, language=src) 
        print(f"The User said {query}\n") 
    except Exception as e: 
        print("say that again please.....") 
        return "None"
    return query 

def takecommand_change(): 
    print('in')
    r = sr.Recognizer() 
    with sr.Microphone() as source: 
        print("listening.....") 
        r.pause_threshold = 1
        audio = r.listen(source) 

    try: 
        print("Recognizing.....") 
        # query = r.recognize_google(audio, language=to_lang_source) 
        if source=='English':
          src='en'
     
        if source=='Chinese':
            src='zh-CN'
        
        if source=='Spanish':
            src='es'
        
        if source=='Japanese':
            src='ja'
        
        # for i in tolist.curselection():
        #    destination=tolist.get(i)
        print(src)
            
        
        
        
        query = r.recognize_google(audio, language=src) 
        print(f"The User said {query}\n") 
    except Exception as e: 
        print("say that again please.....") 
        return "None"
    return query 




def destination_language(): 
    print("Enter the language in which you want to convert : Ex. Spanish , English , etc.") 
    print() 
    
    # Input destination language in 
    # which the user wants to translate 
    to_lang = takecommand() 
    while (to_lang == "None"): 
        to_lang = takecommand() 
    to_lang = to_lang.lower() 
    return to_lang 

def source_language(): 
    print("Enter the language in which you will speak : Ex. Spanish , English , etc.") 
    print() 
    
    # Input source language in 
    # which the user wants to speak 
    to_lang = takecommand() 
    while (to_lang == "None"): 
        to_lang = takecommand() 
    to_lang = to_lang.lower() 
    return to_lang 

def microphone_capture():
     
     # to_lang_source = source_language()
     # # Mapping it with the code 
     # while (to_lang_source not in dic): 
     #      print("Language in which you are trying to speak is currently not available ,please input some other language") 
     #      print() 
     #      to_lang_source = source_language() 

     # to_lang_source = dic[dic.index(to_lang_source)+1] 
     # print("Input language name:")
     # print(to_lang_source)


     # to_lang = destination_language() 

     # # Mapping it with the code 
     # while (to_lang not in dic): 
     #      print("Language in which you are trying to convert is currently not available ,\ please input some other language") 
     #      print() 
     #      to_lang = destination_language() 

     # to_lang = dic[dic.index(to_lang)+1] 
     # print(to_lang)


     # Input from user 
     # Make input to lowercase Take Source language name from this block
     print("Speak Now")
     query = takecommand() 
     while (query == "None"): 
          query = takecommand() 




     # invoking Translator 
     translator = Translator() 


     # Translating from src to dest 
     # text_to_translate = translator.translate(query, dest=to_lang) 
     if str(destination)=='English':
            dest='en'
        
     if str(destination)=='Chinese':
        dest='zh-CN'
    
     if str(destination)=='Spanish':
        dest='es'
    
     if str(destination)=='Japanese':
        dest='ja'
     print(dest)  
        
     
     text_to_translate = translator.translate(query, dest) 
     text = text_to_translate.text 

     # Using Google-Text-to-Speech ie, gTTS() method 
     # to speak the translated text into the 
     # destination language which is stored in to_lang. 
     # Also, we have given 3rd argument as False because 
     # by default it speaks very slowly 
     # speak = gTTS(text=text, lang=to_lang, slow=False) 
     speak = gTTS(text=text, lang=dest, slow=False) 
     # Using save() method to save the translated 
     # speech in capture_voice.mp3 
     speak.save("captured_voice.mp3") 
     #threading.thread.sl
     # Using OS module to run the translated voice. 
     #audio_file = os.path.dirname(__file__) + '\captured_voice.mp3'

     cwd = os.getcwd()
     print(cwd)
     audio_file=cwd+'\captured_voice.mp3'
     print(audio_file)
     playsound(audio_file) 
     #os.remove('captured_voice.mp3') 

     # Printing Output 
     print(text) 
     Output.delete('1.0','end-1c')
     Output.update()
     Output.insert('end',str(text))


center.mainloop()


