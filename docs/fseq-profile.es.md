# Perfil FSEQ de este proyecto

Perfil deliberadamente acotado: FSEQ 2.0, sin compresión, 48 canales, frame de 20 ms, cabecera de 32 bytes, sin bloques opcionales. No es un validador de todas las variantes posibles de FSEQ.

Ejemplo Python para escribir una matriz de bytes en orden frame → canal:

```python
import math
import struct

frames = math.ceil(duration_seconds / 0.020)
header = bytearray(32)
header[:4] = b'PSEQ'
struct.pack_into('<HBBHIIB', header, 4, 32, 0, 2, 32, 48, frames, 20)
assert len(payload) == frames * 48
path.write_bytes(header + payload)
```

| Offset | Tipo | Valor |
| --- | --- | --- |
| 0 | 4 bytes | PSEQ |
| 4 | uint16 little endian | Inicio de datos: 32 |
| 6 / 7 | uint8 / uint8 | Versión menor 0 / mayor 2 |
| 8 | uint16 | Cabecera estándar: 32 |
| 10 | uint32 | Canales: 48 |
| 14 | uint32 | Frames |
| 18 | uint8 | Paso: 20 ms |
| 19–31 | bytes | Cero en este perfil mínimo |

El payload tiene exactamente `48 * frames` bytes. Los últimos cinco frames se dejan en cero. El generador debe reservar el final del audio para concluir las rampas antes del apagado. La diferencia entre duración del audio y de la secuencia debe ser menor o igual a un frame.

El validador local acepta únicamente este perfil conservador; puede rechazar un FSEQ válido creado por otra herramienta con una cabecera distinta. No lo uses para declarar inválidos archivos ajenos en general. `--musical` añade las expectativas de actividad y composición de nuestro proyecto; el diagnóstico, que usa el canal 12 para ensayarlo, se valida sin esa opción.
