from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit
from enigma import Enigma


class MyWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.layout = QVBoxLayout()

        beg_str = 'ПРИВЕТ'
        beg_key1 = 'п'
        beg_key2 = 'В'
        self.enigma = Enigma(beg_key1, beg_key2)
        result = self.enigma.code(beg_str)

        self.label_result = QLabel(f'Результат: {result}')
        self.layout.addWidget(self.label_result)

        self.label_instruction = QLabel('Введите строку на РУССКОМ языке, затем первый ключ, затем 2-й ключ:')
        self.layout.addWidget(self.label_instruction)

        self.edit_line = QLineEdit(self)
        self.edit_line.setText(beg_str)
        self.layout.addWidget(self.edit_line)

        self.edit_key1 = QLineEdit(self)
        self.edit_key1.setMaxLength(1)
        self.edit_key1.setText(beg_key1)
        self.layout.addWidget(self.edit_key1)

        self.edit_key2 = QLineEdit(self)
        self.edit_key2.setMaxLength(1)
        self.edit_key2.setText(beg_key2)
        self.layout.addWidget(self.edit_key2)

        self.edit_line.textChanged.connect(self.update_result)
        self.edit_key1.textChanged.connect(self.update_result)
        self.edit_key2.textChanged.connect(self.update_result)

        self.setLayout(self.layout)
        self.setWindowTitle('EnigmaRU')

    def update_result(self):
        text = self.edit_line.text()
        key1 = self.edit_key1.text()
        key2 = self.edit_key2.text()

        try:
            self.enigma.set_keys(key1, key2)
        except ValueError:
            self.label_result.setText('')
            self.label_instruction.setText('Произошла ошибка, вы используете неверный язык или ввели числовой ключ')
            return 1

        result = self.enigma.code(text)
        if result != '':
            self.label_result.setText(result)
            self.label_instruction.setText('Успешно. Спасибо за использование')
        else:
            self.label_result.setText('')
            self.label_instruction.setText('Произошла ошибка, вы используете неверный язык или ввели числовой ключ')


if __name__ == '__main__':
    app = QApplication([])
    window = MyWidget()
    window.show()
    app.exec()
