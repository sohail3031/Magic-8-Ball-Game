from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.config import Config
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton
from kivy.uix.popup import Popup
from kivymd.uix.list import TwoLineListItem

import random
import pyttsx3 as pt
import threading
import speech_recognition as sr


class MagicBallWindow(MDBoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.engine = pt.init()
        self.ids.select_voice.values = ["FEMALE", "MALE"]
        self.recognizer = sr.Recognizer()
        self.questions, self.answers = [], []
        self.infinite_thread = False
        self.word = ["what can you do for me?", "what is your work?", "how can you help me."]
        self.word_response = ["You can ask me any question.", "I can predict your future.",
                              "I can tell about your fortune. On bases of your questions"]
        self.created = ["who created you?", "who is your creator?", "who is your owner?", "who is your master?"]
        self.created_responses = ["MOHAMMED SOHAIL AHMED created me.", "MOHAMMED SOHAIL AHMED is my creator.",
                                  "MOHAMMED SOHAIL AHMED is my master.", "MOHAMMED SOHAIL AHMED is my owner."]
        self.name_responses = ["You can call me Alex.", "I'm Alex!"]
        self.names = ["what is your name", "what should I call you", "whats your name?", "who are you?"]
        self.responses = ["It is certain", "Reply hazy, try again", "Don’t count on it", "It is decidedly so",
                          "Ask again later", "My reply is no", "Without a doubt", "Better not tell you now",
                          "My sources say no", "Yes – definitely", "Cannot predict now", "Outlook not so good",
                          "You may rely on it", "Concentrate and ask again", "Very doubtful", "As I see it, yes",
                          "Most likely", "Outlook good", "Yes", "Signs point to yes"]

    def check_voice(self):
        if self.ids.select_voice.text == "FEMALE":
            self.voice_function(num=1)
        elif self.ids.select_voice.text == "MALE":
            self.voice_function(num=0)

    def recognizing_speech(self):
        """ This function is responsible for recognizing voice. """
        self.check_voice()
        self.speak_function(f"Welcome to Magic 8 Ball {self.ids.user_name.text}. I am Alex!")

        with sr.Microphone() as source:
            while True:
                if self.infinite_thread:
                    self.ids.speech_recognition_status.text = "Speech Recognition: ON\nSpeak Something"
                    self.recognizer.pause_threshold = 1
                    self.recognizer.adjust_for_ambient_noise(source, duration=0.2)
                    audio = self.recognizer.listen(source)
                    if self.infinite_thread:
                        self.check_voice()
                        try:
                            self.ids.speech_recognition_status.text = "Speech Recognition: ON\nRecognizing Please Wait"
                            text = self.recognizer.recognize_google(audio, language="en-in")
                            self.ids.ask_question.text = text
                            self.ask_question()
                        except Exception:
                            pass

    def control_speech_recognition(self):
        """ This function is responsible for speech voice input. """
        if self.ids.speech_recognition_button.text == "Start Speech Recognition":
            self.infinite_thread = True
            self.ids.speech_recognition_button.text = "Stop Speech Recognition"
            self.ids.speech_recognition_status.text = "Speech Recognition: ON"
            self.show_popup(title="Speech Recognition is activated", message="Now you can give voice input")
        else:
            self.infinite_thread = False
            self.ids.speech_recognition_button.text = "Start Speech Recognition"
            self.ids.speech_recognition_status.text = "Speech Recognition: OFF"
            self.show_popup(title="Speech Recognition is deactivated", message="Now you cannot give voice input")

    def voice_function(self, num=1):
        """ Function to change voice. User has option to select either male or female voice. """
        self.voices = self.engine.getProperty("voices")
        self.engine.setProperty("voice", self.voices[num].id)

    def speak_function(self, word):
        """ This function is responsible for speaking. """
        self.engine.say(word)
        self.engine.runAndWait()

    def change_first_screen(self):
        """ Function to change the home page to user name page. """
        self.ids.screen_manager.current = "second_screen"
        self.ids.user_name.focus = True

    def validate_user_name(self):
        """ Function to check the user name is valid or not. """
        if len(self.ids.user_name.text) > 0:
            self.ids.screen_manager.current = "third_screen"
            self.ids.welcome_user.text = f"Welcome {self.ids.user_name.text}"
            thread = threading.Thread(target=self.recognizing_speech)
            thread.daemon = True
            thread.start()
        else:
            self.show_popup(title="Invalid Input", message="Please Provide a valid user name")

    @staticmethod
    def show_popup(title, message):
        """ Function to display popup messages. """
        layout = MDGridLayout(cols=1, padding=10, spacing=10)
        popup_label = MDLabel(text=message, font_size=20, bold=True, pos_hint={"center_x": .5, "center_y": .5},
                              theme_text_color="Custom", text_color=[1, 1, 1, 1], halign="center")
        popup_button = MDRaisedButton(text="OK", size_hint=(1, None), height=50, bold=True, font_size=20,
                                      pos_hint={"center_x": .5, "center_y": .5}, md_bg_color=[.06, .47, .47, 1])
        layout.add_widget(popup_label)
        layout.add_widget(popup_button)
        popup = Popup(title=title, content=layout, size_hint=(None, None), size=(350, 350), auto_dismiss=False)
        popup.open()
        popup_button.bind(on_press=popup.dismiss)

    def ask_question(self):
        """ Main function. """
        self.check_voice()
        user_question = self.ids.ask_question.text.lower()
        answer = None

        if user_question in self.questions:
            position = self.questions.index(user_question)
            user_question = self.questions[position]
            answer = self.answers[position]
        elif ("quit" in user_question) or ("bye" in user_question) or ("see you later" in user_question):
            self.speak_function("Bye!")
            exit()
        elif (user_question in self.names) or ("name" in user_question) or (user_question in self.word):
            answer = random.choice(self.name_responses)
            self.speak_function(answer)
        elif (user_question in self.created) or ("owner" in user_question) or ("creator" in user_question):
            answer = random.choice(self.created_responses)
        elif ("work" in user_question) or ("help me" in user_question) or (user_question in self.word_response) or \
                ("my future" in user_question) or ("fortune" in user_question) or ("you do" in user_question):
            answer = random.choice(self.word_response)
        else:
            answer = random.choice(self.responses)

        self.questions.append(user_question)
        self.answers.append(answer)
        self.ids.comp_reply.text = f"Alex: {answer}"
        self.speak_function(answer)
        self.ids.chat_questions.add_widget(TwoLineListItem(text=f"You: {self.questions[-1]}",
                                                           secondary_text=f"Alex: {self.answers[-1]}",
                                                           theme_text_color="Custom", text_color=[1, 1, 1, 1],
                                                           secondary_theme_text_color="Custom",
                                                           secondary_text_color=[1, 1, 1, 1]))


class MagicBallApp(MDApp):
    def build(self):
        self.title = "Magic 8 Ball Game"
        self.icon = "images/magic_ball.jpg"
        Config.set('kivy', 'window_icon', 'images/magic_ball.jpg')
        return MagicBallWindow()


if __name__ == "__main__":
    MagicBallApp().run()
