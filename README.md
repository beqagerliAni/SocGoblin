# Social Agent

Hi! I'm building this on my own for fun, and it's still a side project. It's a little tool that lets me peek at what other companies are posting on social media, without spending my evenings scrolling through their feeds. 📱☕

## Why I started it

Every time I wanted to know what a companies was up to, I'd open their page, scroll, forget what I'd seen, and end up with scattered notes. I figured a small app could do the boring part.

## 🎮 What it can do (so far, in my head)

- **Recap the last 30 days.** Type a company and get the themes, launches, and promos, with links to the posts it's based on. 🔗
- **Read the comments for me.** What people praise, complain about, and ask. I'm not interested in who wrote them, just what they said. 
- **Answer my questions.** Ask something like "what did they say about pricing?" and get an answer from the posts and comments it has collected. If the answer's not there, it'll say so. 🙃
- **Find stuff fast.** Search by words, hashtags, company, or date. 🔍
- **Check before it guesses.** Describe a company, pick the right one from the list, then let it run. 🎯

🧪 Where it is

Still an experiment, and most of it isn’t built yet. Here’s where things stand:

- 🔎 Search works from a plain prompt. A question looks across TikTok, Facebook, and Instagram, and fetches up to 100 posts per run.
- 🧠 Two AI tools are wired in. Jev and OpenAI are both set up, using Jev for sorting, filtering and openAI for analyzeing user request
- ✅ Done so far: fetching posts, normalizing them, the Facebook fetch, the filters, and saving collected posts.
- 🛠️ In progress: checking the AI prompts and search quality.
