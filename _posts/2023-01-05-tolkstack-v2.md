---
title: "Tolki's Stack - 2023 edition"
categories: Development
tags:
  - Python
  - Rust
  - PostgreSQL
  - VSCode
  - Vim
header:
  image: /assets/images/2023_01.png
---

In January 2020 [I made a blog post explaining my tech stack](https://blog.tolki.dev/development/lol-data-stack/). At the time of writing I was leaning heavily into Python, Postgres, SQLAlchemy, FastAPI, and Docker.
I had plans to switch from PyCharm to VS Code and finally ditch Windows for a Debian variant.

While some of those tech choices have changed I'm pretty happy with what I decided on back then. But I am now at a crossroads where I will heavily change my stack and it went through a few iterations in those last three years. I think now is a good time to review those changes and decide on the next steps!

# Dev environment

## OS

In the end I did not fully move to Linux. I used Ubuntu for ~6 months in late 2021, but after getting into Age of Empires 4 and wanting to play some LoL once again I moved back to Windows 11 relying on WSL2 for my development environment.

Unfortunately I've had quite a few issues with my Windows workstation in the past few years:

- RAM sticks becoming unstable after ~2 years of usage
- WSL2 issues in Windows 11 including crashes and requiring reboots to work
- Inability to use anything else than VS Code for working with WSL2 smoothly
- No laptop option that really impresses me, or they're the same price as a MacBook Pro

All this is making me go back to Macbooks. I developed on MacBook Pro 2013 for 7 years before moving on to Windows and I'll be moving back to MacOS once the M2 MacBook Pro are released. They're really incredible machines and the ARM architecture is something that I want to push for in my future tech projects so it's a perfect fiu
I'll keep a Windows PC for gaming though 👀

## IDE

Up until summer 2021, I stuck to PyCharm. It was not perfect, but it did most of its job properly.

I had issues with its poor UI, "automagic" integration of many tools which made them more opaque than needed, and obtuse keyboard shortcuts for window management.

Once I started working with web developers and had to regularly edit and read multiple programming languages I made the full switch to VS Code. I've been a mostly happy VS Code user for about a year and a half now.

It has a great plugin ecosystem, first class support for all languages, and is the only IDE with full access to the Rust debugger. It's kind of eclipsing everything and becoming the standard for just about everything. I don't think I've opened Sublime Text in over a year now.

But I'm struggling with its shortcuts and its UI:

- Too many things don't have shortcuts by default, including very useful features like showing the hover info or creating a new terminal on Mac, so you end up with weird custom shortcuts and it gets messy
- Terminal panes not behaving the same as editor panes. This makes them hard to use, especially if you want to use terminal-focused tools like the Rust compiler. They added editors in terminal but it didn't solve the issue as tasks and many existing tools spawn the terminal in the bottom pane.
- Sidebar being full of crucial information for tools like `git` or the extensions instead of spawning an editor pane
- The UI still being quite a bit too thick for use on small screens. It's a real pain on my 13" MacBook Air where even two vertical panes makes the code hard to read.

This is actually what spawned this blog post. I wanted to spend some time reviewing my VS Code usage after 18 months and I ended up spending a full day trying out `Nvim` and `Emacs` 🥲

Unfortunately I'm still on Windows + WSL2 at the moment and this plays
relatively poorly with those tools. While they can be run fully in the terminal
they definitely feel way better with a native GUI like
[`Neovide`](https://neovide.dev/).

But I like `vim` for text editing and I've finally started using [VSCode Vim](https://github.com/VSCodeVim/Vim). Most of the time spent writing that blog post was actually time spent tinkering with the settings of this extension so it behaves exactly as I want it! And I'll give a shot to going full `nvim` once I make the switch to Mac in a few months, which will definitely gonna be a good subject for a new blog post. I have some groundbreaking ideas 👀

# Tooling

## Copilot

In my opinion Github Copilot is the biggest technological revolution of the past few years. Technology is at the forefront of innovation and economy at the moment and this tool increases productivity and more importantly code quality by quite a bit.

At the same time we have to learn how to work with it to really optimize its efficiency. For example it's great at writing unit tests and integration tests from a short description but not great at proposing good logic in front of a complex problem. It's also great at helping you discover a new API but it can offer you wrong or old solutions.

But one of the things that I don't see being mentioned much is how differently it applies to different programming languages. It *strives* with languages focusing on code quality and correctness. And by that, I mean Rust.

You, see when writing Rust Copilot cannot trick you into using a wrong solution because it will likely not compile. As it also helps writing unit tests quickly you can really get a high level of confidence in your code despite it being mostly AI-generated. More on that later!

## Sentry

I started using [Sentry](https://sentry.io/) this year and I just want to quickly share the love. It is super useful for monitoring anything that runs in production. It is also painless to use and built by great developers like [Mitsuhiko](https://fosstodon.org/@mitsuhiko@hachyderm.io).

I was always scared that it would introduce unnecessary complexity in my stack but it simply does not. You should use it too!

In the past year I've also started using [CodeCov](https://about.codecov.io/) for all my projects and they've recently been acquired by Sentry, so it's quickly converging into a one-stop CI/CD tool for me!

# Language

## Python

So. I still love Python and I'm still using it in a professional capacity.

But in the past few years I've started hitting some limits with it:

- Huge performance issues on a project where I needed to parse ~150 Mb JSON files
- Problematic packaging and deployment, for example with AWS Lambda
  - `poetry` + `docker` offer a decent deployment flow but environment management is still horrendous
- Encountering tons of bugs that were definitely due to my own mistakes but not raised by any linter nor caught by tests despite good code coverage

And there's also the Copilot thing. Python is both good and bad at working with Copilot:

- Good because it allows for easy generation of tests which are sorely needed in python
- Bad because code can easily be wrong in insidious way
  - While linters like `pylint` or `ruff` can help a lot they still don't solve all issues

## Rust

Recently tons of Rust projects bridging it with Python have started to pop up. `ruff` is an insanely fast linter written in Rust. `pydantic`, and therefore `FastAPI`, have undergone a full Rust rewrite in the past year which improved performance by multiple orders of magnitude.

So this made me curious, and I had been hearing about Rust for years at that point:

- High performance
- Memory safe
- Compilable to Web Assembly and therefore technically usable for front end (this is a bit of a meme tbh)
- Much beloved, topping StackOverflow developer surveys for almost the whole past decade
- Accepted as the second language for the Linux kernel which is a huge show of trust

So I gave it a shot. Started by reading [THE BOOK](https://doc.rust-lang.org/book/title-page.html). Continued by trying to do [Advent of Code 2022](https://github.com/mrtolkien/advent_of_code_2022/) in Rust. And finally [wrote my first program with it](https://github.com/mrtolkien/kindle_to_notion)!

And the most surprising thing in all that is that RUST IS ACTUALLY NOT THAT HARD. Its focus on correctness, coupled with a great compiler giving helpful error messages as well as a [great linter](https://github.com/rust-lang/rust-clippy) really help write high quality code quickly.

The high quality of the tooling is really one of the big reasons why I love Rust. `cargo check` and `cargo clippy` coupled with [bacon](https://github.com/Canop/bacon) to run tests automatically on file save really makes everything flow together super smoothly. [`insta`](https://github.com/mitsuhiko/insta) makes it a breeze to write tests for complex data structures.

I am still early in my Rust journey but I will try to use Rust on all projects that I lead as I think it results in more stable programs built from higher code quality codebases.

# Databases

## Postgres

So this is boring, but `postgres` is still the best.

My only issue with `postgres` is regarding storage usage. As there is no real compression options, I usually run it atop a `zfs` pool using `zstd` compression. On my home instance it gives me a crazy 3.64x compression ratio.

I reall wish compression was just built into `postgres` beyond `TOAST` compression for big values. Outside of that, it's the perfect database!

## TimescaleDB

Talking about `postgres`, I have started using [`timescaledb`](https://www.timescale.com/) this year. It's an open source `postgres` plugin that gives it a few great extra features:

- Compression 👀
- [Continuous aggregates](https://docs.timescale.com/getting-started/latest/create-cagg/)
- Much increased performance on some types of queries

Unfortunately, this is not painless. Timescale have their own concept of "hypertables", which are tables with a timestamp used to index the data. Only those tables can benefit from Timescale's features, and joins can't be used on continuous aggregates. This means you're expected to pretty much dump all your data in a single table and work with it.

While it's a decent data flow for many applications, it goes opposite to all I'm used to with `postgres`. So I'm still undecided at how much I'll use it in the future, but look forward to a database comparison post in the near future as I need to choose a database for my next LoL project!

## Redis

I use `redis` occasionally so it deserves a spot here. It's the best database for low latency workflows and it does its job well enough. I like the simplicity of it!

# Deployment

I started learning Kubernetes this year and deployed a cluster with 60 cores total in my closet. I might have gone a bit overkill.

It's a great tool and a great project. But in the end even for my work projects it's overkill. AWS Lambda does the work just well for IoT workflows with thousands of requests per seconds.

Managing a cluster would definitely increase performance thanks to `async` usage on the server, and it might reduce costs, but server upkeep for my single-person team is likely not worth it.

So no K8s at work just yet despite using `docker` almost everywhere already!

# TL;DR

- Windows + WSL2 (Ubuntu) on an x64 PC
  - MacOS on ARM soon!
- VSCode + VsCodeVim
  - Nvim in the future
- Github Copilot is a gamechanger
- Rust but still using Python for work!

{% if page.comments %}
<div id="disqus_thread"></div>
<script>
    /**
    *  RECOMMENDED CONFIGURATION VARIABLES: EDIT AND UNCOMMENT THE SECTION BELOW TO INSERT DYNAMIC VALUES FROM YOUR PLATFORM OR CMS.
    *  LEARN WHY DEFINING THESE VARIABLES IS IMPORTANT: https://disqus.com/admin/universalcode/#configuration-variables    */
    /*
    var disqus_config = function () {
    this.page.url = PAGE_URL;  // Replace PAGE_URL with your page's canonical URL variable
    this.page.identifier = PAGE_IDENTIFIER; // Replace PAGE_IDENTIFIER with your page's unique identifier variable
    };
    */
    (function() { // DON'T EDIT BELOW THIS LINE
    var d = document, s = d.createElement('script');
    s.src = 'https://blog-tolki.disqus.com/embed.js';
    s.setAttribute('data-timestamp', +new Date());
    (d.head || d.body).appendChild(s);
    })();
</script>
<noscript>Please enable JavaScript to view the <a href="https://disqus.com/?ref_noscript">comments powered by Disqus.</a></noscript>
{% endif %}

<script id="dsq-count-scr" src="//blog-tolki.disqus.com/count.js" async></script>
