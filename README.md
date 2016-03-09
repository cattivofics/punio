# punio

## requirements:

- get the proper version of [pywin32](https://sourceforge.net/projects/pywin32/files/pywin32/)
- install [python](https://www.python.org/downloads/) (recommended 3.4.4), and add it to the PATH variable

## supported operative systems
- Win 8, XP (probably others, but we did not test them yet, give us your feedback!)

## how it works
punio connects with your DGT via USB or Serial ports, detects which square gets updated every time a piece is removed
or dropped and send clicks to the screen. In order to work punio needs the app currently running your game 
(the browser) always on top, and the hosting application should allow the make of moves by clicks.

## how to use it
- make sure the DGT board is connected and the driver not started (we don't want to use the original softeware from DGT)
- open your favourite chess website and open a chessboard (make sure this will be the final layout, don't change 
the location of the window when all is set), use an analysis board the first time
- open the windows command prompt
- navigate to punio's folder and run it typing "python punio.py"
- click on "New board layout", the app will get transparent and you should see the chessboard behind it
- draw a rectangle around the a8 square (make sure the white pieces are at the bottom)
- a grid will be generated, if all the squares are covered you can click on "Done" in the top-middle part of the screen
otherwise click on "Undo" and repeat until all the squares gets properly covered by the new grid
- click on "Save Current Layout" and give it a name, otherwise you have to repeat this tedious process every time
- click on "Test Click Squares" to verify the clicks will reach the proper squares
- enter your DGT port name and click "Save"
- click on "Start" to initialize the port communication
- bring the browser with your chessboard on top and remove a piece, you should see a new message on the status bar 
(Trying to click "something") and the piece selected in the chess website.

## Instructions in other Languages
- [Spanish (Español)] (https://github.com/Boniato82/punio/blob/master/README_ES.md)
