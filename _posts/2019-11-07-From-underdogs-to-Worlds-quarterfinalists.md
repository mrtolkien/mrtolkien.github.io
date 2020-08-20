---
title: "From underdogs to Worlds quarterfinalists — A year at Splyce"
categories: Personal
tags:
  - Esports
  - LoL
---

This is the first in a series of articles looking back at my year 2019. As the introduction, this one is pretty personal and focused on what I learned during this year.

![Fear the snek](img\1____OUVx1NlkUW50JIF1SfJmg.png)

*Fear the snek*

# Before it all started

Talking about my year 2019 needs a bit of context. I will turn 30 in December and in the last ten years I have been a:

*   [Starcraft 2 Youtuber](https://www.youtube.com/channel/UC54dcAoEXY2ws6bMjBz8aYA)
*   [League of Legends streamer](https://www.twitch.tv/tolkicasts)
*   [League of Legends caster](https://www.youtube.com/watch?v=BkA_W_tx-qY&list=PLkUujrXHJknWfJ_bcvWGqVfCNC5f8Nd6G&index=4)
*   [IT consultant focused on Android and Big Data development](https://www.octo.com/en/)
*   [Magic: the Gathering writer](https://magic.wizards.com/fr/articles/archive/321521)
*   [Associate Producer on Mario vs Rabbids](https://www.mobygames.com/game/switch/mario-rabbids-kingdom-battle/credits)
*   [League of Legends team owner and coach in Japan](https://web.archive.org/web/20180322103914/http://www.hokutoesports.com/)
*   [Artifact writer](https://drawtwo.gg/articles/how-to-think-like-a-combo-player)
*   [League of Legends Lead Data Analyst at Splyce](https://splyce.gg/content/753/leveling-up-splyce-tolki-data-analyst)

And I’m not even talking about the time when I tried to become a [Shadowverse Youtuber](https://www.youtube.com/channel/UCRW2vvAs4YvR1-CBaKMwlwg).

To say my resume is a mess is quite the understatement. After failing to qualify for LJL with my team in mid-2018, I was lost. I had been living in Japan for two years and no clue what to do next. My messy resume was a bit too scary for traditional companies and I failed interview after interview due to my Japanese skills dwindling.

I knew I learned a lot from my experience at the head of a LoL team but wasn’t finding any way to leverage those skills in Japan.

After almost six months of failures and introspection, I chanced upon this tweet by [Duke](https://twitter.com/Duke_Esports):

Thanks [Chips](https://twitter.com/Twisted_Chips) for the retweet 👀

This was a full time, remote, LoL-related, technical position. It felt like I just crossed a unicorn.

A week later, I was hired.

# Setting goals

I started the year with a simple goal from Duke: see what could be done with LoL data and go as far as possible in a year. From patch understanding and smurf detection to opponent’s scouting or picks and bans prediction, I had _carte blanche_ to implement any method I saw fit to be useful to the team.

I decided to also use this year to get back to a good technical level, as I had been in management positions for a few years. I focused on [using the most popular data analysis tools at the moment](https://medium.com/@gary.mialaret/pioneering-data-driven-esports-analysis-b57d5079abda) despite having no experience with them. From Python to SQL through Debian servers management, I knew I needed to learn those skills to be the best LoL data analyst possible. A lot of analysts on LoL are undercover assistant coaches, and my goal was specifically to not fall into this trap and bring another point of view.

As LoL data analysis is still in its infancy, I also knew I had to build everything from scratch. There was a long uncharted road ahead of me.

# Coding is fun

To be honest, I never thought of myself as a developer. Even though I have a Master of Science in Machine Learning, I mostly focused on the research side of it and never had to deliver quality code. Even when I was working as an IT consultant I was always suffering from imposter syndrome and felt deeply incompetent.

Python reignited my love for software development.

I’m not sure why, but it all came together this year. I loved learning all those new skills even though I spent upwards of 12 hours a day on it at the beginning. I finally could do [test-driven development](https://twitter.com/TolkiCasts/status/1175312660834865153) on a real project.

I think at heart I love work well done, and software development is a field where attention to detail and craftsmanship matters a lot. Thanks to full test coverage, I could focus on regular refactors to make my module as efficient as possible. I currently sit on the 4th version of my library, and I am confident to say it is the most powerful LoL analysis tool out there.

Let me share how you would get all blind picks for a given team since June 2019:

Code so simple even an analyst could write it

This script takes 150ms to run, which I consider decent enough since it’s brute-forcing everything for convenience sake.

[As Mark Rosewater says](https://magic.wizards.com/en/articles/archive/making-magic/how-get-your-dream-job-2012-06-04), your dream job lies at the intersection of what you are good at, what you like, and what people are willing to pay you for. Focusing on development this year was an eye-opener, making me realise I both enjoyed it and was decent at it. I would now feel confident going back to technical positions in traditional companies, which was far from a given a year ago.

# I love esports

But going to Google or Microsoft would likely involve abandoning esports, and I can’t bring myself to it. I have been gravitating around the field for more than 10 years and this year cemented my love for it.

Until 2019, I never worked in the “real” esports market. I was a middle of the pack French caster, wrote articles in French for a game where all the good content was in English, and owned a LoL team that never won anything. Stepping into LEC made me discover [a whole new world](https://www.youtube.com/watch?v=hZ1Rb9hC4JY).

Splyce got into franchising at the last possible moment, and the team was put together in a rush. My onboarding process was more than bumpy. Nobody thought we’d be more than bottom feeders, especially seeing Misfit’s and Origen’s rosters.

Despite this, I loved the “purity” of working in an esports team. Being in a competitive environment means there’s only one goal: winning. There’s no politics, no bullshit, everybody is just here to win as many games as possible. I loved talking about items and runes with players. I loved talking about draft with Duke. I loved crafting new metrics and KPIs weekly to help us better understand the game. Nothing comes close to the rush of playing a series you trained months for.

Over the course of the year, we took games off Fnatic, G2, FunPlus Phœnix, and SKT T1. We were contenders, and I am proud to say my data analysis was a part of Splyce’s 2019 run.

Despite this, I am not sure if being a data analyst is the position that fits me best in an esports team. Being data-driven shouldn’t be exclusive to data analysts, and looking back on my experience as a coach I feel like it was the kind of position that suit me best. I think my strength lies in being able to understand and get along well with players while staying professional. I will explain in my next article how I see the “optimal” organisation of a coaching staff, which will better explain how I see the role of head coach.

# Understanding LoL data

LoL is inherently a game about numbers, and therefore data. I want to talk about creating meaningful metrics for LoL as traditional ones like win-rate or average creep score difference at 15 don’t tell us much, but after starting writing it I was already past 5 pages. It will therefore be the subject of a standalone article in the near future, look out for it!

Anyways, my LoL experience helped me a lot in making sense of the data and it helped me build up my analytical skills. I am still far from good at statistical inference, but I started understanding the core concepts better this year thanks to working with data I had a strong interest in.

I also think studying esports data is a good gateway to data analysis for students. In general, I feel like esports are a great educational starting point for the new generation, as it gives them a field they enjoy and relate to while having a lot of very interesting technical challenges.

# Tokyo life

As I live in Japan, I worked all year remotely from Tokyo, only coming to Berlin for summer split preparation and worlds.

At the beginning, it was great. I could focus on development during daytime and start interacting with the team around 5 PM JST.

But it quickly became apparent the lack of social interactions was taking its toll on me. I would spend entire weeks not talking to anybody in person but my wife. I tried going to co-working spaces but it wasn’t cutting it.

Not being in person with the team also made it so I missed a lot of information. It is hard for a team seeing each other every day to integrate a single remote worker, so I had to be a bother time and time again to keep myself updated.

Overall, I feel like to work remotely efficiently you need to be fully integrated into the company’s workflow. I also think that for full-time remote you need to be close to people who understand your work, as it helps both socially and professionally.

If I had to do it again, I am not sure I could find a solution. Living in Japan is definitely a huge detriment to my career if I want to work for a LoL team. After this year, I am willing to relocate if I find an appealing opportunity.

But as I still wish to stay in Japan, I will also look at other options. For example, I could go deeper on the technical side of LoL data, helping other teams setup their own tools, or develop new ones either by myself or with an existing company.

# TL;DR of my year 2019

*   Bounced back from a rough 2018
*   Gained confidence back in my technical skills
*   Deepened my conviction that I want to keep working in esports
*   Went deeper into data analysis, a field I always skirted around in the past
*   Realized how taxing it was to be working 100% remotely

# Looking to the future

With our worlds run being over, I am now looking towards 2020. As I see things, here are my options, in order of preference:

*   Work for a team as coach
*   Help multiple teams include data into their workflow and act as a consultant
*   Join a game development company and work on game analytics/balance
*   Join a company in the “esports data” field
*   Work for a team as data analyst
*   Leave esports

I am still unsure as to what to do next, and also what people are willing to hire me for. Even though my last position attracted a bit of attention I am still relatively unknown in the LoL scene, which makes finding interesting positions much harder.

I don’t what 2020 has in store for me, but I can’t wait to see. Here is to one more year of craziness!