# -*- coding: utf-8 -*-


from textblob import TextBlob
import re
import pytesseract
from PIL import Image
import wikipedia
import moviepy.editor as mp
from selenium import webdriver
from time import sleep
import subprocess
import speech_recognition as sr
import language_tool_python
import chardet
from pathlib import Path
import shutil
import os
#import logging
import sys
sys.path.insert(0, "__pycache__")
import pytube
# \Python\Python39\lib\site-packages\pytube\cipher.py     line 293: name = "iha"
# fix bags in module pytube


#logging.basicConfig(level=logging.ERROR)
#logger = logging.getLogger("my-logger")
#logger.propagate = False

os.system("CLS")

def zapros(text):

    #lg = TextBlob(text)
    #language = lg.detect_language()
    #text = lg.correct()
    #text = str(text)
    #language = str(language)
    wikipedia.set_lang("uk")

    try:

        ny = wikipedia.page(text)
        wikitext = ny.content[:1000]
        wikimas = wikitext.split(".")
        wikimas = wikimas[:-1]
        wikitext2 = ""
        
        for x in wikimas:

            if not("==" in x):
                    
                if(len((x.strip())) > 3):
                   wikitext2 = wikitext2 + x + "."

            else:

                break
        
        wikitext2 = re.sub("\([^()]*\)", "", wikitext2)
        wikitext2 = re.sub("\([^()]*\)", "", wikitext2)
        wikitext2 = re.sub("\{[^\{\}]*\}", "", wikitext2)

        return wikitext2
    
    except Exception as e:

        options = webdriver.ChromeOptions()
        options.add_argument("headless")
        driver = webdriver.Chrome(r"__pycache__\chromedriver.exe", chrome_options = options)

        driver.get("https://www.google.com")
        driver.set_window_size(1920,1080)
        sleep(1)

        driver.find_element_by_xpath("/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input").send_keys(text)
        sleep(1)
        driver.find_element_by_xpath("/html/body/div[1]/div[3]/form/div[1]/div[1]/div[2]/div[2]/div[5]/center/input[1]").click()
        sleep(2)
        driver.find_element_by_css_selector(".LC20lb").click()

        find_text = driver.find_element_by_tag_name("body")
        otv = find_text.text

        otv = re.sub("\([^()]*\)", "", otv)
        otv = re.sub("\([^()]*\)", "", otv)
        otv = re.sub("\{[^\{\}]*\}", "", otv)
        otv = re.sub("\n", " ", otv)

        if len(otv) >= 1051:

            otv = otv[500:1500]

            wikitext2 = otv

        else:

            wikitext2 = otv

        driver.quit()

        return wikitext2


def photo_to_text(img_path):

    pytesseract.pytesseract.tesseract_cmd = r"images\Tesseract-OCR\tesseract.exe"

    img = Image.open(img_path)
    custom_config = r"--oem 3 --psm 13"
    text = pytesseract.image_to_string(img, lang = "rus+eng+ukr")

    return text.strip()


def video_to_mp(file_path):

    try:

        src = r"videos/audio_in_video.mp3"
        clip = mp.VideoFileClip(file_path).subclip(0,20)
        clip.audio.write_audiofile(src)
    
    except:

        pass

    return src


def download_youtube(link):

    filename = "youtube.mp4"
    DOWNLOAD_FOLDER = "videos"
    youtube = pytube.YouTube(link)
    video = youtube.streams.get_highest_resolution()
    video.download(DOWNLOAD_FOLDER, filename = filename)
    #title = youtube.title

    src = DOWNLOAD_FOLDER + "/" + filename

    return src


def record(lang = "ru", src_filename = ""):

    dest_filename = r"audio/audio.wav"

    #file_source = ""
    #file_destination = r"audio"

    #for file in Path(file_source).glob("1.wav"):

        #shutil.move(os.path.join(file_source,file),file_destination)

    process = subprocess.run([r"audio\ffmpeg-master-latest-win64-gpl\bin\ffmpeg", "-nostats", "-y", "-i", src_filename, dest_filename]) # здесь путь к скаченому ffmpeg

    if process.returncode != 0:

        raise Exception("Something went wrong")

    r = sr.Recognizer()

    with sr.AudioFile(dest_filename) as source:
        audio = r.listen(source)
        said = ""

        try:
            #различные языки
            if (lang == "en") :

                said = r.recognize_google(audio,language = "en_US")

            elif (lang == "ru") :

                said = r.recognize_google(audio, language = "ru-RU") 

            elif (lang == "uk") :

                said = r.recognize_google(audio, language = "uk-UA") 

            # print(said)
        except Exception as e:

            if (str(e) != ""):

                return "Не можу розпізнати текст у цьому голосовому 😢"

    return said.lower()


def output(path):

    text_en = record(lang = "en", src_filename=path)

    tool = language_tool_python.LanguageTool("ru-RU")

    text_ru = record(lang = "ru", src_filename = path)
    matches = tool.check(text_ru)

    tool2 = language_tool_python.LanguageTool("uk-UA")

    text_uk = record(lang = "uk", src_filename = path)
    matches2 = tool.check(text_uk)

    temp = False
    temp_ru = False
    temp_uk = False

    #print(text_en)
    #print(text_ru)
    #print(text_uk)

    for x in text_en.split():

        if re.compile(r"[a-zA-Z]").match(x):

            temp = True

    for x in text_ru.split():

        if re.compile(r"[a-zA-Z]").match(x):

            temp_ru = True

    for x in text_uk.split():

        if re.compile(r"[a-zA-Z]").match(x):

            temp_uk = True

    if temp == True and temp_ru == True and temp_uk == True:

        #print("Text from example: " + text_en)
        pass

    elif temp_ru == False or temp_uk == False:

        if len(matches) > len(matches2):

            return text_ru

        else:

            return text_uk

#print(output(r"audio\1.ogg")) # здесь путь к файлу указываем
#download_youtube("https://www.youtube.com/watch?v=5QRCKvcYewE&ab_channel=4ndre")