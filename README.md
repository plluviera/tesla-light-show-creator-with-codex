# Tesla Light Show creator with Codex

Guía práctica para que **Codex, otro LLM o un agente con herramientas** cree shows musicales para un **Tesla Model Y Juniper**, con barra frontal, LED blancos laterales y señaleros delanteros y traseros.

El proyecto reúne un mapa observado en un vehículo, instrucciones para agentes, un prompt reutilizable, una prueba con audio sintético y un validador local. **No es una aplicación de generación automática de música ni un producto oficial de Tesla u OpenAI.** El agente debe analizar el audio y generar la coreografía siguiendo estas instrucciones.

## Empezar

1. Cloná este repositorio y abrilo en tu entorno de programación.
2. Leé [el flujo de trabajo](docs/workflow.es.md) y [el mapa y sus límites](docs/channel-map.es.md).
3. Copiá [el prompt completo](prompts/create-show.es.md), completá año, firmware, ruta del audio y carpeta de salida, y enviáselo al agente. Si tu herramienta no carga `AGENTS.md`, adjuntalo como instrucciones del proyecto.
4. El agente debe producir pares `LightShow/nombre.fseq` + `LightShow/nombre.wav`, código reproducible e informe de validación.
5. Probá el resultado en tu vehículo y registrá qué respondió. Un archivo válido no demuestra compatibilidad física.

Ejemplo de pedido breve, después de cargar las instrucciones:

> Usá el prompt del proyecto para crear un show con el audio que adjunto. Mi auto es Model Y Juniper [año], firmware [versión]. Quiero alternancias rítmicas de señaleros delante y atrás, barra central con crescendos y momentos separados para los laterales blancos. Guardá los resultados en output/mi_tema y usá mi_tema como nombre corto. Generá y validá archivos reales. No copies a un USB hasta que te indique cuál.

## Probar el mapa sin música

Requiere Python 3.10 o posterior. Las herramientas incluidas sólo usan la biblioteca estándar.

```sh
python3 tools/juniper_fade_probe.py --output output/probe
python3 tools/validate_show.py output/probe/LightShow/juniper_fade_probe.fseq --audio output/probe/LightShow/juniper_fade_probe.wav
python3 -m unittest discover -s tests -v
```

La prueba genera pitidos y cuatro bloques: canal 11 solo, 12 solo, 11+12 y 7+8+11+12. El [informe en inglés](docs/observed-mapping.en.md) explica los tiempos. No mezcla música protegida ni videos del propietario. Este diagnóstico acortado reproduce comandos ensayados; **el archivo concreto incluido no fue ejecutado físicamente**.

Para una coreografía generada según el perfil del proyecto:

```sh
python3 tools/validate_show.py output/mi_tema/LightShow/mi_tema.fseq --audio output/mi_tema/LightShow/mi_tema.wav --musical
```

`--musical` exige actividad de barra, laterales y señaleros, canal 12 apagado y pulsos ámbar de al menos 100 ms. Es una comprobación adicional, no un reemplazo del validador oficial ni de una prueba en el auto.

## Qué aprendimos

- En el vehículo probado, **11 o 12 por separado operaron la barra central completa**. Para componer usamos 11 y dejamos 12 apagado.
- **7/8 operaron los LED blancos laterales frontales**. La barra no necesitó esos canales para realizar fundidos.
- **13/14 son los señaleros delanteros**; 23/24 son las salidas de señaleros traseros del template. El color trasero depende del hardware; el video frontal no lo certifica.
- Los bytes de fundido son comandos temporales, no niveles lineales de brillo.
- Una primera composición dejó 13/14 apagados por comparar energía promedio de frases contra un umbral de energía instantánea. Ahora exigimos estadísticas y actividad real en ambos canales.

Los ensayos pertenecen a un Juniper reportado como año 2027. Firmware, acabado y especificación de mercado no se registraron. No demostramos píxeles direccionables ni garantizamos el mapa para todas las versiones. [Reporte público a Tesla #183](https://github.com/teslamotors/light-show/issues/183).

## Contenido

| Archivo | Uso |
| --- | --- |
| [AGENTS.md](AGENTS.md) | Instrucciones operativas para el agente |
| [Prompt en español](prompts/create-show.es.md) | Pedido completo listo para adaptar |
| [Mapa de canales](docs/channel-map.es.md) | Salidas, bytes y límites de la evidencia |
| [Flujo de creación](docs/workflow.es.md) | Audio, ritmo, exportación, validación y USB |
| [Formato FSEQ](docs/fseq-profile.es.md) | Perfil conservador y cabecera reproducible |
| [Informe en inglés](docs/observed-mapping.en.md) | Método y resultados de las pruebas |
| [Cómo aportar](CONTRIBUTING.md) | Reportar pruebas sin exponer información personal |

Los audios del usuario y los archivos generados deben quedar en `input/` y `output/`, excluidos de Git. No se incluyen canciones comerciales, videos privados ni coreografías descargadas de terceros. El código y los textos originales se distribuyen con licencia MIT.

Fuentes: [guía oficial Tesla](https://github.com/teslamotors/light-show), [discusión #166](https://github.com/teslamotors/light-show/issues/166), y ensayos documentados en #183. La guía oficial consultada se fija en el [commit 9f94951](https://github.com/teslamotors/light-show/tree/9f949512146d881b6eb66d042b22ee3f9e115afb); revisá cambios posteriores antes de introducir capacidades nuevas.
