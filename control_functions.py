import webbrowser
import pyautogui


def open_website(website_url):
    webbrowser.open(website_url, new=1)


def press_key(text):
    pyautogui.press(text)