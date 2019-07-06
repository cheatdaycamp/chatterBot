import requests
import random
import http.cookies
import os


boto_dictionaries = {
                'swear': ['arse', 'ass', 'asshole', 'bastard', 'bitch', 'bollocks ', 'crap', 'cunt', 'dick', 'damn',
                        'frigger', 'fuck', 'goddamn', 'godsdamn', ' shit', 'horseshit', 'motherfucker', 'nigga',
                        'nigger', 'prick', 'shit', 'shit ass', 'shitass', 'slut', 'son of a bitch',
                        'son of a motherless goat', 'son of a whore', 'twat'],
                'greetings': ['Shalom', 'Hello', 'Howdy', 'Hey there', 'Ahoy', 'Shalom', 'Ala kefa', 'Long time no see',
                            'Well, look at you'],
                'greetings_old_user': ['Hello old user'],
                'greet_b':  ['! It is a pleasure to meet you my friend!',
                             "! Nice to meet you!",
                             '! YEAH!!! bring the questions baby!!'
                             ],
                'no_swear': ["Please, don't swear. I might be a robot but I am educated",
                            "Why do you swear, when you can bless?",
                            "If you swear, your mouth only becomes dirtier",
                            "That's not nice from you",
                            "I should have followed Eliza's advice"],
                'jokes':    ['joke', 'jokes', 'laugh', 'laughter', 'funny', 'joke?', 'jokes?', 'laugh?', 'funny?'],
                'jokes_intro': ['Alright, here you have a joke: ',
                                'Let me tell you a joke: ',
                                'I am robot, but I am also funny. Check this out: '],
                'random_answers': ['Yes', 'No', 'Definitely no', 'Maybe', 'Without any doubt.'],
                'bye':      ['Bye', 'Bye bye', 'Bye, bye, bye', 'Goodbye', 'Have a great day', 'Hasta la vista'],
                'weather': ['weather', 'today', 'umbrella', 'sunny', 'rainy', 'weather?', 'today?', 'umbrella?',
                            'sunny?', 'rainy?'],
                'general': ['I see', 'Tell me more', 'Interesting', 'Aha.', 'What else can you tell me?',
                            "It is always nice to know", "That is really smart from you.",
                            "Yeah, you are totally right!!!",]
                }


boto_feelings = {
                'afraid': ['fear', 'stress', 'scared'],
                'bored': ['bored', 'exhausted'],
                'confuse': ['blur', 'jumble', 'disorder', 'confusion', 'confused'],
                'crying': ['sad', 'sadness', 'depressed', 'tragic', 'tragedy'],
                'dancing': ['dance', 'dancing', 'joy', 'movement', 'cheerfull'],
                'dog': ['pet', 'cat', 'dog', 'animal', 'animals'],
                'excited': ['excitement'],
                'giggling': ['funny', 'joke', 'embarrassing'],
                'heartbroke': ['ex', 'gone', 'broke', 'broken'],
                'inlove': ['love', 'fiance', 'marriage', 'wife', 'husband'],
                'laughing': ['happy', 'happiness', 'joy'],
                'money': ['$', 'money', 'bills', 'account'],
                'no': ['no', 'negative', 'refuse'],
                'ok': ['ok', 'okay', 'sababa'],
                'takeoff': ['go', 'bye', 'leave', 'leaving'],
                'waiting': ['time', 'wait', 'waiting', ],
                }

boto_values = {
                'user_message': '',
                'count': 0,
                'user_name': '',
                'answer': '',
                'animation': '',
                'input_message': '',
                }

def getKeysByValues(dictOfElements, listOfValues):
    listOfKeys = list()
    listOfItems = dictOfElements.items()
    for item in listOfItems:
        if item[1] in listOfValues:
            listOfKeys.append(item[0])
    return  listOfKeys


def random_value(key):
    return random.choice(boto_dictionaries.get(key))


def boto_logic(user_message):
    boto_values['count'] += 1
    boto_values['input_message'] = (user_message.lower()).split()
    if any(word in boto_values['input_message'] for word in boto_dictionaries.get('swear')):
        swear()
    elif boto_values['user_name'] == "":
        unknown_user()
    elif any(word in boto_values['input_message'] for word in boto_dictionaries.get('jokes')):
        handle_joke()
    elif any(word in boto_values['input_message'] for word in boto_dictionaries.get('weather')):
        weather()
    elif any(word in boto_values['input_message'] for word in [x.lower() for x in boto_dictionaries.get('bye')]):
        handle_goodbye()
    elif "?" not in user_message:
        handle_sentence()
    elif '?' in user_message:
        handle_question()


def check_cookies():
    if 'localhost:7001' in os.environ:
        boto_values['cookie_string'] = os.environ.get('localhost:7001')
        boto_values['c'] = http.cookies.SimpleCookie()
        boto_values['c'].load(boto_values['cookie_string'])
        try:
            boto_values['user_name'] = boto_values['c']['user_name'].value

        except KeyError:
            boto_values['user_name'] = ""

def unknown_user():
    boto_values['user_name'] = boto_values['input_message'][-1].capitalize()
    boto_values['answer'] = random_value('greetings') + " " + boto_values['user_name'] + random_value('greet_b')
    boto_values['animation'] = 'excited'


def handle_joke():
    boto_values['answer'] = random_value('jokes_intro') + requests.get('https://geek-jokes.sameerkumar.website/api').text
    boto_values['animation'] = 'laughing'


def handle_goodbye():
    boto_values['answer'] = random_value('bye') + "! :)"
    boto_values['animation'] = 'takeoff'

def handle_sentence():
    boto_values['answer'] = random_value('general')
    boto_values['animation'] = get_proper_animation()

def get_proper_animation():
    list_intersections = []
    founds = []
    for item in boto_feelings:
        for k, v in boto_feelings.items():
            list_intersections.append([k, v])
    for word in boto_values['input_message']:
        for subitem in list_intersections:
            for a in subitem:
                if word in a and (a not in founds):
                    founds.append(subitem[0])
    founds = list(dict.fromkeys(founds))
    if founds == []:
        return random.choice(list(boto_feelings.keys()))
    return random.choice(list(founds))


def handle_question():
    boto_values['answer'] = random_value('random_answers')
    boto_values['animation'] = get_proper_animation()


def known_user():
    boto_values['answer'] = random_value('greetings_old_user')
    boto_values['animation'] = 'inlove'


def weather():
    my_weather = requests.get(
        'https://api.darksky.net/forecast/a9090af6f6307a2632ccb6a87416f16f/32.1093,34.8554?exclude=minutely,daily,hourly,flags,alerts')
    weather_data = my_weather.json()
    weather_summary = str(weather_data.get('currently').get('summary')).lower()
    weather_temp = str(int(round(weather_data.get('currently').get('temperature') - 32) / 1.8)) + "°C"
    weather_humidity = str(int(round(weather_data.get('currently').get('humidity') * 100))) + "%"
    boto_values['answer'] = "The weather is " + weather_summary + ". The temperature is " + weather_temp + ", and the humidity: " + weather_humidity
    boto_values['animation'] = 'giggling'


def swear():
    boto_values['answer'] = random_value('no_swear')
    boto_values['animation'] = 'confused'
    boto_values['count'] -= 1
