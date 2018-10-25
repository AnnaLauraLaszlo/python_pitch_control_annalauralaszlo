import webbrowser
import pyautogui


def open_website(website_url):
    webbrowser.open(website_url, new=1)


def press_key(text):
    pyautogui.press(text)


def keep_pressing_key(text):
    pyautogui.keyDown(text)


def release_key(text):
    pyautogui.keyUp(text)