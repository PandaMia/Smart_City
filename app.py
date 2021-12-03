import time
import os
import streamlit as st
import io
import streamlink
import numpy as np
import matplotlib.colors as mcolors
import torch
import cv2
from config import COCO_CLASSES


@st.cache(max_entries=2)
def get_yolo5(weights='weights/yolov5s.pt'):
    return torch.hub.load('ultralytics/yolov5', 'custom', path=weights)


@st.cache(max_entries=10)
def get_preds(img):
    return model([img]).xyxy[0].cpu().numpy()


def get_colors(indexes):
    to_255 = lambda c: int(c*255)
    tab_colors = list(mcolors.TABLEAU_COLORS.values())
    tab_colors = [list(map(to_255, mcolors.to_rgb(name_color)))
                                                for name_color in tab_colors]
    base_colors = list(mcolors.BASE_COLORS.values())
    base_colors = [list(map(to_255, name_color)) for name_color in base_colors]
    rgb_colors = tab_colors + base_colors
    rgb_colors = rgb_colors*5

    color_dict = {}
    for i, index in enumerate(indexes):
        if i < len(rgb_colors):
            color_dict[index] = rgb_colors[i]
        else:
            color_dict[index] = (255, 0, 0)

    return color_dict


def save_uploaded_file(uploaded_file):
    with open(os.path.join("source", uploaded_file.name), "wb") as f:
        f.write(uploaded_file.getbuffer())


def prepare_video(filename):
    vid_cap = cv2.VideoCapture(os.path.join('source', filename))
    fps = vid_cap.get(cv2.CAP_PROP_FPS)
    frames = vid_cap.get(cv2.CAP_PROP_FRAME_COUNT)
    w = int(vid_cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(vid_cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    save_path = os.path.join('source', 'prepared', filename[:-4] + '.mp4')
    vid_writer = cv2.VideoWriter(save_path, cv2.VideoWriter_fourcc(*'H264'), fps, (w, h))
    for i in range(int(frames) - 1):
        _, frame = vid_cap.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        result = get_preds(frame)
        result_copy = result.copy()
        result_copy = result_copy[np.isin(result_copy[:, -1], target_class_ids)]

        # нарисуем боксы для всех найденных целевых объектов
        frame = draw_boxes(frame, result_copy)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        vid_writer.write(frame)
    vid_writer.release()
    vid_cap.release()
    cv2.destroyAllWindows()
    return save_path


def draw_boxes(frame, boxes):
    for bbox_data in boxes:
        xmin, ymin, xmax, ymax, _, label = bbox_data
        p0, p1, label = (int(xmin), int(ymin)), (int(xmax), int(ymax)), int(label)
        frame = cv2.rectangle(frame,
                              p0, p1,
                              rgb_colors[label], 2)
    return frame


streams = {'Камера 1': 'https://youtu.be/AdUw5RdyZxI',
           'Камера 2': 'https://youtu.be/J6LiOrQoih4',
           'Камера 3': 'https://youtu.be/RQA5RcIZlAM'}

st.title('Умный город')

yolo_weights = 'weights/garbage_weights.pt'
with st.spinner('Loading the model...'):
    model = get_yolo5(yolo_weights)
st.sidebar.success('Loading the model.. Done!')

target_class_ids = list(range(len(COCO_CLASSES)))
rgb_colors = get_colors(target_class_ids)

data_type = st.sidebar.selectbox('Выберите способ передачи данных',
                                 ('Способ не выбран', 'Загрузка видео', 'Подключение к камере'),
                                 index=0)


if data_type == 'Загрузка видео':
    uploaded_file = st.sidebar.file_uploader("Загрузите видео", type=['avi', 'mp4'])
    if uploaded_file is not None:
        with st.spinner(text='Loading video'):
            save_uploaded_file(uploaded_file)

        prepared_video_path = prepare_video(uploaded_file.name)
        video_file = io.open(prepared_video_path, 'rb')
        video_bytes = video_file.read()
        st.video(video_bytes)

elif data_type == 'Подключение к камере':
    camera_num = st.sidebar.selectbox('Выберите камеру',
                                      ('Камера не выбрана', 'Камера 1', 'Камера 2', 'Камера 3'),
                                      index=0)
    if camera_num != 'Камера не выбрана':
        run = st.checkbox('Подключиться к камере')
        frame_window = st.image([])

        url = streams[camera_num]

        streams = streamlink.streams(url)
        camera = cv2.VideoCapture(streams["480p"].url)

        if run:
            process = st.checkbox('Обработать')

        while run:
            _, frame = camera.read()
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            if process:
                result = get_preds(frame)
                # скопируем результаты работы кэшируемой функции, чтобы не изменить кэш
                result_copy = result.copy()
                # отберем только объекты нужных классов
                result_copy = result_copy[np.isin(result_copy[:, -1], target_class_ids)]

                # нарисуем боксы для всех найденных целевых объектов
                frame = draw_boxes(frame, result_copy)

            frame_window.image(frame)
            #time.sleep(0.01)
        else:
            st.write('Видеопоток остановлен')
