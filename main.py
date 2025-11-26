import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QTextEdit, QLineEdit, QPushButton
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile
import subprocess

class ChatBotUI(QMainWindow):
    def __init__(self):
        super().__init__()

        # Load the UI file
        loader = QUiLoader()
        ui_file = QFile("chatbot.ui")
        ui_file.open(QFile.ReadOnly)
        self.window = loader.load(ui_file, self)
        ui_file.close()

        # --- Correct way to find widgets using type + objectName ---
        self.chatDisplay = self.window.findChild(QTextEdit, "chatDisplay")
        self.inputField = self.window.findChild(QLineEdit, "inputField")
        self.sendButton = self.window.findChild(QPushButton, "sendButton")

        # --- Safety Check (to help spot issues faster next time) ---
        print("chatDisplay:", self.chatDisplay)
        print("inputField:", self.inputField)
        print("sendButton:", self.sendButton)

        # Connect send button + Enter key
        self.sendButton.clicked.connect(self.handle_send_message)
        self.inputField.returnPressed.connect(self.handle_send_message)

        self.window.show()
    # asking Ollama
    def ask_ollama(self, prompt, model="gemma3:1b"):
        try:
            ollama_path=r"C:\Users\OLASQUARE\AppData\Local\Programs\Ollama\ollama.exe"
            result = subprocess.run(
                [ollama_path, "run", model, prompt],
                capture_output=True
            )
            # Decode safely as UTF-8
            output = result.stdout.decode("utf-8", errors="replace")

            return output.strip()
        except Exception as e:
            return f"Error calling Ollama: {e}"
        
    
    def handle_send_message(self):
        user_text = self.inputField.text().strip()
        if user_text == "":
            return

        # USER MESSAGE BUBBLE (right aligned)
        user_bubble = f"""
        <table width="100%">
        <tr>
            <td></td>
            <td style="
                background-color:#3A8DFF;
                color:white;
                padding:10px;
                border-radius:10px;
                margin:10px;
                max-width:70%;
                width:auto;
            ">
                {user_text}
            </td>
        </tr>
        </table>
        """

        self.chatDisplay.append(user_bubble)
        self.inputField.clear()

        # BOT PLACEHOLDER RESPONSE
        bot_reply = self.ask_ollama(user_text)

        bot_bubble = f"""
        <table width="100%">
        <tr>
            <td style="
                background-color:#2d2d2d;
                color:#e8e8e8;
                padding:10px;
                border-radius:10px;
                margin:10px;
                max-width:70%;
                width:auto;
            ">
                {bot_reply}
            </td>
            <td></td>
        </tr>
        </table>
        """

        self.chatDisplay.append(bot_bubble)

        # Scroll to bottom
        sb = self.chatDisplay.verticalScrollBar()
        sb.setValue(sb.maximum())

    



if __name__ == "__main__":
    app = QApplication(sys.argv)
    chatbot = ChatBotUI()
    sys.exit(app.exec())