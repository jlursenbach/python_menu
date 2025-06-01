#!/usr/bin/env python3
# Jacob Ursenbach
# 2022-07-21
# jlursenbach@csu.fullerton.edu
# @jlursenbach
#
#

"""
A default menu class
Allows menu items to be set and called
provides string for header etc
functions can have parameters
"""


# menu.py

from typing import Callable, Dict, List, Optional
from collections import OrderedDict


class EscapeCommand:
    def __init__(self, name: str, handler: Callable[[List[str]], None], description: str):
        self.name = name
        self.handler = handler
        self.description = description


class EscapeManager:
    """
    Central registry for escape commands. Uses a configurable prefix (default "./").
    """
    def __init__(self, prefix: str = "./"):
        self.prefix = prefix
        self._commands: Dict[str, EscapeCommand] = {}

    def register(self, cmd: EscapeCommand):
        self._commands[cmd.name] = cmd

    def dispatch(self, raw_input: str) -> bool:
        parts = raw_input.split(maxsplit=1)
        cmd_name = parts[0]
        if cmd_name in self._commands:
            args = parts[1].split() if len(parts) > 1 else []
            self._commands[cmd_name].handler(args)
            return True
        print(f"❓ Unrecognized command '{cmd_name}'. Type '{self.prefix}help' for valid commands.")
        return True


class MenuItem:
    def __init__(
        self,
        key: str,
        description: str,
        handler: Callable[[], None],
        group: Optional[str] = None,
        enabled: bool = True
    ):
        self.key = key.upper()
        self.description = description
        self.handler = handler
        self.group = group
        self.enabled = enabled


class Menu:
    """
    Generic CLI menu with customizable escape‐prefix. 
    """
    class ExitMenu(Exception):
        pass

    def __init__(
        self,
        title: str,
        prompt: str = "Select an option:",
        parent: Optional["Menu"] = None,
        escape_prefix: str = "./"
    ):
        self.title = title
        self.prompt = prompt
        self.parent = parent
        self.items: "OrderedDict[str, MenuItem]" = OrderedDict()
        self.escape_mgr = EscapeManager(prefix=escape_prefix)
        self._register_default_escape_commands()

    def _register_default_escape_commands(self):
        p = self.escape_mgr.prefix
        self.escape_mgr.register(
            EscapeCommand(f"{p}help", self._cmd_help, "Show list of escape commands.")
        )
        self.escape_mgr.register(
            EscapeCommand(f"{p}exit", self._cmd_exit, "Exit current menu (return to parent).")
        )
        self.escape_mgr.register(
            EscapeCommand(f"{p}quit", self._cmd_exit, "Alias for exit.")
        )
        self.escape_mgr.register(
            EscapeCommand(f"{p}disable", self._cmd_disable, "Disable a menu item: '{p}disable <KEY>'.")
        )
        self.escape_mgr.register(
            EscapeCommand(f"{p}enable", self._cmd_enable, "Enable a menu item: '{p}enable <KEY>'.")
        )
        self.escape_mgr.register(
            EscapeCommand(f"{p}list", self._cmd_list, "List menu items and status.")
        )

    def register_escape(self, name: str, handler: Callable[[List[str]], None], description: str):
        self.escape_mgr.register(EscapeCommand(name, handler, description))

    def _cmd_help(self, args: List[str]):
        print("\n=== Escape Commands ===")
        for cmd in self.escape_mgr._commands.values():
            print(f"  {cmd.name:<12} — {cmd.description}")
        print()

    def _cmd_exit(self, args: List[str]):
        raise Menu.ExitMenu

    def _cmd_disable(self, args: List[str]):
        if not args:
            print(f"❗ Usage: {self.escape_mgr.prefix}disable <KEY>")
            return
        key = args[0].upper()
        if key in self.items:
            item = self.items[key]
            if not item.enabled:
                print(f"⚠️ '{key}' already disabled.")
            else:
                item.enabled = False
                print(f"✅ Disabled '{key}'.")
        else:
            print(f"❗ No menu item '{key}'.")

    def _cmd_enable(self, args: List[str]):
        if not args:
            print(f"❗ Usage: {self.escape_mgr.prefix}enable <KEY>")
            return
        key = args[0].upper()
        if key in self.items:
            item = self.items[key]
            if item.enabled:
                print(f"⚠️ '{key}' already enabled.")
            else:
                item.enabled = True
                print(f"✅ Enabled '{key}'.")
        else:
            print(f"❗ No menu item '{key}'.")

    def _cmd_list(self, args: List[str]):
        print("\n=== Menu Items ===")
        current_group = None
        for item in self.items.values():
            if item.group != current_group:
                current_group = item.group
                if current_group:
                    print(f"\n-- {current_group} --")
            status = "(Disabled)" if not item.enabled else ""
            print(f"  [{item.key}] {item.description} {status}")
        print()

    def add_item(
        self,
        key: str,
        description: str,
        handler: Callable[[], None],
        group: Optional[str] = None,
        enabled: bool = True
    ):
        item = MenuItem(key, description, handler, group=group, enabled=enabled)
        self.items[item.key] = item

    def add_submenu(self, key: str, description: str, submenu: "Menu", group: Optional[str] = None):
        submenu.parent = self
        def _enter_submenu():
            try:
                submenu.run()
            except Menu.ExitMenu:
                return
        self.add_item(key, description, _enter_submenu, group=group)

    def set_enabled(self, key: str, enabled: bool):
        key = key.upper()
        if key in self.items:
            self.items[key].enabled = enabled

    def _breadcrumb(self) -> str:
        if self.parent:
            return f"{self.parent._breadcrumb()} > {self.title}"
        return self.title

    def read_input(self, prompt: str) -> str:
        raw = input(prompt).strip()
        if raw.startswith(self.escape_mgr.prefix):
            handled = self.escape_mgr.dispatch(raw)
            if handled:
                return self.read_input(prompt)
        return raw

    def _print_menu(self):
        print("\n" + "=" * 50)
        print(f"  {self._breadcrumb()}")
        print("=" * 50)
        current_group = None
        for item in self.items.values():
            if item.group != current_group:
                current_group = item.group
                if current_group:
                    print(f"\n-- {current_group} --")
            prefix = "[ ]" if not item.enabled else f"[{item.key}]"
            print(f"  {prefix} {item.description}")
        print("=" * 50)

    def run(self):
        while True:
            try:
                self._print_menu()
                choice = self.read_input(f"{self.prompt} ").upper()
                if choice in self.items:
                    item = self.items[choice]
                    if not item.enabled:
                        print(f"❗ Option '{choice}' is disabled.")
                        continue
                    item.handler()
                else:
                    print(f"❗ Invalid choice: '{choice}'. Type '{self.escape_mgr.prefix}help' or select a valid key.")
            except Menu.ExitMenu:
                return


if __name__ == '__main__':
    pass
