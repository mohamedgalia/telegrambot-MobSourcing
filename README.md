# MobSourcing Bot
<https://github.com/Elevationacademy/xt-brosh-bot-hackathon-mobsourcing/blob/gazal/README.md>

bot for recruitment people for doing events 

* Mohamed Galia
* Muhammad Abu madeghem
* Orwa Watad


## Screenshots

![1](https://user-images.githubusercontent.com/48689046/67978476-db4f3680-fc22-11e9-80e6-8d07295fbcad.png)
![SCREESHOT DECSRIPTION](screenshots/2.png)
![SCREESHOT DECSRIPTION](screenshots/3.png)
![SCREESHOT DECSRIPTION](screenshots/4.png)
![SCREESHOT DECSRIPTION](screenshots/5.png)
![SCREESHOT DECSRIPTION](screenshots/6.png)
![SCREESHOT DECSRIPTION](screenshots/7.png)
![SCREESHOT DECSRIPTION](screenshots/8.png)
![SCREESHOT DECSRIPTION](screenshots/9.png)
![SCREESHOT DECSRIPTION](screenshots/10.png)
![SCREESHOT DECSRIPTION](screenshots/11.png)

## How to Run This Bot
### Prerequisites
* Python 3.7
* pipenv
* MONGODB

### Setup
* Clone this repo from github
* Install dependencies: `pipenv install`
* Get a BOT ID from the [botfather](https://telegram.me/BotFather).
* Create a `secret_settings.py` file:

        BOT_TOKEN = '1049330787:AAGjZZetNTtBhdmCcCpWSW5b7vWGseXf5jM'

### Run
To run the bot use:

    pipenv run python bot.py

### Running tests
First make sure to install all dev dependencies:

    pipenv install --dev

To run all test  use:

    pipenv run pytest

(Or just `pytest` if running in a pipenv shell.)

## Credits and References
* [Telegram Docs](https://core.telegram.org/bots)
* [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot)
* [Mongo DB Docs](https://www.mongodb.com/cloud/atlas/lp/general/try?utm_source=google&utm_campaign=gs_emea_israel_search_brand_atlas_desktop&utm_term=mongodb%20docs&utm_medium=cpc_paid_search&utm_ad=e&_bt=335279733251&_bn=g&gclid=EAIaIQobChMIpMeKg-3D5QIVB9reCh32yglJEAAYASAAEgK37fD_BwE)
