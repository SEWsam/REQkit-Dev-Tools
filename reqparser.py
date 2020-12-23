import sys
import time
import json
from json import JSONDecodeError

import requests
import click

from halo import Halo
from colorama import Fore, Style, init

init(convert=True)
mdot = u'\u00b7'
success = f"[{Fore.GREEN}+{Style.RESET_ALL}]"
failure = f"[{Fore.RED}-{Style.RESET_ALL}]"


def setup(id_file, out_file, headers):
    try:
        spinner.start("Loading ID File...")
        time.sleep(.5)
        with open(id_file) as f:
            ids = []
            for i in f:
                ids.append(i.strip())
        spinner.stop_and_persist(success, "ID File Loaded!")
    except FileNotFoundError:
        spinner.stop_and_persist(failure, "Invalid ID File Path. Exiting in 2 seconds.")
        time.sleep(2)
        sys.exit()

    spinner.start("Verifying API Key...")
    test = requests.get(
        "https://www.haloapi.com/metadata/h5/metadata/requisition-packs/5f96269a-58f8-473e-9897-42a4deb1bf09",
        headers=headers
    )
    if test.status_code == 401:
        spinner.stop_and_persist(failure, "Invalid API Key / 401 Unauthorized. Exiting in 2 seconds")
        time.sleep(2)
        sys.exit()
    else:
        spinner.stop_and_persist(success, "API Key Valid!")

    spinner.start("Creating output files")
    try:
        with open(out_file, "x") as f:
            base = []
            f.write(json.dumps(base))
    except FileExistsError:
        pass
    spinner.stop_and_persist(success, "Output files created!")

    return ids


def gather_data(ids, out_file, typ, headers):
    for i in ids:
        spinner.start(f"Getting metadata for Pack: '{i}'")
        try:
            metadata = requests.get(
                f"https://www.haloapi.com/metadata/h5/metadata/{typ}/{i}",
                headers=headers
            ).json()
            name = metadata["name"]
            if typ == "requisitions":
                price = metadata["sellPrice"]
            else:
                price = metadata["creditPrice"]

            if typ == "requisition-packs":
                entry = [
                    f"A {name}",
                    f"{price:,}",
                    f"RequisitionPackId={i}&ExpectedPrice={price}&__RequestVerificationToken="
                ]

                if metadata["isPurchasableWithCredits"]:
                    pass
                else:
                    raise JSONDecodeError
            else:
                entry = [
                    f"{name}",
                    f"{price:,}",
                    f"RequisitionId={i}&ExpectedSellPrice={price}&__RequestVerificationToken="
                ]

            with open(out_file) as f:
                file = json.load(f)

            with open(out_file, "w") as f:
                file.append(entry)
                f.write(json.dumps(file, indent=4))

            time.sleep(1)
            spinner.stop_and_persist(success, f"Obtained metadata for REQ: '{i}'")
        except JSONDecodeError:
            time.sleep(1)
            spinner.stop_and_persist(failure, f"Couldn't obtain metadata for REQ: '{i}'")


@click.command()
@click.argument('typ', metavar="<Type:'req'|'pack'>")
@click.argument('id-file', metavar="<ID File Location>")
@click.argument('out-file', metavar="<Output File>")
@click.option(
    "--api-key", "-k", metavar="string",
    help="Your Halo 5 Public API Key"
)
def main(id_file, out_file, typ, api_key):
    if typ == "pack":
        typ = "requisition-packs"
    elif typ == "req":
        typ = "requisitions"
    else:
        print(failure, "Invalid REQ type. Please enter 'req' or 'pack'")

    headers = {
        'Ocp-Apim-Subscription-Key': f'{api_key}'
    }
    ids = setup(id_file, out_file, headers)
    print(f"[{mdot}] Gathering metadata! \n")
    gather_data(ids, out_file, typ, headers)


if __name__ == '__main__':
    spinner = Halo()
    print(f"{Fore.CYAN}REQParser Version 2.0{Style.RESET_ALL}")
    print(
        f"{Fore.GREEN}A tool for batch compiling REQkit database entries from REQ-ids"
        f"{Style.RESET_ALL}\n"
    )
    main()
