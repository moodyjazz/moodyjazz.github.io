# moodyjazz.github.io

Source code for <https://moodyjazz.github.io/>

## Publishing Crosswords

Python is needed as a prerequisite.

Clone the repository locally using
```
git clone git@github.com:moodyjazz/moodyjazz.github.io.git
```
To run the script:

```
python publish.py
```

It will prompt you then for the crossword information. 

The script will then update the local repo with the updated puzzles.json and the new puzzle.html

To push the changes to remote repository:
```
git add .
git commit "Add next puzzle"
git push origin main
```
