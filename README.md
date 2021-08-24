# Messenger Visualizer

This project visualizes Facebook Messenger data.
I also experiment with TDD, frameworks like `nltk`, and whatever else is interesting when I spend time on this project.

## Quick Start

Run the program with: `python src/Main.py -i test/Messages/conversation_skeleton.json -o out/ -w util/100_Common_English.txt`
- `-i` - Input file, this is `.json` sourced from Facebook Messenger.
- `-o` - Output directory for artifacts.
- `-w` - A wordlist of terms to ignore, if desired.

## Project Structure

`src` contains:
- `Conversation.py` - An exchange between two or more participants, this class manages instances of the `Message` class and keeps track of running totals about the conversation history.
- `FileIO.py` - This project uses `.json` and `.txt` files. This file defines a common way to do that in the context of this project (and maybe re-invents the wheel).
- `Main.py` - Given input files as arguments, generate graphs and text logs. Mostly an imperative set of instructions that leverages `FileIO`, `Conversation`, and `Visualizer`.
- `Message.py` - Represent messages parsed from `.json` as a Python class.
- `Visualizer.py` - Functions that wrap calls to `matplotlib.pyplot`.

`test` contains unit tests and sample `.json` input for use by the test suite. 
Run this locally with: `python -m unittest discover -s MessengerVisualizer/test -t MessengerVisualizer`

`util` contains:
- `100_Common_English.txt` - A wordlist of the 100 most-common english words.
- `Custom_List.txt` - A wordlist with additional words to filter out.
- `ClearDirectory.sh` to delete the contents of `output/` between executions.
- `MessageType.py` - An enum for MessageType that doesn't to much (yet).