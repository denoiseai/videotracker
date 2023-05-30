#####################################################
# video_tracker.py
#
# Autor: Ángel López Morales
# Licencia: MIT
#####################################################


import cv2
from moviepy.editor import *
import os
import sys
import argparse
from tqdm import tqdm

def resize_frame(frame, height=1280):
    (original_height, original_width) = frame.shape[:2]
    aspect_ratio = original_width / original_height

    new_width = int(height * aspect_ratio)
    resized_frame = cv2.resize(frame, (new_width, height))
    return resized_frame


def resize_display_frame(frame):
    display_width = 480
    display_height = 720
    resized_frame = cv2.resize(frame, (display_width, display_height), interpolation=cv2.INTER_AREA)
    return resized_frame

# Configura el analizador de argumentos
parser = argparse.ArgumentParser(description="Video Tracker")
parser.add_argument("input_video", help="ruta del archivo de video de entrada")
args = parser.parse_args()

# Carga el video
video = cv2.VideoCapture(args.input_video)

# Crea un objeto tracker
tracker = cv2.TrackerCSRT_create()

# Lee el primer frame del video
ret, frame = video.read()

frame = resize_frame(frame)
# Calcula la posición inicial para la ROI
roi = cv2.selectROI("Tracker", frame, False, False)
roi_x, roi_y, _, _ = roi
print(roi_x, roi_y)
roi = (roi_x, roi_y, 720, 1280)

# Inicializa el tracker con el primer frame y la ROI
tracker.init(frame, roi)

# Configura el codec y crea un objeto VideoWriter para guardar el video resultante
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter('output.mp4', fourcc, video.get(cv2.CAP_PROP_FPS), (720, 1280))
if not out.isOpened():
    print("Error: VideoWriter no se pudo abrir.")
    exit()

start_y = 0
end_y = 0
start_x = 0
end_y = 0
fps = int(video.get(cv2.CAP_PROP_FPS))

frame_count = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
progress_bar = tqdm(total=frame_count, desc="Procesando video", unit="frame")


frames_to_skip = 2

frame_count = 0

while True:
    # Lee el siguiente frame
    ret, frame = video.read()
    if not ret:
        break

    frame_count += 1
    progress_bar.update(1)


    if frame_count % frames_to_skip == 0:
        ret, roi = tracker.update(frame)
    # Actualiza el tracker y obtén la nueva posición
    # ret, roi = tracker.update(frame)


    if ret:
        x, y, w, h = tuple(map(int, roi))
    #    cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

        # Calcula la posición central del objeto
        center_x = x + w // 2
        center_y = y + h // 2


        start_x = max(0, center_x - 720 // 2)
        end_x = start_x + 720

      #  start_y = max(0, center_y - 1280 // 2)
        start_y = 0
        end_y = start_y + 1280
        
        

        # Recorta el frame centrado en el objeto
        cropped_frame = frame[start_y:end_y, start_x:end_x]

       
    else:
        #cv2.putText(frame, "Tracking failure", (100, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)
        #cropped_frame = cv2.resize(frame, (720, 1280))
        
        cropped_frame = frame[start_y:end_y, start_x:end_x]

    # Guarda el frame en el archivo de salida
    
    if out.isOpened():
    # Verificar si las dimensiones de 'cropped_frame' coinciden con las dimensiones especificadas en VideoWriter
        if cropped_frame.shape[1] != 720 or cropped_frame.shape[0] != 1280:
        # Redimensionar el frame recortado a las dimensiones esperadas (720, 1280)
            cropped_frame = cv2.resize(cropped_frame, (720, 1280))

    # Escribir el frame en el archivo de salida
        out.write(cropped_frame)
    else:
        print("Error: El objeto VideoWriter no está abierto correctamente.") 
    # Muestra el resultado
    display_frame = resize_display_frame(cropped_frame)
    cv2.imshow("Tracker", display_frame)

    # Termina el bucle si se presiona la tecla 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


# Libera los recursos y cierra las ventanas
video.release()
out.release()
cv2.destroyAllWindows()
progress_bar.close()


# Agrega el audio al video de salida
input_video = VideoFileClip(args.input_video)
output_video_without_audio = VideoFileClip("output.mp4")
output_video_with_audio = output_video_without_audio.set_audio(input_video.audio)

# Genera el nombre del archivo de salida
output_filename = os.path.splitext(args.input_video)[0] + "_vertical.mp4"
output_video_with_audio.write_videofile(output_filename, codec='libx264', audio_codec="aac")


# Elimina el archivo temporal "output.mp4"
os.remove("output.mp4")