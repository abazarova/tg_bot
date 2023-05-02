from aiogram.utils.markdown import link

WELCOME = '''
*Hello!* This bot is created to help you learn Chinese characters. \n
List of available commands: \n
/random\_character - print random character with pinyin and translation to English \n
/add\_character - add character with translation to the dictionary \n
/train\_pinyin\_mul - learn 5 random characters' pinyin (multiple choice) \n
/train\_translation\_mul - learn 5 random characters' translation (multiple choice)  \n
/train\_pinyin\_write - learn 5 random characters' pinyin (writing) \n
/train\_transl\_write - learn 5 random characters' translation (writing) \n
To find new characters that you want to learn, you can use the website {}
'''.format(link(title='trainchinese', url='https://www.trainchinese.com'))

GAME_OVER_WIN = '''
Game over! \n
_You win._
'''

GAME_OVER_LOSE = '''
Wrong! \n
_You lose._
'''

ENTER_THE_CHARACTER_TO_ADD = '''
Please, enter the character that you want to save, its' pinyin and translation. \n
_Example:_ 你 ni4 you
'''

WORD_ADDED = '''
Added {} to the dictionary
'''

ENTER_THE_CHARACTER_TO_TRANSLATE = '''
The character is {}. \n
Please, enter its' meaning. 
'''

ENTER_THE_CHARACTER_TO_PINYIN = '''
The character is {}. 
Please, enter its' pinyin. 
'''


