from PIL import Image, ImageGrab, ImageOps
from pyautogui import position as mPos
import pytesseract
from time import sleep
import translators as ts
import threading, queue

print("Put mouse at first position and press enter.")
input()
a = mPos()
print("Put mouse at secound position and press enter.")
input()
b = mPos()

roi = (a.x, a.y, b.x, b.y)

sleep(1)

last = ''
current = ''
done = 0
translated = 0

def translate(current):
    print('\n'+current)
    with open('log.txt', 'a') as w:
        w.write(current+'\n')
    try:
        t_text = ts.bing(current, to_language='en').replace('Carle', 'Kyaru')
        print(t_text)
        with open('log.txt', 'a') as w:
            w.write(t_text+'\n\n')
    except TypeError:
        pass
    except UnicodeError:
        pass
    except KeyError:
        pass

q = queue.Queue()

def t_worker():
    while True:
        t = q.get()
        if len(t) > 10:
            translate(t)
        q.task_done()

with open('log.txt', 'w') as w:
    w.write('Starting translation...\n')

threading.Thread(target=t_worker, daemon=True).start()

print('Translator is running.')

try:
    while True:
        im = ImageGrab.grab(bbox=(roi))
        last = current
        #print('Checking.')
        current = pytesseract.image_to_string(im, lang='jpn').replace('\n\n', ':')\
              .replace(' ', '')\
              .replace('\n', '')\
              .replace(':', '\n')\
              .replace('丿', '！')

        if current != '':
            if current == last and done == 1 and translated == 0:
                translated = 1
                #print('Queuing.')
                q.put(current.replace(' / ', '\n').replace('/', '！'))

            elif current == last and done == 0:
                #print('Text done.')
                done = 1
        
            elif current != last and done == 1 and translated == 1:
                #print('New text.')
                done = 0
                translated = 0
    
        sleep(0.1)
        
except KeyboardInterrupt:
    print('Stop detected.')
    q.join()
    print('Exiting.')
    exit()
