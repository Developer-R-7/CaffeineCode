# 🍵 CaffeineCode 
CaffeineCode is a Community website made using popular python web-development framework `django` ,
This website is enclosed with ✍️ Tech-Blogs , 🎮 Playground (solve problems and write code)  , ✨ Awesome projects showcase 
<br>

👀 Looking forward to developed this community, get register yourself through our website contact-us page 📞

<br>

# ➕ Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install required packages.

> ⚠️ **NOTE** : **Recommedded to download all packages in a virtual python environment and third-party pacakages are also thier**
<br>

```bash
pip install -r requirements.txt
```
<br>

# 🔭 Usage
<br>

## 🚀 Setuping project
Step 1 - 💄 Make database migrations
<br>

```bash
python manage.py makemigrations
```
Step 2 - 📝 Apply database migrations
<br>

```bash
python manage.py migrate
```

Step 3 - 🎉 Finally use this command to run-server on localhost
<br>

```bash
python manage.py runserver
```
<br>

## 🚀 Setuping Environment
Step 1 - ✨ Create a `.env` file
<br>
Step 2 - 🔎 Look for `.env.sample` file in codebase and follow the format
<br>
Step 3 - 📧 Sending mail requires `SMTP` settings So change `.env` file with your credentials  
<br>
Step 4 - 🔒 Django requires a `SECRET_KEY` (a string with randomized combinations of every characters) [Read More about Django secret key](https://docs.djangoproject.com/en/4.0/ref/settings/)
Step 5 - 🔌 Celery package for performing asynchronous task with django requires a broker ,This projects uses `REDIS` as a broker read more about redis installation and setup in my [repositories](https://github.com/Developer-R-7/Celery-Integration-Django)

<br>

# ⚙️ Technology Used
Front-end : `HTML` `Bootstrap` `Ajax` `CSS` `Jquery` `JavaScript`
<br>
Back-end : `Python` 

<br>

# 🧑‍💻 Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
<br>

**There are some cases, such as using this code for a business or something that is greater than a personal project,
that we may be less comfortable saying yes to use this django project. 
If in doubt, please don't hesitate to ask the repo owner.**

<br>

# 🔑 License
This repo is lincense in [MIT](https://github.com/Developer-R-7/CaffeineCode/blob/main/LICENSE)
