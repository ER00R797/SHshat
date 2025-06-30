
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
import requests, os

class GPTBox(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', **kwargs)
        self.input_text = TextInput(size_hint_y=None, height=100, multiline=True)
        self.send_button = Button(text="🚀 إرسال", size_hint_y=None, height=50)
        self.send_button.bind(on_press=self.send_to_gpt)
        self.output_label = Label(text="🤖 أهلاً بيك، ابدأ اكتب أي سؤال!", size_hint_y=None, height=300)
        self.output_scroll = ScrollView(size_hint=(1, 1))
        self.output_scroll.add_widget(self.output_label)

        self.add_widget(self.input_text)
        self.add_widget(self.send_button)
        self.add_widget(self.output_scroll)

    def send_to_gpt(self, instance):
        prompt = self.input_text.text.strip()
        if not prompt:
            self.output_label.text = "❌ من فضلك اكتب سؤال."
            return

        try:
            response = requests.post(
                "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.1",
                headers={"Authorization": f"Bearer {os.getenv('HF_TOKEN', 'your_token_here')}"},
                json={"inputs": prompt}
            )
            result = response.json()
            output_text = result[0]['generated_text'] if isinstance(result, list) else str(result)
        except Exception as e:
            output_text = f"⚠️ حدث خطأ: {str(e)}"

        self.output_label.text = f"📥 سؤالك:\n{prompt}\n\n📤 الرد:\n{output_text}"

class SHshatApp(App):
    def build(self):
        return GPTBox()

if __name__ == '__main__':
    SHshatApp().run()
