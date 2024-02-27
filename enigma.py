class Rotor:
    def __init__(self, key):
        self.key = 0
        self.previous_key = 0
        self.alphabet = [' ', 'А', 'Б', 'В', 'Г', 'Д', 'Е', 'Ё', 'Ж', 'З', 'И',
                         'Й', 'К', 'Л', 'М', 'Н', 'О', 'П', 'Р', 'С', 'Т', 'У',
                         'Ф', 'Х', 'Ц', 'Ч', 'Ш', 'Щ', 'Ъ', 'Ы', 'Ь', 'Э', 'Ю', 'Я']
        self.code_alphabet = ['Ф', 'Я', 'Ц', 'Ы', 'Ч', 'У', 'В', 'С', 'К', 'А', 'М',
                              'Е', 'П', 'И', 'Н', 'Р', 'Т', 'Г', 'О', 'Ь', 'Ш', 'Л',
                              'Й', ' ', 'Б', 'Щ', 'Д', 'Ю', 'З', 'Ж', 'Х', 'Ъ', 'Э', 'Ё']
        self.set_key(key)

    def code(self, letter):
        letter = letter.upper()

        if letter in self.alphabet:
            letter = self.alphabet.index(letter)
            letter += self.key - self.previous_key
            if letter >= len(self.alphabet):
                letter -= len(self.alphabet)
            elif letter < 0:
                letter += len(self.alphabet)

            return self.code_alphabet[letter]
        else:
            raise ValueError

    def reverse_code(self, letter):
        letter = letter.upper()

        if letter in self.alphabet:
            letter = self.code_alphabet.index(letter)
            letter -= self.key - self.previous_key
            if letter < 0:
                letter += len(self.code_alphabet)
            elif letter >= len(self.alphabet):
                letter -= len(self.alphabet)

            return self.alphabet[letter]
        else:
            raise ValueError

    def set_key(self, key):
        if key == '':
            key = ' '
        self.key = self.alphabet.index(key.upper())


class Reflector:
    def __init__(self, rotor):
        self.rotor_key = rotor.key
        self.alphabet = [' ', 'А', 'Б', 'В', 'Г', 'Д', 'Е', 'Ё', 'Ж', 'З', 'И',
                         'Й', 'К', 'Л', 'М', 'Н', 'О', 'П', 'Р', 'С', 'Т', 'У',
                         'Ф', 'Х', 'Ц', 'Ч', 'Ш', 'Щ', 'Ъ', 'Ы', 'Ь', 'Э', 'Ю', 'Я']
        self.reverse_alphabet = ['Я', 'Ю', 'Э', 'Ь', 'Ы', 'Ъ', 'Щ', 'Ш', 'Ч', 'Ц', 'Х',
                                 'Ф', 'У', 'Т', 'С', 'Р', 'П', 'О', 'Н', 'М', 'Л', 'К',
                                 'Й', 'И', 'З', 'Ж', 'Ё', 'Е', 'Д', 'Г', 'В', 'Б', 'А', ' ']

    def code(self, letter):
        letter = letter.upper()
        letter = self.alphabet.index(letter)
        letter -= self.rotor_key

        if letter < 0:
            letter += len(self.alphabet)
        elif letter >= len(self.alphabet):
            letter -= len(self.alphabet)

        letter = self.alphabet.index(self.reverse_alphabet[letter])
        letter += self.rotor_key

        if letter >= len(self.alphabet):
            letter -= len(self.alphabet)
        elif letter < 0:
            letter += len(self.alphabet)

        return self.alphabet[letter]


class Enigma:
    def __init__(self, key1, key2):
        if key1 == '':
            key1 = ' '
        elif key2 == '':
            key2 = ' '

        self.rotor1 = Rotor(key1)
        self.rotor2 = Rotor(key2)
        self.rotor2.previous_key = self.rotor1.key
        self.reflector = Reflector(self.rotor2)

    def update_keys(self):
        if self.rotor1.key + 1 >= len(self.rotor1.alphabet):
            if self.rotor2.key + 1 >= len(self.rotor1.alphabet):
                self.rotor2.key += 1 - len(self.rotor1.alphabet)
            else:
                self.rotor2.key += 1
        else:
            self.rotor1.key += 1

    def code(self, word):
        result = ""
        try:
            for letter in word:
                letter = self.rotor1.code(letter)
                letter = self.rotor2.code(letter)
                letter = self.reflector.code(letter)
                letter = self.rotor2.reverse_code(letter)
                letter = self.rotor1.reverse_code(letter)
                result += letter
                self.update_keys()
        finally:
            return result

    def set_keys(self, key1, key2):
        self.rotor1.set_key(key1)
        self.rotor2.set_key(key2)
        self.rotor2.previous_key = self.rotor1.key

