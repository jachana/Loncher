Arcade Launcher La Resistencia

En memoria de Ricardo Aldana Rameau (1993-2014).

Autores:
-Ricardo Aldana
-Julio Chaná
-Vicente Errázuriz
-Jurgen Heysen

Proyecto iniciado por La Resistencia y enmarcado en IPre, a cargo del prof. Raúl Montes.

El código fuente de este proyecto puede ser utilizado con fines no comerciales, y siempre dando cuenta de los créditos. Adicionalmente puede avisar a los autores sobre su proyecto.
Para fines comerciales, enviar un mail a jdheysen@uc.cl para negociar los derechos.

Dependencias:
El software ha sido elaborado con Python 2.7.5 y es compatible con todas las versiones de Python 2.7, adicionalmente depende de:
-Pygame 1.9.6
-Pillow 2.2.2

Las versiones indicadas son las utilizadas al momento del desarrollo, es posible que otras versiones funcionen pero no se garantiza.
El software no es compatible con Python 3.x y superiores.

Scripts principales:
El script de inicio es launcher_main.py que sin parámetros iniciará la GUI normal. el parámetro -C iniciará el modo Consola
El script game_install.py puede ser usado para administrar los juegos instalados, debe ser utilizado desde consola.

Algunos parámetros pueden ser especificados en el archivo ArcadeConfig.xml dentro del directorio config.

Información sobre cambios respecto a versiones anteriores se encuentra en CHANGELOG.txt

Interfaz gráfica puede ser utilizada tanto con Teclado como con Joystick, con teclado se selecciona un juego con las flechas y con enter se inicia su ejecución. Utilizando joystick el movimiento de cualquier eje o hat cambia la selección y la pulsación de cualquier botón inicia la ejecución del juego.

El juego Demo que viene incluido es simplemente una demostración sobre cómo hacer un juego e integrarlo con el software, si bien es un pequeño juego que puede interesar a jugadores, no se garantiza que esté libre de errores.