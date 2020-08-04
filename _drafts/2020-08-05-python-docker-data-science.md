---
layout: post
title: "Python & Docker for data science"
categories: development
---

Docker is the new be-all-end-all of environment management for software development. By providing a concise and heavily customizable way to handle dependencies resolution for multiple programming languages as well as providing a "runtime system" for just about everything, it is slowly but surely supplanting other options. WSL 2 for Windows in particular is a huge boon for Docker, making it run very well on Windows.

Python, on the other hand, suffers from relatively poor tooling regarding environment management and particularly clumsy deployment processes. I personally cannot count the times I could easily write a script to solve a friend’s issue but it took me 2+ hours to help them run it on their machine. Packaging python code is no easy task, especially when working with packages undergoing development and with closed source.

In the past year, I read multiple articles about using Docker for Python development but I was never satisfied with the guidelines proposed. Articles usually focus on web applications development, which is a very different development paradigm than data science. They also rarely talk about testing. All of this really put me off, and it took me a long time before even considering Docker.

But as I realized my deployment practices were bad I pushed onwards and forced myself to make the move. All this work paid off as I am now able to download my development environment on any machine in a matter of seconds, as well as all the apps I developed around it.

Let’s dive deeper, step-by-step, in how I got there.

# Python environment management

Python environment management is one of the weakest points of the language. `pip` does its job pretty well for pypi-hosted packages, but as soon as you stray outside the beaten path and need to use closed-source source-installed packages it all goes south.

Before understanding how to use Docker for python, it is important to understand python environment management itself as Docker will still be using it.

## Understanding python environments

Python works with an **interpreter** that has access to specific **packages**. 

A single system can, and usually *will*, have multiple python interpreters installed. MacOS in particular comes with both python 2 and python 3 installed. An interpreter is what most people will know as a python version, like `3.8.4`.

Even worse, you usually do not want multiple projects to use the same "list" of packages. If you did so all your projects would automatically use the "latest" packages you installed, creating bugs as soon as anything that is not back-compatible pops up. Which is to say, almost every week.

And packages themselves can ask to download and install other packages from `pypi`. This is done through their `setup.py` file. This means that updating a single package can have ripples through the whole environment.

