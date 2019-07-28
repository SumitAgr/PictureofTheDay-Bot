![Bot logo](https://i.imgur.com/V4WEJJN.jpg)

<h3 align="center">Picture of The Day Bot for Telegram</h3>

![Language](https://img.shields.io/badge/Python-3.7-blue.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)
[![CodeFactor](https://www.codefactor.io/repository/github/sumitagr/pictureoftheday-bot/badge)](https://www.codefactor.io/repository/github/sumitagr/pictureoftheday-bot)

---

<p align="center"> 🤖 A Telegram bot that retrieve's NASA renowned picture of the day service (APOD) with a single command!
    <br> 
</p>

## 📝 Table of Contents
+ [About](#about)
+ [Demo / Working](#demo)
+ [How it works](#working)
+ [Usage](#usage)
+ [Built Using](#built_using)
+ [Authors](#authors)
+ [License](#license)
+ [Acknowledgments](#acknowledgement)

## 🧐 About <a name = "about"></a>
A simple and convenient telegram bot that retrieves pictures from NASA's APOD Service after the user enters a simple command: '/picture'. It shows the title of the image, the photo and a simple description of the picture.

## 🎥 Demo / Working <a name = "demo"></a>
![Working](https://i.imgur.com/nVF8viS.gif)

## 💭 How it works <a name = "working"></a>

The bot uses Telegram's API to communicate with the user to send messages to them. After the user successfully authenticates i.e starts the bot by clicking on the start button on the bot, it is ready to send the current picture of the day. 

The user is provided with two GUI options, an on-screen button to easily get the image or an in-line suggestion as the user writes '/picture' in the message box. 

Once the bot receives this request, it uses NASA APOD's API to retrieve the data in JSON format. The information is then converted into a message that is sent to the user within 5 seconds using Telegram's API.

The entire bot is written in Python 3.7

## 🎈 Usage <a name = "usage"></a>

To use the bot, type:
```
/picture
```
You can either type the entire command - '/picture' or use the GUI interface instead.
The bot will then quickly reply the current picture of the day. 

Please note: The bot could be slow sometimes as it depends on NASA's API requests.

## ⛏️ Built Using <a name = "built_using"></a>
+ [Python-Telegram-Bot](https://python-telegram-bot.org/) - Unofficial Python wrapper for Telegram's API
+ Requests - Requests library for HTTP Requests
+ Logging - Logging library for debugging
+ Time / DateTime - Time libraries

## ✍️ Authors <a name = "authors"></a>
+ Sumit Agrawal

## 📗 License <a name = "license"></a>
This project is licensed under the MIT License - see the LICENSE file for more details.

## 🎉 Acknowledgements <a name = "acknowledgement"></a>
+ Thank you to Python-telegram-bot for providing the python wrapper!
