# Snyfx 🕵️‍♂️

**Snyfx** is a lightning-fast, lightweight OSINT tool for hunting down usernames across the web.

Think of it as a streamlined, DIY alternative to Sherlock. It uses asynchronous Python to ping multiple social media sites, developer platforms, and forums simultaneously—telling you exactly where a specific username exists in seconds.

---

## ✨ Why use Snyfx?

- ⚡ **Fast**  
  Built with `aiohttp` and `asyncio`, so it checks dozens of sites at the same time rather than one by one.

- 🪶 **Lightweight**  
  No bloated dependencies. Just plug in a username and get your results.

- 🛠️ **Easy to tweak**  
  The code is simple by design. Want to add a new site to check? Just drop the URL into the dictionary.

---

## 🛠️ Installation

You only need a couple of standard libraries to get this running.

Open your terminal and install them:

```bash
pip install aiohttp colorama
