
# coding: utf-8

# In[ ]:


import pygame
import pyautogui

def select_alarm(result) :
    if result == 0:
        sound_alarm("short_alarm.mp3")

    elif result == 1 :
        pyautogui.click(1646, 546)

    else :
        pyautogui.click(1646, 546)


def sound_alarm(path) :
    pygame.mixer.init()
    pygame.mixer.music.load(path)
    pygame.mixer.music.play()
    

