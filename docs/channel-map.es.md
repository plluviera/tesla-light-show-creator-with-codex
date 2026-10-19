# Mapa de trabajo del Juniper

Numeración desde 1. Índice Python = canal − 1. La evidencia proviene de un único vehículo, reportado como Model Y Juniper 2027; firmware, acabado y mercado no registrados.

| Canal | Salida de trabajo | Evidencia |
| --- | --- | --- |
| 3/4 | Grupos blancos inferiores del frente | Respuesta visible en ensayo aislado |
| 7/8 | Tiras blancas laterales del frente | Encendido independiente y fundidos visibles |
| 11 | Barra central completa | Fundidos con 7, 8 y 12 apagados |
| 12 | Misma barra completa | También respondió solo; mantener cero al usar 11 |
| 13/14 | Señaleros ámbar delanteros | Respuesta visible en ensayo aislado |
| 21/22 | Repetidores laterales | Nombres del template; no verificados por el video frontal |
| 23/24 | Señaleros traseros | Nombres del template; no verificados por el video frontal |
| 25 | Freno | Nombre del template, salida binaria |
| 26/27 | Posición trasera | Nombres del template, salidas binarias |
| 31–46 | Partes móviles | Siempre cero en este proyecto |

Las demás salidas permanecen en cero en el perfil musical. El color de los señaleros traseros depende del vehículo: un archivo no convierte una lámpara roja en amarilla.

## Bytes exactos utilizados

| Acción | Tiempo nominal | Byte | Porcentaje constante xLights |
| --- | --- | ---: | ---: |
| Apagar inmediato | — | 0 | 0 |
| Bajar | 0,5 s | 25 | 10 |
| Bajar | 1 s | 51 | 20 |
| Bajar | 2 s | 76 | 30 |
| Subir | 0,5 s | 178 | 70 |
| Subir | 1 s | 204 | 80 |
| Subir | 2 s | 229 | 90 |
| Encender inmediato | — | 255 | 100 |

Se calcularon con `int(255 * porcentaje / 100)`. Se ensayaron esos bytes, no todos los enteros adyacentes. Mantené el comando durante el tiempo nominal más 60 ms para completar el fundido. No uses rampas en salidas binarias. Exposición y brillo de la cámara impiden medir tiempos exactos o luminancia calibrada.

## Lo que no se demostró

No hay evidencia de control por píxel ni por mitades de barra. La prueba de canales 47–106 no produjo respuesta visible en este auto aunque hubo audio y destellos de control. Eso no demuestra ausencia universal de soporte. Tampoco se verificó intensidad lineal para valores arbitrarios 0–255. El requisito de un líder Channel 4 de otros mapas no fue necesario para la barra de este vehículo.

Para repetir el ensayo, ver [el informe y cronograma](observed-mapping.en.md). Para publicar resultados indicar firmware y vehículo, y separar observaciones de hipótesis.
