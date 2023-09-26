import Constant
import sys
import os
import openai
from PyQt5.QtpCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QGroupBox,
    QTextEdit
)
 
openai.api_key = Constant.API_KEY
 
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
 
    def init_ui(self):
      #Create the widgets
      self.logo_label = QLabel()
      self.logo_pixmap = QPixmap('XYZ').scaled(150, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation)
      self.logo_label.setPixmap(self.logo_pixmap)
     
      self.input_label = QLabel('Ask a question: ')
      self.input_field = QLineEdit()
      self.input_field.setPlaceholderText('Type here... ')
      self.answer_label = QLabel('Answer: ')
      self.answer_field = QTextEdit()
      self.answer_field.setReadOnly(True)
      self.submit_button = QPushButton('Submit')
      self.submit_button.setStyleSheet(
            """
         QPushButton {
            background_color: #4CAF50;
            border: none;
            color: white;
            padding: 15px 32px;
            font-size: 18px;
            font-weight: bold;
            border-radius: 10px;
            }
        QPushButton:hover {
            background-color: #3e8e41
            }
            """
      )
      self.popular_questions_group = QGroupBox('Popular Consultant Questions')
      self.popular_questions_layout = QVBoxLayout()
      #[] could also be added using langchain as dropdown for a consultant, here done with empty space workaround
      self.popular_questions = ["What are 20 best-practices for Digital Strategy Development in the [INDUSTRY] industry?", "What are the 10 most crucial Data Management and Analytics best-practices in the [INDUSTRY] industry?", "What do companies have to consider for the new General Data Protection Regulation (GDPR)? Browse the internet and summarize the top 10 websites.", "Give me a top level summary of the following data: "]
      self.question_button = []
 
      #Create a layout
      layout = QVBoxLayout()
      layout.setContentsMargins(20, 20, 20, 20)
      layout.setSpacing(20)
      layout.setAlignment(Qt.AlignCenter)
 
      #Add Logo
      layout.addWidget(self.logo_label, alignment=Qt.AlignCenter)
 
      #Add Input Field and Submit Button
      input_layout = QHBoxLayout()
      input_layout.addWidget(self.input_label)
      input_layout.addWidget(self.input_field)
      input_layout.addWidget(self.submit_button)
      layout.addLayout(input_layout)
 
      #Add Answer Field
      layout.addWidget(self.answer_label)
      layout.addWidget(self.answer_field)
 
      #add the popular questions buttons
      for question in self.popular_questions:
        button = QPushButton(question)
        button.setStyleSheet(
            """
            QPushButton {
                background-color: #FFFFFF;
                border: 2px solid #00AEFF;
                colour: #00AEFF;
                padding: 10px 20px;
                font-size: 18px;
                font-weight: bold;
                border-radius: 5px;
                }
                QPushButton:hover {
                    background-color: #00AEFF;
                    color: #FFFFFF;
                    }"""
        )
        button.clicked.connect(lambda _, q=question: self.input_field.setText(q)) 
        self.popular_questions_layout.addWidget(button)
        self.question_button.append(button)
      self.popular_questions_group.setLayout(self.popular_questions_layout)
      layout.addWidget(self.popular_questions_group)
 
    #set the layout
      self.setLayout(layout)
 
    #Set the window properties
      self.setWindowTitle('KPMG Digitalization Consultant AI Bot')
      self.setGeometry(200, 200, 600, 600)
 
    #Connect the submit button to the function which queries the OpenAI API
      self.submit_button.clicked.connect(self.get_answer)
 
    def get_answer(self):
        question = self.input_field.text()
 
        completion = openai.ChatCompletion.create(
            model = "gpt-3.5-turbo-0301",
            messages = [{"role": "user", "content": "You are a digitalization consultant AI helpbot. Take a deep breath and work on this problem step by step. Answer the following questions in a concise way or with bullet points."},
                        {"role": "user", "content":f'{question}'}],
            max_tokens = 1024,
            n = 1,
            stop = None,
            temperature = 0.7
        )
 
        answer = completion.choices[0].message.content
 
        self.answer_field.setText(answer)
 
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())