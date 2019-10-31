# MobSourcing Bot
<https://github.com/Elevationacademy/xt-brosh-bot-hackathon-mobsourcing/blob/gazal/README.md>

bot for recruitment people for doing events 

* Mohamed Galia
* Muhammad Abu madeghem
* Orwa Watad


## Screenshots

![2](https://user-images.githubusercontent.com/48689046/67978683-59134200-fc23-11e9-8370-1a4c89b20e0c.png)
![1](https://user-images.githubusercontent.com/48689046/67978685-59134200-fc23-11e9-8c42-942afd1cc456.png)
![3](https://user-images.githubusercontent.com/48689046/67978729-6b8d7b80-fc23-11e9-99f8-0ccda6da7526.png)
![4](https://user-images.githubusercontent.com/48689046/67978732-6cbea880-fc23-11e9-9819-28f4645cf5ac.png)
![5](https://user-images.githubusercontent.com/48689046/67978741-70eac600-fc23-11e9-9e4e-23a5b433699c.png)
![6](https://user-images.githubusercontent.com/48689046/67978743-72b48980-fc23-11e9-876b-fe73865f137b.png)
![7](https://user-images.githubusercontent.com/48689046/67978748-75af7a00-fc23-11e9-9b7a-2a8e976c698a.png)
![8](https://user-images.githubusercontent.com/48689046/67978753-77793d80-fc23-11e9-93c7-bd940a5a03ab.png)
![9](https://user-images.githubusercontent.com/48689046/67978756-78aa6a80-fc23-11e9-8c21-c06d60ad9ac4.png)
![10](https://user-images.githubusercontent.com/48689046/67978760-79430100-fc23-11e9-9648-f2e27f93d690.png)
![11](https://user-images.githubusercontent.com/48689046/67978762-7b0cc480-fc23-11e9-845d-6e53d7f65ee1.png)

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
