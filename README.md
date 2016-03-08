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

# Spanish instructions (Instrucciones en Español)
## requisitos técnicos:

- Obten la versión más actualizada de [pywin32](https://sourceforge.net/projects/pywin32/files/pywin32/)
- instala [python](https://www.python.org/downloads/) (recommendado 3.4.4), y añádelo a la variable PATH

## sistemas operativos soportados
- Win 8, XP (probablemente más, ¡pruébalos y danos tu opinion!)

## cómo funciona
punio conecta con tu tablero digital DGT via USB o puerto Serie, detecta cual casilla es actualizada cada vez que una pieza es eliminada o levantada del tablero, y envía un "click" a la pantalla. Para que punio funcione necesita que la aplicación en la que se ejecuta el juego (el navegador) esté siempre encima del resto de ventanas del sistema, y la aplicación que usemos permita el uso de movimientos por clicks de ratón.

## cómo usarlo.
- Asegúrate de que el tablero DGT está conectado y el driver no se ha iniciado (no queremos usar el software original de DGT)
- Abre tu web de ajedrez preferida y abre un tablero (asegúrate de que ésta será la pantalla y composición final, no cambies la localización de la pantalla después). Usa un tablero de analisis la primera vez. 
- Abre la consola de comandos de windows (cmd)
- Ve a la carpeta donde descargaste punio y ejecutalo teclando "python punio.py" (sin comillas)
- Pulsa en ""New board layout", la aplicación se volverá transparente y tú deberías ver el tablero detrás de ella.
- Dibuja un rectángulo alrededor de la casilla a8 (esquina superior izquierda. Asegúrate de que las piezas blancas están en la parte inferior del tablero).
- Una rejilla será generada. Si todas las casillas son cubiertas puedes pulsar en "Done", en la parte central-arriba de la pantalla. 
- Pulsa en "Save Current Layout" y dale un nombre, de otro modo tendrás que repetir este tedioso proceso cada vez.
- Pulsa en "Test Click Squares" para verificar que los clicks llegan a las casillas correspondientes.
- Introduce el nombre de tu puerto DGT y pulsa "Save"
- Pulsa en "Start" para iniciar la  comunicación con el puerto.
- Mantén el navegador con tu tablero en primer plano y quita/mueve una pieza, deberías ver un nuevo mensaje en la barra de estado (Intentando pulsar "algo/something") y la pieza seleccionada en tablero de la web en la que estés.
