"""
colors.py - Colored terminal output example using Colorama.
"""

from colorama import Fore, Style, init

init(autoreset=True)


def display_colors():
    print(Fore.RED + "🔴 Error / Critical Warning" + Style.RESET_ALL)
    print(Fore.GREEN + "🟢 Success / Task Complete" + Style.RESET_ALL)
    print(Fore.BLUE + "🔵 Information / Progress" + Style.RESET_ALL)
    print(Fore.YELLOW + "🟡 Notice / Attention Required" + Style.RESET_ALL)


if __name__ == "__main__":
    display_colors()
