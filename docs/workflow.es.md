# Del audio al pendrive

## 1. Inspeccionar

Registrá año y firmware, duración, frecuencia y canales del audio. Si también recibís un FSEQ, analizá su cabecera, duración, valores y actividad por canal antes de reutilizar algo. No supongas que dos archivos con el mismo nombre están sincronizados: nuestra referencia tenía 186,08 segundos de FSEQ y unos 51,17 de MP3.

## 2. Analizar el ritmo

Usá herramientas de audio locales, por ejemplo ffmpeg para convertir y bibliotecas de análisis si están disponibles. Registrá dependencias y parámetros. Medí energía por ventanas, ataques y pulsos; inspeccioná si el tempo estimado está al doble o a la mitad. No equipares un detector de beats con comprensión musical garantizada.

Agrupá 8/16/32 pulsos en frases. Compará energía media de frase con cuantiles calculados sobre esas mismas medias. En una versión anterior, usar un umbral de energía instantánea produjo cero acentos delanteros: el código existía, pero la condición nunca se cumplía. Medí la actividad de la salida final para detectar estos casos.

## 3. Componer capas

- Barra central: crescendos en comienzos de frase, olas lentas en partes suaves y respuestas más cortas en estribillos.
- Señaleros: alternancia izquierda/derecha, llamada delante y respuesta atrás, diagonales y acentos conjuntos.
- Laterales blancos: reservar ventanas sin ámbar frontal del mismo lado, para que ambos se distingan.
- Blancos inferiores y luces traseras: apoyar el pulso sin mantener todo encendido.

No hay que copiar todos los movimientos de una secuencia descargada. Este perfil deja las partes móviles apagadas. Cada canal debe tener una sola línea de tiempo; resolver superposiciones antes de exportar. Usá límites temporales con precisión completa y redondeá a frames sólo al escribir: redondear primero a milisegundos puede dejar un frame residual al borrar un efecto.

## 4. Exportar y comprobar

Convertí a WAV PCM 16 bits, 44,1 kHz, conservando la duración. Generá FSEQ según [el perfil](fseq-profile.es.md). Guardá escenas, envolventes y estadísticas: canal, segundos activos, cantidad de encendidos y valores usados.

Ejecutá el validador local y el [validador oficial](https://github.com/teslamotors/light-show/blob/9f949512146d881b6eb66d042b22ee3f9e115afb/validator.py). Leé las instrucciones del oficial antes de ejecutarlo. Añadí pruebas de las envolventes del generador, ya que el validador incluido no demuestra que cada rampa llegó al extremo. Para XML editable comprobá equivalencia con el FSEQ; no afirmes un render xLights sin ejecutar esa aplicación.

El informe debe distinguir estructura válida, intención coreográfica y resultado físico. Si faltan datos del vehículo, registralos como desconocidos.

## 5. Copiar y probar

Sólo si el usuario autorizó la copia, identificá el USB correcto y colocá los pares en su carpeta raíz LightShow. No hace falta formatear un volumen compatible. Conservá los archivos ajenos a esta entrega y las revisiones anteriores en la computadora. Compará hashes y expulsá el volumen.

Registrá la respuesta del auto por canal o escena. Los videos son evidencia cualitativa, no mediciones fotométricas. Antes de compartirlos, revisá matrículas, rostros, ubicación y metadatos. Una autorización para generar un show no autoriza publicar su audio o videos.
