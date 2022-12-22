---
title: "My note-taking journey - A foray into Personal Knowledge Management systems"
categories: Productivity
tags:
- Notion
- Obsidian
- PKM
header:
  image: /assets/images/obs_not.png
---

The biggest reason I've managed to enter [École polytechnique](https://en.wikipedia.org/wiki/%C3%89cole_polytechnique) is my note-taking love coupled with my ability to synthetize.

Back in 2009 I used to have binders of class notes, which then were made into binders of recapitulative notes with only the core substance. I would then iterate over those recapitulative notes to improve them, rewrite them, and make them easier to commit to memory.

Once I started spending more and more time on my PC, I stopped taking and organizing physical notes. As my workflow became increasingly digital, I didn't find the right way to manage the breadth of information I had access to.

So let's walk through this chronologically, from my first digital notes up to reading [Building a Second Brain](https://www.buildingasecondbrain.com/) this week and completely overhauling my systems!

# Early forays (2011-2021)

I created my [Evernote](https://en.wikipedia.org/wiki/Evernote) account in early 2011 and used it regularly until 2014.

![Evernote](https://i.imgur.com/8uk8w6g.png)

It was messy, my notes looked like shit, but it worked for me. It was a tool that was ahead of its time, and I was not using even 10% of its features.

When they announced that it would become paying to sync notes across devices, I was already falling off note-taking and I dropped the app.

So I switched to something that fit my needs and was just released, [Google Keep](https://en.wikipedia.org/wiki/Google_Keep).

For seven years, Google Keep was good enough for me. I used it to take short notes, write tasks lists, and share small snippets of information. I used its tagging system and search to quickly find the information that was relevant to me. I used its reminders features for any time-sensitive task or information.

![Keep](https://i.imgur.com/TBxwvBp.png)

It was basic and very limited, but it mostly worked. Taking notes was quick, finding information was quick. It had good keyboards shortcuts too, which made it super fast to use for me.

But after years of taking notes, its limitations became increasingly clear. No formatting. No prioritization of tasks. No automation. No folders.

In the meanwhile, I saw the rise of team information and tasks management tools. From Confluence, Jira, Trello, Shortcut, to `github` wikis and `mkdocs`, there were tons of great tools to create comprehensive collaborative knowledge systems. But what about personal knowledge?

# Discovering Notion

A bit more than a year ago, I was looking for a new note-taking app. I tried OneNote, Apple Notes, Evernote, Joplin, and many more.

Then, [Petter](https://twitter.com/petkasp) talked to me about Notion.

I launched it and was instantly blown away. It just *worked* and everything made sense. The database paradigm, with its multiple ways to visualize data, was groundbreaking. Everything was a page, and page could hold any metadata through databases. It was everything I was looking for.

I used it daily for about 18 months. I wasn't taking that many notes, but I was categorizing all of them in neat "folders" of pages. I was using databases for tasks and recipes, where they worked perfectly. And its search feature worked really well, giving me quick access to any note I took in the past in seconds.

But I wasn't capturing much because:

- Notion requires to be online to be used and is very slow to start
- Note creation is pretty clunky, especially on mobile
- I needed to use my mouse *all the time* for pretty much any thing I wanted to do on desktop

I knew I was only scratching the surface. It did most of what I wanted even though it was not perfect. And during my search for note apps I heard a lot about [Obsidian](https://obsidian.md/) and [LoqSeq](https://logseq.com/) so I knew there were other solutions out there. I had them on my TODO list as `Later` tasks.

Then, two weeks ago, my mom asked me about my note-taking systems. She's 55 and needs help with digital knowledge management and wanted a good solution for herself.

So I did the only thing I know. I went *waaaaaay too deep*

# Building a Second Brain

I started by watching a video on the subject by a Youtuber I like: [Knowledge Management For Software Developers - YouTube](https://www.youtube.com/watch?v=C5ycVOMaiwU).

In this video, he talks about the book [Building a Second Brain](https://www.buildingasecondbrain.com/), so I started by reading the book. And it ticked.

Tiago Forte offers a simple note-taking system. I'll keep it simple here, but I recommend to read the book if you're interested.

## Capture

- Capture what resonates with you
- Find the right tools to do it quickly and efficiently

The important part of capturing is that it has to be **fast and painless**. You don't triage during the capture process. You just capture to an `Inbox` folder and move on.

It works because it lets you stay in the flow. When you see a cool social media post, article, or get important information from an email, just capture it and continue what you were doing. Don't interrupt your train of thought.

## Organize

When you have some time, organize the notes that were in your `Inbox` folder. Tiago Forte offers a simple system with 4 folders, based on **actionability** of the information.

### PARA

- Projects
  - What you're working on right now, 5~10 folders for most people
- Area of responsibility
  - Things that have direct impact on your day-to-day life, for example health and relationships
- Resources
  - Things that are long-term information relevant to your interests
- Archive
  - Finished projects and obsolete resources

In each of those 4 folders, create a folder per subject. And that should be enough. You don't need more granularity as modern note taking tools have powerful search, tagging, and link systems. With that, you'll find the information you need quickly and efficiently.

## Distill

Once your notes have been captured and organized, it's time to improve them. Tiago Forte advocates for an iterative process. This was a natural step for me with paper notes, but something I never really did with digital notes. As my systems were messy, I ended up with many mis-categorized notes that I simply never checked again.

So every time you go back to a note, make it better. This can be bolding the important points, highlighting the crucial information, adding a TL;DR, or updating information. But every time you access a note, improve it.

This is how you get your thinking to be clearer. This is how you remember what matters. This is how you make your notes useful at a glance.

## Express

Then finally, the last step is to make use of that information to produce new information. New notes recapitulating a recent book, ready-to-use paragraphs, ...

This is the hardest part to put in a blog post as that's literally half the book, so if you're stuck at the expression step, give it a read!

# Trying to make Notion work

In his book, Tiago Forte insists that the note-taking software is just a means to an end and that there's no right or wrong tool. The right tool is the one you'll enjoy using.

As I was used to Notion, I tried to adapt it to this new workflow. And by over-engineering it, I broke everything.

You see, Notion databases are simply lists of notes. And notes in databases can hold any number of child notes. But those notes don't appear in the sidebar, and they're not easy to find in pages as they're just there as references. Search is the only way you'll ever see those notes living inside database rows.

And database are very inflexible. They can have relationships to other database rows, but not to pages. If you try to move a row from a database into a normal page, it's buggy as hell and you can't `ctrl+z` if you made a mistake. If you want to switch from a database to a list of pages, god help you.

![Notion](https://i.imgur.com/162EPKD.png)

I ended up almost destroying my last 18 months of notes because I was trying to put some structure on it. Add to that all of my previous pet peeves and I finally got the motivation to give Obsidian a real try.

# Obsidian

Obsidian promised me *almost* everything I wanted:

- Offline-first, meaning I could always capture what I wanted quickly
- Heavily customizable through plugins
- Formatting I am used to through writing docs in markdown for years

But being customizable is both a blessing and a curse. It means that while you *can* find solutions to do exactly what you want, you *need* to find it. Obsidian without plugins is almost unusable.

You know, I love plugins. Emacs, Neovim, and VS Code all use plugins perfectly. But they're open source dev tools and the few plugins there are usually well maintained.

While in Obsidian those plugins are small open source projects, sometimes not updated and not ready to react to breaking changes from Obsidian, and conflicting with each other. Not to mention that Obsidian itself is **not** open source, which really irks me when it relies so much on open source plugins to be functional.

But I pressed on and made Obsidian pretty much exactly what I had in mind:

![Obsidian](https://i.imgur.com/fEaxJxZ.png)

It mostly worked. This took me two days, but I got to a point I was happy with. It included:

- The `Obsidian Nord` theme
- Quick notes creation with [`QuickAdd`](https://quickadd.obsidian.guide/docs/)
- Better filesystem navigation with [`Quick Explorer`](https://github.com/pjeby/quick-explorer)
- Better fuzzy search with [`omnisearch`](https://github.com/scambier/obsidian-omnisearch)
  - It still kinda sucks though
- [`Make.MD`](https://make.md/) for better looking linked notes
- [`outliner`](https://github.com/vslinko/obsidian-outliner) for better lists handling
- [`jump to link`](https://github.com/mrjackphil/obsidian-jump-to-link) for quick keyboard-driven navigation
  - It's bugged at the moment though
- And of course `kanban` and `dataview` as they're main draws to Obsidian imo, as well as a few UX-related ones like custom folders ordering and folder icons

Despite that, I longed to go back to Notion, because:

- Sync is a pain
  - Synchronization via iCloud is *very* flaky
    - Start sometimes took 30+ seconds
    - At some point I wasn't even able to create a new note
  - Synchronization via git is a massive pain on iOS
  - Their proprietary sync solution is nice but expensive for what it is
- The customization process was long, painful, and still faulty after ~20 hours spent on it
  - I just want [`lazygit`](https://github.com/jesseduffield/lazygit) for notes tbh
- I don't really trust the project
  - I feel like they are taking advantage of open source developers
  - It's a very small team with very low funding, I'm not sure how long it'll survive
- Many small things
  - Can't drag to select files in the explorer
  - Sometimes deleting a note takes 5s and freezes the whole interface
  - Overall lack of polish
  - UX is really awful by default

# Other solutions

## Dendron

I gave [Dendron](https://wiki.dendron.so/) a quick shot but it was just too dev-focused. I want to be able to save links and thoughts quickly on my iPhone.

## Loqseq

Seemingly the perfect fit for me:

- Open source
- Properly keyboard-driven
- Built-in support for tasks and data views

But I couldn't get past the first wall

- *Everything* is a list
- Your only way of organizing is through links, tags, and properties
  - No folders, kind of a no-go for the [PARA](### PARA) system
- Even worse sync integration than Obsidian
  - Sync issues crashed the app twice in 20 minutes for me

## OneNote

Looking around, Microsoft OneNote seemed like a decent option. Support for all types of notes, good track record, loved everywhere.

What turned me off was the weird notebook/pages system. The whole point to digitalize is to make a *better* system for sorting and finding information!

Also I didn't really like the look and feel. Pass.

## The return of Evernote

At this point I realized that I ditched Evernote almost a decade ago for no good reason so I fired it up again.

And it looked decent **but**:

- I don't like the tasks view as a list. I want a board for easy prioritization
- Notebooks? Stacks? What even are those? Just give me folders and stop reinventing the wheel
- Editor is a bit *too* WYSIWYG for me, I like my markdown or at least markdown-like syntax
- Keyboard shortcuts look to be few and far between
  - I only tried the web app so maybe this one's on me but still, nothing pops up on hovers...

Overall, it looks like it's made for longer notes and clipping more than it is to write quick notes and make links.

# Notes apps pros and cons

So here I am. I wasted almost a week trying every single app instead of continuing to hone my Rust skills. And I'm still not sure which app I want to use.

So let's structure all the info in a very biased table:

| App      | Sync | Offline | Speed | Boards | Mobile | Queries | Links | Trust | Style | ⌨️  | Team |
| -------- | ---- | ------- | ----- | ------ | ------ | ------- | ----- |:----- | ----- | --- | ---- |
| Obsidian | ✔️   | ✅      | ✔️    | ✅     | ✅     | ✅      | ✅    | ❌    | ✅    | ✅  |❌      |
| Notion   | ✅   | ❌      | ❌    | ✅     | ✅     | ✅      | ❌    | ✅    | ✅    | ✔️  |✅      |
| Dendron  | ❌   | ✅      | ✅    | ❌     | ❌     | ❌      | ✅    | ✔️    | ✔️    | ✅  |❌      |
| Loqseq   | ❌   | ✅      | ✅    | ❌     | ✅     | ✅      | ✅    | ✅    | ✔️    | ✅  |❌      |
| OneNote  | ✅   | ✅      | ✔️    | ❌     | ✅     | ❌      | ❌    | ✅    | ❌    | ❌  |✅      |
| EverNote | ✅   | ✅      | ✔️    | ❌     | ❌     | ❌      | ❌    | ✅    | ✔️    | ❌  |✅      |

# Conclusion

In conclusion, the search for the perfect note-taking tool is a treacherous journey, a perilous quest through a landscape filled with pitfalls and dangers at every turn. Don't be afraid to take risks, dear reader. Embrace the unknown and let your heart guide you on this perilous journey. The reward of finding the right tool for you will be worth any danger you may encounter along the way.

I will decide on my weapon of choice as the sun rises tomorrow. Wish me luck.

## AI-generated summary

(Useful to save as a Note 👀)

The article describes the author's journey in finding the right note-taking tool for their needs, starting with binders and Evernote and eventually settling on Notion. However, the author eventually becomes frustrated with Notion's clunkiness and reliance on an internet connection, leading them to explore alternative options such as Obsidian and LoqSeq. The article concludes by emphasizing the importance of finding the right tool for one's specific needs and the value in taking the time to explore different options.
