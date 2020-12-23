import json

from halo import Halo
from colorama import Fore, Style, init

init(convert=True)
mdot = u'\u00b7'
success = f"[{Fore.GREEN}+{Style.RESET_ALL}]"
failure = f"[{Fore.RED}-{Style.RESET_ALL}]"


def output(ids):
    with open("ids.txt", "w") as f:
        for i in ids:
            f.write(i + "\n")


def url_parse(urls):
    ids = []
    for url in urls:
        url = url.replace("https://image.halocdn.com/h5/requisitions/", "")
        url = url.split("?locale")
        ids.append(url[0])

    return ids


def har_parse(entries):
    urls = []
    for entry in entries:
        url = (entry["request"])["url"]
        if "image.halocdn" in url:
            urls.append(url)

    return urls


def main():
    with open("halo.har") as f:
        har = json.load(f)

    entries = (har["log"])["entries"]
    urls = har_parse(entries)
    ids = url_parse(urls)
    output(ids)


if __name__ == '__main__':
    spinner = Halo()
    print(f"{Fore.CYAN}REQ HAR Parser Version 1.0{Style.RESET_ALL}")
    print(
        f"{Fore.GREEN}A (repurposable) tool for compiling REQ ids from halowaypoint exported HAR files."
        f"{Style.RESET_ALL}\n"
    )
    main()
