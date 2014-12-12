ChameleonBot
=========

This CS 221 project creates a chatbot that can imitate a certain celebrity.
Currently it is set up to imitate Arnold Schwarzenegger at [chiploons.com](http://www.chiploons.com).


We added over 1200 lines to give the generic [Program-O](https://github.com/Program-O/Program-O) chatbot a personality, please see our [Github Contributions](https://github.com/markulrich/chambot/graphs/contributors) to see what changes we made. To run some of our data scraping files in isolation rather than setting up the entire Chambot PHP server, from the home directory you can run

```
cd genbot

python scrape_quotes.py albert_einstein
python scrape_quotes.py arnold_schwarzenegger
python scrape_quotes.py oprah_winfrey

python scrape_personality.py albert_einstein
python scrape_personality.py arnold_schwarzenegger
python scrape_personality.py oprah_winfrey
```

To run some of the learning experiments, from the home directory you can run

```
cd config

python learn.py
```
