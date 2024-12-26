from g4f.client import Client
from telebot import TeleBot, types


token = 'Ваш токен телеграмм бота.'
client = Client()
bot = TeleBot(token)

kb_text = types.ReplyKeyboardMarkup()

models_work = ['gpt-3.5-turbo', 'gpt-4o','gpt-4o-mini','gpt-4-turbo',
               'o1-mini','llama-3.1-70b','llama-3.2-11b','mistral-large',
               'gemini-pro','gemini-flash','claude-2.1','claude-3-haiku',
               'claude-3.5-sonnet','blackboxai','blackboxai-pro','llava-13b',
               'sonar-chat']

models_image_work = ['sdxl','sd-3','playground-v2.5','flux','flux-realism','flux-anime','flux-3d','flux-disney',
                     'flux-pixel','flux-4o','any-dark']


kb_images = types.ReplyKeyboardMarkup()
for model in models_image_work:
    kb_images.add(types.KeyboardButton(model))

for model in models_work:
    kb_text.add(types.KeyboardButton(model))


@bot.message_handler(commands=['start'])
def welcome_func(message):
    kb_mode = types.ReplyKeyboardMarkup()
    kb_mode.add(types.KeyboardButton('text'),types.KeyboardButton('image'))
    bot.send_message(message.chat.id,'Привет! Выбери режим работы!', reply_markup=kb_mode)

@bot.message_handler(func=lambda message: message.text in ['text', 'image'])
def qw_function(message):
    if message.text == 'text':
        bot.send_message(message.chat.id,'Вы выбрали генерацию текста, выбери модель:', reply_markup=kb_text)
    else:
         bot.send_message(message.chat.id,'Вы выбрали генерацию картинок, выбери модель:', reply_markup=kb_images)

@bot.message_handler(func=lambda message: message.text in models_work)
def text_gen_function(message):
    model = message.text
    bot.send_message(message.chat.id,f'Вы выбрали модель {model}.')
    bot.send_message(message.chat.id,f'Введите запрос:')
    bot.register_next_step_handler(message, text_send, model)

@bot.message_handler(func=lambda message: message.text in models_image_work)
def imgage_gen_function(message):
    model = message.text
    bot.send_message(message.chat.id,f'Вы выбрали модель {model}.')
    bot.send_message(message.chat.id,f'Введите запрос:')
    bot.register_next_step_handler(message, img_send, model)


def img_send(message, model):
    user_response = message.text
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[{'role': 'user','content': user_response}]
        )
        answer=response.choices[0].message.content
        bot.send_message(message.chat.id, answer)
    except Exception as e:
        bot.send_message(message.chat.id,f'Ошибка генерации: {str(e)}')

def text_send(message, model):
    user_response = message.text
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[{'role': 'user','content': user_response}]
        )
        answer=response.choices[0].message.content
        bot.send_message(message.chat.id, answer)
    except Exception as e:
        bot.send_message(message.chat.id,f'Ошибка генерации: {str(e)}')


bot.infinity_polling(none_stop=True)