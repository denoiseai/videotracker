# Video Tracker

Este proyecto utiliza el algoritmo de rastreo CSRT para centrar a una persona en un video al cambiar de formato horizontal a vertical, como en dispositivos móviles. Mantiene el audio original y muestra una barra de progreso en la consola, ofreciendo una solución eficiente y profesional para ajustar videos a visualizaciones verticales.

## Requisitos

- Python 3
- OpenCV
- MoviePy
- tqdm

## Instalación

Para instalar las dependencias necesarias, ejecute el siguiente comando:

\```bash
pip install opencv-python opencv-python-headless moviepy tqdm
\```

## Uso

Para usar este script, ejecute el siguiente comando en la terminal o línea de comandos:

\```bash
python video_tracker.py input.mp4
\```

Reemplace `input.mp4` con la ruta de su archivo de video de entrada. El archivo de salida se creará con el mismo nombre que el archivo de entrada, pero con el sufijo "_vertical".

## Licencia

Este proyecto está licenciado bajo la [Licencia MIT](LICENSE).
