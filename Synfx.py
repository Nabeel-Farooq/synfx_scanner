import asyncio
import aiohttp
import argparse
import sys
from colorama import init, Fore, Style

# Initialize colorama for cross-platform colored output
init(autoreset=True)

# Snyfx Site Database
# Add new sites here. The '{}' is where the username will be injected.
SITES = {
    "GitHub": "https://github.com/{}",
    "Twitter/X": "https://twitter.com/{}",
    "Instagram": "https://www.instagram.com/{}/",
    "Reddit": "https://www.reddit.com/user/{}",
    "HackerNews": "https://news.ycombinator.com/user?id={}",
    "Pinterest": "https://www.pinterest.com/{}/",
    "Twitch": "https://www.twitch.tv/{}",
    "Vimeo": "https://vimeo.com/{}",
    "SoundCloud": "https://soundcloud.com/{}",
    "Linktree": "https://linktr.ee/{}"
}

# Standard User-Agent to prevent basic bot-blocking
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
}

async def check_username(session, site_name, url_template, username):
    """Asynchronously checks a single URL for the username."""
    url = url_template.format(username)
    try:
        # We allow redirects, but some sites return 200 for missing users.
        # Advanced OSINT tools check page content to avoid false positives.
        async with session.get(url, headers=HEADERS, timeout=10, allow_redirects=True) as response:
            if response.status == 200:
                print(f"{Fore.GREEN}[+] {site_name}: {url}{Style.RESET_ALL}")
            elif response.status == 404:
                # User not found
                pass
            else:
                # Other status codes (e.g., 403 Forbidden, 429 Too Many Requests)
                print(f"{Fore.YELLOW}[?] {site_name}: {url} (HTTP {response.status}){Style.RESET_ALL}")
    
    except asyncio.TimeoutError:
        print(f"{Fore.RED}[-] {site_name}: Connection Timed Out{Style.RESET_ALL}")
    except aiohttp.ClientError:
        pass # Silently ignore connection drops to keep output clean

async def main(username):
    print(f"{Fore.CYAN}=========================================={Style.RESET_ALL}")
    print(f"{Fore.CYAN}       SNYFX - OSINT Username Hunter      {Style.RESET_ALL}")
    print(f"{Fore.CYAN}=========================================={Style.RESET_ALL}")
    print(f"[*] Hunting down footprint for: {Fore.CYAN}{username}{Style.RESET_ALL}\n")
    
    # Create an asynchronous HTTP session
    async with aiohttp.ClientSession() as session:
        tasks = []
        # Create a task for every site in our database
        for site_name, url_template in SITES.items():
            task = asyncio.create_task(check_username(session, site_name, url_template, username))
            tasks.append(task)
        
        # Run all tasks concurrently
        await asyncio.gather(*tasks)
        
    print(f"\n{Fore.CYAN}[*] Scan complete.{Style.RESET_ALL}")

if __name__ == "__main__":
    # Set up command-line arguments
    parser = argparse.ArgumentParser(description="Snyfx - A fast, asynchronous OSINT username checker.")
    parser.add_argument("username", help="The username to search for across platforms.")
    args = parser.parse_args()

    # Handle Windows specific async loop issue gracefully
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    try:
        asyncio.run(main(args.username))
    except KeyboardInterrupt:
        print(f"\n{Fore.RED}[!] Scan interrupted by user. Exiting...{Style.RESET_ALL}")
