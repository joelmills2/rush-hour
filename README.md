# Simulating Rush Hour for CISC204 Modelling Project

Welcome to rush hour for CISC/CMPE 204!

Rush Hour is a classic logic game that requires the sliding of vehicles across a grid to allow the red vehicle
to escape.

Cells will be numbered in the form (row, column), counting from the top left, which is cell (0,0).

Our model will correspond to the states of every cell. Every cell will have a true proposition representing
the vehicle type that is in that cell. Every cell will also have propositions that will be true if it is the
lead cell in a car that can move (For example, the rightmost cell in a car that can move right).

We will use our model to simulate the game of Rush Hour according to its rules. From that base, we
can then build a playable game.

We hope you enjoy!

Cheers,

 \- Alex, Ethan, Jacob, and Joel

## Structure

* `documents`: Contains folders for both of your draft and final submissions. README.md files are included in both.
* `run.py`: Main code file. Contains all of our propositions, constraints, and gameplay functions.
* `test.py`: Run this file to confirm that your submission has everything required. This essentially just means it will check for the right files and sufficient theory size.
* `boards.py`: This file is called by `run.py` and maintains a list of valid game boards ranging in difficulty.


