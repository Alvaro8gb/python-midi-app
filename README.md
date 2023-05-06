# APP INSTRUMENTO MUSICAL MIDI

## Estructura
### 1. Interfaz
- [folder](view)
### 2. Teclado Midi
- [folder](input)

### 3. Logica ( Modelos)
- [folder](models)
- [Sintetizador](models/sintesis.py)
- [Sampler](models/sampler.py)

### 4. Reproductor de audio
- [folder](out)


### 5. Controlador entre in y out
- [app](./app.py)


## Ejecutarla

```pipenv run ```
## Detalles

- `view`: carpeta que contiene archivos relacionados con la interfaz gráfica de la aplicación, como componentes de la interfaz y el icono de la aplicación.
- `input`: carpeta que contiene archivos relacionados con la entrada de datos MIDI, como la conexión y el manejo de dispositivos MIDI.
- `models`: carpeta que contiene los modelos de la lógica de la aplicación, como el sintetizador y el sampler, así como otros archivos relacionados con la lógica de la aplicación, como los efectos y las utilidades.
- `out`: carpeta que contiene los archivos relacionados con la reproducción de audio, como el reproductor de audio.
- `app.py`: archivo principal que contiene la lógica de la aplicación y actúa como controlador entre los datos de entrada MIDI y la reproducción de audio.
- `globals.py`: archivo que contiene variables globales que se utilizan en diferentes partes de la aplicación.
- `samples`: carpeta que contiene archivos de audio que se utilizan en la aplicación, como muestras de notas de un piano.
- `tests`: carpeta que contiene archivos de prueba para diferentes partes de la aplicación, como la entrada MIDI y la lógica de la aplicación.
- `build.sh`: archivo de script que se utiliza para construir la aplicación.
- `LICENSE`: archivo que contiene la información de la licencia de la aplicación.
- `Pipfile` y `Pipfile.lock`: archivos que contienen la información de las dependencias de la aplicación y sus versiones.
- `README.md`: archivo que contiene información general sobre la aplicación y cómo utilizarla.
- `requirements.txt`: archivo que contiene la lista de dependencias y sus versiones necesarias para la aplicación.
