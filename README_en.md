## Introduction
There is already Notero that implements the synchronization of literature entry data and notes from Zotero to Notion. Unfortunately, this repository cannot sync notes from Zotero to other software compatible with Markdown syntax, nor can it implement the backlink feature for notes (jumping from notes back to specific locations in Zotero entries or even annotations in PDFs).

The purpose of this repository is to enable the copying of notes from Zotero to other software compatible with Markdown syntax, with the capability to jump back to specific locations in Zotero, thus implementing the backlink feature for notes.



## Installation of Compiled Version
Download the corresponding version's compressed package, unzip it, and double-click Link2Zotero.exe to run.

## Manual Compilation Method
```bash
cd path/to/Link2Zotero
pyinstaller --onefile --icon=Link2Zotero_2.ico --noconsole .\CopyReplace\main.py
```


## Usage Instructions
After running Link2Zotero.exe, the program will automatically monitor the clipboard. When it detects that a Zotero note has been copied, it will automatically update the text to include global jump functionality (a notification will appear in the bottom right corner indicating the number of jumpable links). Simply paste the text into your notes. Notes are supported in software such as Notion, Typora, Obsidian, and other Markdown-compatible applications.

## References