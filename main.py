from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
class SpeechToTextApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical')

        text_canvas = TextInput(height=200, readonly=True)
        layout.add_widget(text_canvas)

        button_layout = BoxLayout(orientation='horizontal')

        button = Button(text="Start Conversion", on_press=self.start_conversion, background_color=(0, 0, 1, 1))
        button_layout.add_widget(button)

        save_button = Button(text="Save", on_press=self.save_text_as_file, background_color=(1, 1, 0, 1), disabled=True)
        button_layout.add_widget(save_button)

        layout.add_widget(button_layout)

        return layout

    def start_conversion(self, instance):
        self.button.disabled = True
        self.save_button.disabled = True
        self.speech_to_text_and_speak()
        self.button.disabled = False

    def save_text_as_file(self, instance):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
        if file_path:
            with open(file_path, "w") as file:
                file.write(self.save_text)
            print("Text saved as file:", file_path)

    def speech_to_text_and_speak(self):
        recognizer = sr.Recognizer()
        engine = pyttsx3.init()

        with sr.Microphone() as source:
            print("Speak something:")
            audio = recognizer.listen(source)

        try:
            recognized_text = recognizer.recognize_google(audio)
            print("Recognized Text: " + recognized_text)
            engine.say(recognized_text)
            engine.runAndWait()
            self.text_canvas.text = recognized_text
            self.save_button.disabled = False
            self.save_text = recognized_text
        except sr.UnknownValueError:
            print("Speech not recognized")
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))

if __name__ == '__main__':
    SpeechToTextApp().run()
