---
layout: post
title: "Tolki’s LoL data tech stack - 2020"
categories: development
---

A year and a half ago, [my first blog post](https://medium.com/@gary.mialaret/pioneering-data-driven-esports-analysis-b57d5079abda)
was about the tech stack I had settled on for League of Legends data analysis. At that time, I had only re-started 
software development for about a month.

Since then, my libraries have gone through numerous reworks, and I have tried a lot of new tools and packages. 
As the [Valorant](https://playvalorant.com/) API is dawning on us and I will develop a complete stack for 
it as well, let’s see where I stand today!

# Programming

## Language choice
I decided to pick up [python](discord.py) for my data analyst position, despite having never worked with the language before. 
The language was getting more and more traction and its environment seemed very mature.

I don’t regret it a second, and I still think it was the right choice. 
The python language and tools really make it a breeze to develop, especially when working locally or 
creating quick scripts to answer the team’s questions.

But python makes it difficult to share your code with non-technical people, for 
example to allow them to launch a data analysis script by themselves. 
Installing python and recreating the right python environment can be a tall ask, and creating GUIs in python is also far 
from trivial.

This is why I have started learning [Javascript](https://en.wikipedia.org/wiki/JavaScript), 
as it is the de-facto language for front-end development nowadays.
Even if you are building a native application, chances are you are using Javascript with a  framework like Electron.
I aim to learn React to create private data visualisation websites for the teams I work for. 
This is a tall mountain to climb, but it is going to be a great learning experience!

## IDE
Regarding my IDEs, I am still sticking with Jetbrain’s products at the moment, and in particular PyCharm. 
I bought its pro version and the database management features are really great, 
as well as its python interactive console which is really great.

Unfortunately, I feel like PyCharm is starting to stagnate when it comes to the very latest development technologies, 
and I would like to learn using VS Code in the future. I always try to use open source tools as it simplifies collaboration,
and VS Code has been growing at a staggering pace. 
As Jetbrain’s Javascript IDE does not have a community version, I have started using VS Code for Javascript, 
and will work on moving my python workflow there too!

# Environment and deployment

## Python environment management
At the very beginning I used [conda](https://docs.conda.io/en/latest/) to handle environments. 
As it was poorly documented and way too big, I moved on pretty fast.

I first switched to using [venv](https://docs.python.org/3/library/venv.html), managed mostly by PyCharm. 
While fully featured, it is squarely separated from package managements that if left in pip’s hands,
 and sometimes it can get messy to properly see where you are installing your packages.
 Deployment was made with repeated pip freeze -r > requirements.txt, which is not painless.

With venv, I also needed [pyenv](https://github.com/pyenv/pyenv) for python version management, which is a great tool
… As long as you’re not on Windows.
It was not an issue as I was developing on Mac OS and deploying on an Amazon Linux 2 server at that time. 
But when I worked to make my scripts run on Windows, I easily lost about two days setting up my python environment.

Then, about a year ago I started using [pipenv](https://pipenv-fork.readthedocs.io/en/latest/basics.html),
which was my main solution until very recently. 
Pipenv handles both environment and package management, and is aimed at reproducing python environments identically.

Overall, pipenv was great, but working with private git repositories and development versions of packages was 
unfortunately very annoying.

## Docker
This is why I am now using [Docker](https://www.docker.com/) everywhere in my development process. 
My development environment as well as my production applications are now simply Docker images, 
which I can use on any host, with any os, without having to care about python versions or available compilers.

But this was far from painless. 

Using Docker on Windows for python development through Pycharm is still a relatively new option, 
and Docker itself has a pretty steep learning curve.
I plan to write a blog post about my Docker setup in the future,
as I haven’t found any good source regarding full python development in Docker. 
I would not recommend using Docker if you are just starting to develop in python.

Despite that, suffering through all this was definitely worth it, as I can now run the latest version of my parser on any server by simply typing:
```shell script
docker-compose pull && docker-compose run -d
```
The only things I need to do to enable that on a new server is to install Docker, 
register to my Docker repository, and create the right environment and docker-compose file. 
That’s definitely way easier and sustainable than installing a full python environment
and managing it through git.

I also plan on moving to Linux for my development OS pretty soon, 
as I ran into multiple Windows-specific issues recently with Docker. 
For example, I cannot install the WSL 2 Windows update because 
[it clashes with dependencies coming from games ](https://www.theverge.com/2020/6/1/21276653/microsoft-windows-10-may-2020-update-block-known-issues-list#:~:text=Microsoft%20is%20preventing%20a%20large,on%20a%20variety%20of%20PCs.)
I play on the same machine. 
Properly separating my personal OS and my development OS should be better in the long run, 
so I will start working from a [Kubuntu](https://kubuntu.org/) dual boot soon.

# Data access

In my first year as a data analyst, I focused on the data we found on the official Riot API.
 Unfortunately, they lack critical information. Picks and bans order is not recorded, and Chinese games are not available.

Therefore, I started working closely with [Leaguepedia](https://lol.gamepedia.com/League_of_Legends_Esports_Wiki) a year ago. 
As their data is open and meant to be easily queriyable by everybody, it was perfect. 
They manually input picks and ban for professional games as well as end of game stats for games with chrono break, 
making them one of the most reliable sources.

Accessing their data also meant I was able to spot human errors very fast, 
and I quickly came to work with Leaguepedia editors and staff to help maintain the wiki.

Since Leaguepedia staff spent a lot of time helping me access their data, 
I released [leaguepedia_parser](https://github.com/mrtolkien/leaguepedia_parser)
earlier this year to make sure they would not have to redo that work with other analysts.
I am also working on a full refactor (currently in alpha) that will use my new League of Legends game data structure,
but that will be the subject of another post!

As Leaguepedia and I were doing very similar things in regard to professional games parsing,
we also decided to pool our efforts together on that front.
I am proud to say that today new games on Leaguepedia are parsed entirely with code I wrote thanks to help I got from them,
[oracleselixir.com](https://oracleselixir.com/), and [gol.gg](https://gol.gg/).
It will make their maintenance of the website’s tools much easier in the future.

The important thing to get from this is that it’s always better to make allies than foes.
By making a conscious effort to help Leaguepedia and spending time developing tools with them,
I now have access to much better data.

I always strive to make data access as open as possible as I think more cooperation leads to more reliable data
and maintainable code.
I hope other actors in esports analytics see that and start working together in the future instead of
pitting everyone against each other for access to basic game information.

# Data accessibility

As I have said, one of the issues I faced with working in python was giving access to data to the rest of the team.
While I can write detailed reports, coaches often want to access the data themselves.

The first tool I developed on that front was a Discord bot.
Discord is pretty ubiquitous in the gaming community by now, and [discord.py](https://github.com/Rapptz/discord.py)
is a great package to create powerful bots.
With embeds, files attachment, and pure python code, you can give access to the data in multiple formats.

![team stats example](https://i.imgur.com/fzNX1B9.jpg "team stats example")

For example, my !team_stats command outputs an embed table, a kill heat map file attachment, as well as a google
 sheets link to have a complete data export.

Working entirely in python allows for very powerful functionality in the bot, in particular the google sheets
 integration for export through [gspread_pandas](https://pypi.org/project/gspread-pandas/).

My first version of the bot ran purely in python, requiring a pretty complex python environment to run and connecting 
directly to the database.
This is hard to maintain, and means tons of analytics functions I built were very closely linked to the bot’s
 functionality.

I have therefore decided to go for a more modular approach by developing an internal API with
[FastAPI](https://fastapi.tiangolo.com/).
This will allow me to better separate accessing the data vs displaying the data. 
In particular, this will allow me to be language-agnostic and to access the data from Javascript code, 
which will make developing user-facing tools much easier.

# Data back-end
I was hesitating between RDBMS and NoSQL solutions when I started, and by now I don’t think learning how to use a
 document-based database like MongoDB would bring me anything that my SQL experience does not.

SQL and python usually means [SQLAlchemy](https://www.sqlalchemy.org/), and this is no exception. 
My SQLAlchemy package is the core of my work, and I am always working to add functionality to it. 
I must have read the documentation at least 10 times and still don’t understand half of it, but it’s great.

SQLAlchemy also made it much easier to switch database systems.
I used MySQL, sqlite, and PostgreSQL over the past months, and all my data is now in an 
[RDS PostgreSQL instance](https://aws.amazon.com/rds/postgresql/).

I also moved to caching all JSONs I received from any API endpoints on [Amazon S3](https://aws.amazon.com/s3/),
as data has been shown to sometimes disappear in the past.

# TL;DR stack
- Languages
    - SQL, Python, Javascript
- SQL database
    - PostgreSQL
- Back-end
    - SQLAlchemy, FastAPI, gspread_pandas
- Front-end
    - discord.py, React
- Environment management
    - Docker
- IDE
    - Pycharm Pro, planning to switch to VS Code
- Development OS
    - Windows, planning to switch to Kubuntu
- Deployment OS
    - Amazon Linux 2

# Conclusion

My stack has gone through multiple iterations, but I am finally at a point where I can say it is well
 designed and maintainable.
 
 I learnt everything by myself over the last year and a half while being a data analyst, which has been challenging
at times. As I am approaching the end of my current refactor, I will be able to focus on data
analysis for the foreseeable future.
   
And when I say foreseeable future I mean the two weeks until the Valorant API gets released!
