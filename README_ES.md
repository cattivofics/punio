# Spanish instructions (Instrucciones en Español)

## Instrucciones en otros idiomas

- [Inglés (English)] (https://github.com/Boniato82/punio/blob/master/README.md)

## requisitos técnicos:

- Obten la versión más actualizada de pywin32
- instala python (recommendado 3.4.4), y añádelo a la variable PATH

## sistemas operativos soportados

- Win 8, XP (probablemente más, ¡pruébalos y danos tu opinion!)

## cómo funciona

- punio conecta con tu tablero digital DGT via USB o puerto Serie, detecta cual casilla es actualizada cada vez que una pieza es eliminada o levantada del tablero, y envía un "click" a la pantalla. Para que punio funcione necesita que la aplicación en la que se ejecuta el juego (el navegador) esté siempre encima del resto de ventanas del sistema, y la aplicación que usemos permita el uso de movimientos por clicks de ratón. 

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
- Pulsa en "Start" para iniciar la comunicación con el puerto.
- Mantén el navegador con tu tablero en primer plano y quita/mueve una pieza, deberías ver un nuevo mensaje en la barra de estado (Intentando pulsar "algo/something") y la pieza seleccionada en tablero de la web en la que estés.