So every python developer uses [**virtual environments**](https://docs.python.org/3/tutorial/venv.html). While it may sound complicated, "using a virtual environment" pretty much means "pointing your interpreter to a specific package folder". You create this folder, install packages in it, and tell your interpreter to **only** look at this folder of packages.

While it’s all nice and dandy, a very important part of software deployment is replicability, *ie* making sure what works on your machine will work on another one.

## Interpreter tools

So as you see, every time you have to start by installing the interpreter you want. There are many versions of python available, with every new one bringing non backwards-compatible changes. If a single of your packages uses the [walrus operator](https://docs.python.org/3/whatsnew/3.8.html#assignment-expressions), you **need** 3.8 or higher.

One of the most popular tools for that is [`pyenv`](https://github.com/pyenv/pyenv). Unfortunately it’s almost unusable on Windows, so on Windows you usually use [pre-built Windows binaries](https://www.python.org/downloads/windows/). Of course, on Mac OS you can use [`brew`](https://brew.sh/) to install python directly, but you can also use it to install pyenv that’ll install python itself. See the mess already?

## Environment tools

### venv + pip

Python has [`venv`](https://docs.python.org/3/library/venv.html) installed as part of its standard library. This means that `venv` is part of one of your python environments.

It is the recommended tool to use, and many higher level tools simply call venv themselves. `venv` is only a command line tool after all. You first need to select the right interpreter, then call venv with it.

Once you have created a virtual environment, you must activate it by sourcing an activate script in its bin directory. A very fun task on Windows with its great cmd.exe.

And once activated, you can use `pip` to install packages to this virtual environment. You can afterwards open a console or run python scripts with it directly.

If you are using this method, the recommended way to replicate the virtual environment is using a "requirements.txt" file generated with `pip freeze > requirements.txt`. This is pretty much a list of commands that pip will execute through `pip install -r requirements.txt`.

It works pretty well when you are simply installing packages from `pypi` as you will be able to grab the exact right version every time, but it gets pretty messy when you want to install packages from git and guarantee a specific commit.

## pipenv

One way to make things slightly easier is `pipenv`. `pipenv` can use `pyenv` to download and use the right python interpreter. `pipenv` also handles virtual environment creation, installation of packages, and replicability.

It can be called from the command line outside of the virtual environment. Its list of installed packages is stored in a [`Pipfile`](https://github.com/pypa/pipfile) and you can directly add a package to the list and run `pipenv update` to install it. It guarantees replicability by storing checksums of each installed package in a joined `Pipfile.lock` file.

`pipenv` is a huge step in the right direction for python environment management. Alternatives like `Poetry` exist, but it seems that `pipenv` is the one gaining traction at the moment.

## What about code that is NOT on pypi?

While a very convenient tool, `pipenv` is only a wrapper for the other tools we have just seen. It still does not make it much easier to work with editable dependencies and git-based packages. You can make it work, but it makes your development environment clumsy and inconvenient in my opinion.

# Real life example

Let’s look at my use case, using python for data analysis.

## lol_data

`lol_data` is my base package, relying heavily on [SQLAlchemy](https://www.sqlalchemy.org/) to handle everything that is database-related. It handles the connection, data structure, and querying. As this package is the first building block for any tool I build, it is minimal in its dependencies and focused on performance.

## lol_data_parser

`lol_data_parser` is my parser, *ie* an app that is designed to run continuously and parse LoL data from all around the world and insert it into my database. It uses heavier packages like [`scikit-learn`](https://scikit-learn.org/) for role classification.

## lol_data_scripts

`lol_data_scripts` is my collection of scripts. It holds the scripts I wipe up when coaches or players have a question and that I need to do some exploratory analysis. It is mostly made of Jupyter notebook files that I run in Pycharm’s python console.

## lol_data_api

`lol_data_api` is a [`FastAPI`](https://fastapi.tiangolo.com/) based API that serves data in the JSON format. It allows me to build tools in other languages than python, namely websites with [React](https://en.wikipedia.org/wiki/React_(web_framework)).

## lol_data_discord_bot

`lol_data_discord_bot` is the user-facing part of this stack and is a [`discord.py`](http://discordpy.readthedocs.io/) based bot. It used to be based directly on `lol_data`, but with me moving to an API structure it is now an independent app that gets its data through the `lol_data_api`.

## Structure

Here is the approximate structure of my "hierarchy" of projects:
```
lol_data 						python package
├── lol_data_parser				app requiring lol_data
├── lol_data_scripts			scripts requiring lol_data and other dependencies
└── lol_data_api				app requiring lol_data
	└── lol_data_discord_bot	app using lol_data_api
```

`lol_data`, `lol_data_parser`, `lol_data_scripts`, and `lol_data_api` are all part of the same git repository as they are strongly interconnected. Updates to one usually begets updates to the others, and I want to keep it all together.

`lol_data_discord_bot` is in another repository as it does not use `lol_data` directly.

## Old deployment practices

### v1

When I wrote my v1 I had been using python for about a week. I was still discovering the whole environment offered to me.

So I went for a stupid but working solution. I did not bother with a virtual environment on my deployment server as I planned to only run my parser at the time. I replicated my dependencies with `pip freeze` and installed both `lol_data` and `lol_data_parser` dependencies in my system-wide python environment.

And to handle having access to `lol_data` I pulled it from git and added the folder to my `PYTHONPATH` environment variable, meaning it could be imported in any interpreter I opened.

To update `lol_data` or `lol_data_parser`, I would just do a `git pull`, then run the parser with `python run_parser.py` in a `tmux` window.

As you can guess, that was not particular stable, convenient, and clean.

### v2

Shortly after, I discovered `pipenv`, and I used it until I made the switch to Docker.

It was very convenient for finally having a virtual environment and having a better way to handle python versions, but it was still a mess to handle the import of `lol_data`.

My work flow was to create the `lol_data_parser` environment with its own dependencies, activate the environment with `pipenv shell`, move to the `lol_data` folder, and use `pip install -e .`. With the `lol_data` dependencies defined in its `setup.py`, it automatically installed the dependencies in the virtual environment as well.

But updating it was a pain. Updates to `lol_data/setup.py` did of course not ripple to `lol_data_parser` and required a re installation of `lol_data`. While serviceable it was cumbersome.

# What is Docker anyways?

I’ll be honest, it took me some time to properly wrap my head around Docker. It is actually simpler than it looks, but you need to understand the vocabulary. So let’s walk through it!

## Images

You can see a Docker image as an archive of files that are sufficient to define a Linux environment. It is a folder of binaries and files that can be run on a Linux *kernel*. They are **built** from a [`Dockerfile`](https://docs.docker.com/engine/reference/builder/).

By itself, a `Dockerfile` does not guarantee replicability in any way. But a built image does. 

## Containers

Containers are running images. They’re pretty much a running virtual machine. You can access their logs, stop and restart them, and usually you destroy them once you’re done with them.

An image usually has a default command it will run when a container is created. It is defined by the `CMD` line in the `Dockerfile`. For my parser it is a shell script, `CMD [ "/bin/bash", "/app/run_parser.sh" ]`.

## Volumes

Volumes is persistent storage across containers. While you can write to files inside a container, those files will be destroyed if you destroy the container. Using a Docker volume allows for persistence.

The other option is mounting a folder from your computer inside a container, which we’ll talk more about very soon.

## Docker-compose

Compose is a huge part of Docker. It can be used to control multiple inter-dependent services, but more importantly it can replace `docker run` options. Instead of having a very lengthy run command that you need to type each time, you can define most of the run options in a `docker-compose.yml` file. I won’t delve into it in depth, but it’s a key part of Docker.


# Python & Docker for data science

Finally, now that all the groundwork has been laid, we can start talking about how to go about setting up Docker and python for data science.

One of my biggest pet peeves with Docker is that there are 10 000 ways to do any particular thing. While the documentation is very exhaustive, it can be hard to find out what is the *"right"* way to do something. I am not sure mine is the right one, but at least it is sort of coherent.

Another important thing to note is that almost everything you will do with Docker is through the command line. But thankfully if you are using WSL 2 inside Windows everything can be done from your Linux virtual machine, making it incredibly smoother than using cmd.exe or PowerShell.

## Defining a python environment

The best thing about python in Docker is that there are [official images](https://hub.docker.com/_/python) for us to use already maintained and curated by the Python Software Foundation. For every python release there are multiple images depending on your application’s needs. From lightweight alpine distributions to full Debian images, you will find what you want.

Personally, I’m going the easy route and start my root image with `FROM python:latest`. While heavy, it is the image that makes the development process the easiest and guarantees you have the latest features available.

Then, we need to install the dependencies for our project. Looking at examples, you will see most people advising to use a "requirements.txt" file and install it to the global python interpreter inside the image.

My gripe with that is that requirements.txt is not meant to be human-written. It is a format standard that is meant to be the output of `pip freeze`, pinning package versions. And if you are generating this file from a local environment, you’re clearly doing it wrong since you want all your work flow to be inside docker containers. You do not want to need a working python environment on your machine.

Unfortunately, other available solutions are not much better. `pipenv` development paradigm is also centered around having a local environment.

I saw two options:
- Directly write the pip commands inside the Dockerfile
- Write a `.txt` file with dependencies but name it differently for clarity

Writing pip commands inside the Dockerfile actually allows for faster rebuilding of images. As each command generates its own Docker "layer", adding a new package starts where the preceding one left off. Unfortunately, it makes the Dockerfile very verbose, and package dependencies start getting all over the place when doing multi-stage builds (which we’ll come to very shortly).

So I went with using a hand-written "requirements_xxx.txt" file as source, copying it inside the image then running `pip install -r requirements_xxx.txt`. To clearly differentiate it from standard requirements, I used different names for different applications.

![requirement files](https://i.imgur.com/1obMMCW.png)

As we will see, I used multi-stage image builds to not repeat myself in the dependencies. For example, `sqlalchemy` is only defined as a dependency of the root `lol_data` image, which installs dependencies from the following `requirements_base.txt`:

```
# This is the list of packages required for lol_data
lol-id-tools
lol-dto>=0.1a10
sqlalchemy
psycopg2
```

## Mounting vs copying

By now, you might have understood one weird thing about Docker. There are two very different ways to access your source code inside a Docker image. Either you copy it, or you mount it from your local file system. Those two solutions achieve wildly different goals.  I never really see it pointed out when in my opinion it is crucial to have a proper Docker work flow.

Copying the source code inside the image is the "obvious" way of doing it. This means that the built image will contain a specific version of your source code. By doing this, any source code change will require rebuilding the image, as well as restarting a container if you want to open a python console.

But mounting a folder with your source code inside a container is the way most people use Docker for development. Both PyCharm and VS Code even do it transparently when you tell them to use a Docker image. They create a container, mount your source folder into it, and define it as the working directory.

This means that I went with copying code for relatively mature parts of my code, like `lol_data`, while I mounted folders to work with apps undergoing **development**, like `lol_data_parser`. And to **deploy** `lol_data_parser`, I made another image that includes its source code directly.

## Multi-stage Dockerfile

One of the most important thing for me to have a smooth Docker work flow was Using [multi-stage builds](https://docs.docker.com/develop/develop-images/multistage-build/). You can use a single `Dockerfile` to define multiple images, usually images that will be dependent on one another. You can then create a specific image with `docker build --target`.

It was useful to generate:
- Both dev and prod images without code duplication
- Multiple images based on the same "root"

Let’s have a look at my current Dockerfile that can generate up to 8 different images, but where only 5 are actually used.

```docker
# BASE ENVIRONMENT
# This is an image that gives access to lol_data to any other app 
FROM python:latest AS lol_data_env

# Installing packages from pypi
COPY requirements_base.txt /
RUN pip install -r /requirements_base.txt

# Creating a work folder so our code is neatly organized
WORKDIR /app

# We add the folder to PYTHONPATH for easier imports
ENV PYTHONPATH "${PYTHONPATH}:/app"

# Copying the lol_data package (which will be importable anywhere thanks to the previous line)
COPY /lol_data/ ./lol_data


# PARSER

# PARSER ENVIRONMENT
# This is the base python environment for lol_data_parser
FROM lol_data_env as lol_data_parser_env

# Installing parser-only requirements from pypi
COPY requirements_parser.txt /
RUN pip install -r /requirements_parser.txt


# PARSER DEV ENVIRONMENT
# This is the dev environment for the parser, which requires mounting the sources
FROM lol_data_parser_env as lol_data_parser_dev

# Since dev-only dependencies are short, I install them directly here
RUN pip install pytest python-dotenv


# PARSER PROD APP
# This is the production-ready application for the parser
FROM lol_data_parser_env as lol_data_parser_prod

# We copy the parser’s source code and the parsing script inside 
COPY /lol_data_parser/ ./lol_data_parser/
ADD run_parser.sh .

# Finally, we start the script
CMD [ "/bin/bash", "/app/run_parser.sh" ]


# SCRIPTS

# SCRIPTS DEV ENVIRONMENT
# This is the environment for my scripts, based on the root lol_data_env image
FROM lol_data_env as lol_data_scripts_env

# Scripts have their own dependencies, separated from the parser
COPY requirements_scripts.txt /
RUN pip install -r /requirements_scripts.txt

# For easier configuration I copy config files inside the image where they’re expected
COPY /config/gspread_pandas /root/.config/gspread_pandas


# API
(...)
```

As you can see, most of my images "inherit" from `lol_data_env` and add what they each need. I did it by creating an intermediate image that only holds the environment, like `lol_data_parser_env`, then splitting it into a `dev` image that will use mounted source code and a `prod` that copies the source code and has the `CMD` to start the app.

In the end, I only use `lol_data_parser_dev/prod`, `lol_data_api_dev/prod`, and `lol_data_scripts_env`.

## Replicability and distribution

There is another elephant in the room I haven’t touched upon. `python:latest` may change with time. `pip install` might not yield the same packages in the future with non-pinned versions. Unfortunately, only having a `Dockerfile` does absolutely nothing to guarantee replicability in python.

Also, only using a `Dockerfile` and relying on the host to build it means every server you deploy would need to install git, get access to your repositories, pull them after every change, and rebuild the image after each change. This is far from convenient.

The reason is that **this is not how Docker is supposed to be used**. Docker is built to share **images themselves**, not `Dockerfile`s. Sharing the images themselves is the actual strength of Docker, creating a full snapshot of a particular version of your app, guaranteeing its exact behavior to be unaltered on any host. 

Personally, I use a [private Docker registry](https://aws.amazon.com/ecr/) to host my images, but the `docker save` function allows you to simply create a `.tar.gz` archive of your image ready to be deployed anywhere. The benefit of using a registry is the easy of update on your deployment servers.

Once I have built and uploaded the latest version of my parser to my registry, I can simply run `docker container stop lol_data_parser && docker-compose pull && docker-compose up -d` on my server and it will automatically update to the latest version and restart. This reduces what I have to do on a new server to simply installing Docker, identifying to my registry, and creating a `docker-compose.yml` file to specify run arguments.

For example, this is what the `docker-compose.yml` looks like for my parser:
```docker-compose
services:
  lol_data_parser:
    image: REGISTRY_URL/lol_data:parser_prod
    container_name: lol_data_parser
    env_file:
      - env/aws_parser.env
    volumes:
    - type: bind
      source: ./logs
      target: /app/logs
```

## PyCharm vs VS Code paradigm

Finally, to highlight how nobody agrees on how to use Docker just yet, let’s close this out by looking at Docker’s integration in PyCharm and VS Code.

PyCharm can be told to use Docker as a python environment and will create a new container whenever you open a console or run unit tests. You will still mostly be on your local machine, only using Docker to provide you with python environments on demand. You can use a `docker-compose.yml` file to supply your environment with specific bind mounts or environment variables.

VS Code on the other hand makes you work **inside** a specific container, mounting your source code inside it. It will not spawn any other containers, but you can open multiple python interpreters inside of this specific container. But as a container is technically not an image, I was kind of lost as to what was the right work flow with this approach. The integration was much better than PyCharm though!

As I am using PyCharm currently I am getting used to its way of using Docker, but I feel like VS Code approach of working inside a single container is "tidier".

# Step by step setup with PyCharm on Windows

So this was long-winded and I think that closing it out with a step-by-step will help make everything clearer!

## Required programs

### WSL 2

Follow the instructions there: https://docs.microsoft.com/en-us/windows/wsl/install-win10

Personally, I recommend using [Ubuntu for WSL 2](https://docs.microsoft.com/en-us/windows/wsl/install-win10#install-your-linux-distribution-of-choice) as they seem to pay special attention to this use case of their distribution.

If you cannot use WSL 2 because you cannot update to the latest Windows version, I legitimately advise against using Docker. You would have to control everything through PowerShell while everything would be much slower, which is close to the 6th circle of hell. Personally, I reformatted my Windows partition just to be able to install WSL 2.

### Terminal preview + ZSH

Before moving forward, since Docker is mostly a command line tool I advise taking a bit of time to create a good command line environment on your WSL 2 virtual machine.

Start by downloading Windows Terminal, the new official terminal for Windows: https://www.microsoft.com/en-us/p/windows-terminal/9n0dx20hk701

Install [zsh](https://linuxhint.com/install_zsh_shell_ubuntu_1804/) and [oh-my-zsh](https://ohmyz.sh/#install) on your WSL machine.

Once done with the installs, edit your zsh config file, `.zshrc`, and activate the `docker` and `docker-compose` plugins. This will turn on auto completion for every docker command, automatically completing functions and container names. This package is [officially maintained by the Docker team](https://docs.docker.com/compose/completion/#zsh).

I also advise installing [`fzf` for easier auto-completion](https://github.com/junegunn/fzf), [z for directory jumping](https://github.com/ohmyzsh/ohmyzsh/tree/master/plugins/z), [fast-syntax-highlighting](https://github.com/zdharma/fast-syntax-highlighting), [zsh-autosuggestions](https://github.com/zsh-users/zsh-autosuggestions), and [powerlevel10K](https://github.com/romkatv/powerlevel10k). With all this using the shell actually becomes a breeze.

![console](https://i.imgur.com/5ABFFw6.png)

### Docker desktop

## Dockerfile

