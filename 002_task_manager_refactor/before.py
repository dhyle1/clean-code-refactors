#!/usr/bin/env python3

import os
import sys
import json
from datetime import datetime

DATA_FILE = "todo_data.json"

tasks = []
last_loaded_at = None


def _ensure_data_file():
    if not os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "w", encoding="utf-8") as f:
                f.write("[]")
        except Exception as e:
            print("could not create data file:", e)
            sys.exit(1)


def load_data():
    global tasks, last_loaded_at
    _ensure_data_file()
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            content = f.read().strip() or "[]"
            data = json.loads(content)
            if not isinstance(data, list):
                data = []
            tasks = data
            last_loaded_at = datetime.now().isoformat(timespec="seconds")
    except Exception as e:
        print("Failed reading file, resetting. err:", e)
        tasks = []
        last_loaded_at = datetime.now().isoformat(timespec="seconds")


def save_data():
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            f.write(json.dumps(tasks, indent=2, ensure_ascii=False))
    except Exception as e:
        print("Could not save:", e)


def _normalize_priority(p):
    try:
        p = int(p)
    except Exception:
        return 2
    if p < 1:
        return 1
    if p > 3:
        return 3
    return p


def _parse_index(s):
    try:
        return int(s)
    except Exception:
        return None


def _print_task(t, idx):
    title = t.get("title", "")
    done = t.get("done", False)
    pr = t.get("priority", 2)
    due = t.get("due", "")
    tag = t.get("tag", "")
    created = t.get("created_at", "")

    status = "DONE" if done else "TODO"
    print(f"[{idx}] {status} | p{pr} | {title}")
    if due:
        print(f"     due: {due}")
    if tag:
        print(f"     tag: {tag}")
    if created:
        print(f"     created: {created}")


def list_tasks(filter_mode=None, filter_value=None):
    if len(tasks) == 0:
        print("No tasks yet.")
        return

    shown = 0
    for i, t in enumerate(tasks):
        if filter_mode == "tag":
            if (t.get("tag") or "").lower() != (filter_value or "").lower():
                continue
        if filter_mode == "status":
            want_done = (filter_value or "").lower() in ("done", "d", "1", "true", "yes")
            if bool(t.get("done", False)) != want_done:
                continue

        _print_task(t, i)
        shown += 1

    if shown == 0:
        print("No tasks matched that filter.")


def add_task_flow():
    title = input("Title: ").strip()
    if title == "":
        print("Title cannot be empty.")
        return

    pr = input("Priority 1-3 (default 2): ").strip()
    pr = _normalize_priority(pr if pr != "" else 2)

    due = input("Due date (YYYY-MM-DD) optional: ").strip()
    if due != "" and (len(due) != 10 or due[4] != "-" or due[7] != "-"):
        print("Due date format looks wrong; storing as-is anyway...")

    tag = input("Tag optional: ").strip()

    tasks.append(
        {
            "title": title,
            "priority": pr,
            "due": due,
            "tag": tag,
            "done": False,
            "created_at": datetime.now().isoformat(timespec="seconds"),
        }
    )
    save_data()
    print("Added.")


def mark_done_flow():
    if len(tasks) == 0:
        print("No tasks to mark.")
        return
    idx = _parse_index(input("Index to mark done: ").strip())
    if idx is None or idx < 0 or idx >= len(tasks):
        print("Invalid index.")
        return
    tasks[idx]["done"] = True
    save_data()
    print("Marked done.")


def mark_undone_flow():
    if len(tasks) == 0:
        print("No tasks to unmark.")
        return
    idx = _parse_index(input("Index to mark TODO: ").strip())
    if idx is None or idx < 0 or idx >= len(tasks):
        print("Invalid index.")
        return
    tasks[idx]["done"] = False
    save_data()
    print("Marked TODO.")


def delete_task_flow():
    if len(tasks) == 0:
        print("No tasks to delete.")
        return
    idx = _parse_index(input("Index to delete: ").strip())
    if idx is None or idx < 0 or idx >= len(tasks):
        print("Invalid index.")
        return
    removed = tasks.pop(idx)
    save_data()
    print("Deleted:", removed.get("title", ""))


