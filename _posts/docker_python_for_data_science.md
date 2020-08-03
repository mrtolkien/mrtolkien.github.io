# Docker & Python for data science

Docker is the new be-all-end-all of environment management for software development. By providing a concise and heavily customisable way to handle dependencies resolution for multiple programming languages as well as providing a de-facto runtime system for everything, it is slowly but surely supplanting other options. WSL2 for Windows in particular is a huge boon for Docker, making it run with close to native performance on Windows.

Python, on the other hand, suffers from relatively poor tooling regarding environment management and particularly clumsy deployment processes. I personally cannot count the times I could easily write a script to solve a friend’s issue but it took me 2+ hours to help them run it on their machine.

In the past year, I read multiple articles about using Docker for Python development but I was never satisfied with the guidelines proposed. Articles usually focus on web applications development, which is a very different paradigm than data science. They also rarely talk about testing. All of this really put me off, and it took me a long time before fully moving to Docker for my work.

Despite all that, I pushed onwards and forced myself to make the move as I realised my deployment practices, while working, were bad. Packaging Python code is no easy task, especially when working with packages undergoing development and with closed source code.

All this work paid off as I am now able to download my development environment on any machine in a matter of seconds, as well as all the apps I developed around it.

Let’s dive deeper, step-by-step, in how I got there.


# Python environment management

# Understanding Docker

## Replicability

## Defining a python environment

## Distribution

# Real life example

## lol_data

## lol_data_scripts

## lol_data_parser

## lol_data_api
