#!/usr/bin/env python3
import json
import datetime
import os

# File that stores puzzle metadata
JSON_FILE = "puzzles.json"


def load_puzzles():
    """Load the puzzles from the JSON file, or return an empty list if the file does not exist."""
    if os.path.exists(JSON_FILE):
        with open(JSON_FILE, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError as e:
                print(f"Error reading {JSON_FILE}: {e}")
                exit(1)
    return []


def get_next_date(puzzles):
    """Determine the next puzzle date by finding the maximum date in the puzzles list and adding one day.
    If no puzzles exist, default to today's date."""
    if puzzles:
        max_date = None
        for p in puzzles:
            try:
                d = datetime.datetime.strptime(p["date"], "%Y-%m-%d").date()
            except (KeyError, ValueError):
                continue
            if max_date is None or d > max_date:
                max_date = d
        if max_date:
            return max_date + datetime.timedelta(days=1)
    return datetime.date.today()


def prompt_for_data():
    """Prompt the user for the required puzzle data."""
    share_link = input("Enter the crossword share link: ").strip()
    while not share_link:
        share_link = input(
            "Share link is required. Enter the crossword share link: "
        ).strip()

    title = input("Enter the title of the puzzle: ").strip()
    while not title:
        title = input("Title is required. Enter the title of the puzzle: ").strip()

    notes = input("Enter any notes (optional. press enter to skip): ").strip()
    return share_link, title, notes


def generate_html(share_link):
    """Generate the HTML content for the puzzle with the given share link."""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Embedded Crossword</title>
  <style>
    body, html {{
      margin: 0;
      padding: 0;
      height: 100%;
    }}
    iframe {{
      width: 100%;
      height: 90vh;
      border: none;
    }}
  </style>
</head>
<body>
  <iframe 
    src="{share_link}"
    frameborder="0" 
    allowfullscreen="true" 
    allowtransparency="true" 
    allow="clipboard-write *">
  </iframe>
</body>
</html>
"""


def save_puzzles(puzzles):
    """Write the updated puzzles list to the JSON file with pretty formatting."""
    with open(JSON_FILE, "w") as f:
        json.dump(puzzles, f, indent=2)


def main():
    puzzles = load_puzzles()
    new_index = len(
        puzzles
    )  # Use current count to generate filename, e.g. puzzle3.html if there are 3 puzzles already.
    next_date = get_next_date(puzzles)

    share_link, title, notes = prompt_for_data()
    filename = f"puzzle{new_index}.html"

    # Create a new puzzle data entry
    new_puzzle = {
        "title": title,
        "filename": filename,
        "date": next_date.strftime("%Y-%m-%d"),
        "iframe": share_link,
        "notes": notes,
    }

    puzzles.insert(0, new_puzzle)
    save_puzzles(puzzles)

    # Generate new HTML content and write to file.
    html_content = generate_html(share_link)
    with open(filename, "w") as f:
        f.write(html_content)

    print("Puzzle published successfully!")
    print(f"New puzzle entry: {new_puzzle}")


if __name__ == "__main__":
    main()