def edit_task_flow():
    if len(tasks) == 0:
        print("No tasks to edit.")
        return
    idx = _parse_index(input("Index to edit: ").strip())
    if idx is None or idx < 0 or idx >= len(tasks):
        print("Invalid index.")
        return

    t = tasks[idx]
    print("Leave blank to keep value.")

    new_title = input(f"Title [{t.get('title','')}]: ").strip()
    if new_title != "":
        t["title"] = new_title

    new_pr = input(f"Priority 1-3 [{t.get('priority',2)}]: ").strip()
    if new_pr != "":
        t["priority"] = _normalize_priority(new_pr)

    new_due = input(f"Due [{t.get('due','')}]: ").strip()
    if new_due != "":
        t["due"] = new_due

    new_tag = input(f"Tag [{t.get('tag','')}]: ").strip()
    if new_tag != "":
        t["tag"] = new_tag

    tasks[idx] = t
    save_data()
    print("Edited.")


def quick_add_from_args(argv):
    if len(argv) < 3:
        print('Usage: add "title" [--p 1-3] [--tag TAG] [--due YYYY-MM-DD]')
        return

    title = argv[2].strip()
    pr = 2
    due = ""
    tag = ""

    i = 3
    while i < len(argv):
        a = argv[i]
        if a in ("--p", "--prio", "--priority") and i + 1 < len(argv):
            pr = _normalize_priority(argv[i + 1])
            i += 2
            continue
        if a == "--due" and i + 1 < len(argv):
            due = argv[i + 1]
            i += 2
            continue
        if a == "--tag" and i + 1 < len(argv):
            tag = argv[i + 1]
            i += 2
            continue
        i += 1

    tasks.append(
        {
            "title": title,
            "priority": pr,
            "due": due,
            "tag": tag,
            "done": False,
            "created_at": datetime.now().isoformat(timespec="seconds"),
        }
    )
    save_data()
    print("Added via args.")


def show_menu():
    print("\n=== ToDo ===")
    print("1) List tasks")
    print("2) Add task")
    print("3) Mark done")
    print("4) Mark TODO")
    print("5) Edit task")
    print("6) Delete task")
    print("7) List by tag")
    print("8) List by status")
    print("9) Reload from disk")
    print("0) Quit")
    if last_loaded_at:
        print("(last loaded:", last_loaded_at + ")")


def main_loop():
    while True:
        show_menu()
        choice = input("> ").strip()

        if choice == "1":
            list_tasks()
        elif choice == "2":
            add_task_flow()
        elif choice == "3":
            mark_done_flow()
        elif choice == "4":
            mark_undone_flow()
        elif choice == "5":
            edit_task_flow()
        elif choice == "6":
            delete_task_flow()
        elif choice == "7":
            tag = input("Tag: ").strip()
            list_tasks(filter_mode="tag", filter_value=tag)
        elif choice == "8":
            st = input("Status (done/todo): ").strip()
            list_tasks(filter_mode="status", filter_value=st)
        elif choice == "9":
            load_data()
            print("Reloaded.")
        elif choice == "0":
            print("bye")
            break
        else:
            print("??")


def main():
    load_data()

    if len(sys.argv) > 1:
        cmd = sys.argv[1].lower().strip()
        if cmd == "add":
            quick_add_from_args(sys.argv)
        elif cmd == "list":
            list_tasks()
        elif cmd == "list-tag":
            if len(sys.argv) >= 3:
                list_tasks(filter_mode="tag", filter_value=sys.argv[2])
            else:
                print("Usage: list-tag TAG")
        elif cmd == "list-status":
            if len(sys.argv) >= 3:
                list_tasks(filter_mode="status", filter_value=sys.argv[2])
            else:
                print("Usage: list-status done|todo")
        else:
            main_loop()
    else:
        main_loop()


if __name__ == "__main__":
    main()
