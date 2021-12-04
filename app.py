import os
import streamlit as st
import streamlink
import pandas as pd
import torch
import cv2
from config import GARBAGE_CONFIG, POTHOLE_CONFIG
from create_anomaly_model import get_anomaly_model, evaluate
from Run import main


@st.cache(max_entries=3)
def get_yolo5(weights='weights/yolov5s.pt'):
    return torch.hub.load('ultralytics/yolov5', 'custom', path=weights)


@st.cache(max_entries=10)
def get_preds(img, model):
    return model([img]).xyxy[0].cpu().numpy()


def save_uploaded_file(uploaded_file):
    with open(os.path.join("source", uploaded_file.name), "wb") as f:
        f.write(uploaded_file.getbuffer())


def prepare_video(filename, model, colors):
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

        result = get_preds(frame, model)
        result_copy = result.copy()

        # нарисуем боксы для всех найденных целевых объектов
        frame = draw_boxes(frame, result_copy, colors)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        vid_writer.write(frame)
    vid_writer.release()
    vid_cap.release()
    cv2.destroyAllWindows()
    return save_path


def draw_boxes(frame, boxes, colors):
    for bbox_data in boxes:
        xmin, ymin, xmax, ymax, _, label = bbox_data
        p0, p1, label = (int(xmin), int(ymin)), (int(xmax), int(ymax)), int(label)
        frame = cv2.rectangle(frame,
                              p0, p1,
                              colors[label], 2)
    return frame


def load_and_show_video(model, config):
    uploaded_file = st.sidebar.file_uploader("Загрузите видео", type=['avi', 'mp4'])

    if uploaded_file is not None:
        with st.spinner(text='Загрузка видео'):
            save_uploaded_file(uploaded_file)
        with st.spinner(text='Обработка видео'):
            prepared_video_path = prepare_video(uploaded_file.name, model, config['colors'])

        st.video(prepared_video_path)
        show_legend(config)


def video_to_frames(filename):
    indir = os.path.join('source', filename)
    videoCapture = cv2.VideoCapture()
    videoCapture.open(indir)
    frames = videoCapture.get(cv2.CAP_PROP_FRAME_COUNT)

    outdir = 'source/images'
    for i in range(int(frames) - 1):
        ret, frame = videoCapture.read()
        cv2.imwrite(os.path.join(outdir, "frame_%06d.jpg" % (i)), frame)


def prepare_anomaly_video():
    uploaded_file = st.sidebar.file_uploader("Загрузите видео", type=['avi', 'mp4'])
    if uploaded_file is not None:
        with st.spinner(text='Загрузка видео'):
            save_uploaded_file(uploaded_file)
        with st.spinner(text='Обработка видео'):
            video_to_frames(uploaded_file.name)

        st.video(os.path.join("source", uploaded_file.name))

        images_path = 'source/images'
        evaluate(anomaly_model, images_path)
        st.image('source/saved_figure.png')


def show_stream(model, config):
    streams = {'Камера 1': 'https://youtu.be/AdUw5RdyZxI',
               'Камера 2': 'https://youtu.be/J6LiOrQoih4',
               'Камера 3': 'https://youtu.be/RQA5RcIZlAM'}

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
            if process:
                show_legend(config)

        while run:
            _, frame = camera.read()
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            if process:
                result = get_preds(frame, model)
                result_copy = result.copy()

                frame = draw_boxes(frame, result_copy, config['colors'])

            frame_window.image(frame)

        else:
            st.write('Видеопоток остановлен')


def show_legend(config):
    class_ids = list(range(len(config['classes'])))
    labels = [config['classes'][index] for index in class_ids]
    legend_df = pd.DataFrame({'Класс': labels})

    classes = config['classes']
    colors = config['colors']

    def get_legend_color(class_name: int):
        index = classes.index(class_name)
        color = colors[index]
        return 'background-color: rgb({color[0]},{color[1]},{color[2]})'.format(color=color)

    st.dataframe(legend_df.style.applymap(get_legend_color))


st.title('Умный город')

garbage_weights = 'weights/garbage_weights.pt'
pothole_weights = 'weights/pothole_weights.pt'
coco_weights = 'weights/yolov5s.pt'
with st.spinner('Загрузка моделей...'):
    garbage_model = get_yolo5(garbage_weights)
    pothole_model = get_yolo5(pothole_weights)
    coco_model = get_yolo5(coco_weights)
st.sidebar.success('Модели загружены!')

task_type = st.sidebar.selectbox('Выберите тип задачи',
                                 ('Задача не выбрана', 'Чистый двор', 'Дорожник',
                                  'Safety-прак', 'Teplo-maps', 'Паркинг'),
                                 index=0)

if task_type == 'Чистый двор':
    data_type = st.sidebar.selectbox('Выберите способ передачи данных',
                                     ('Способ не выбран', 'Загрузить видео', 'Подключиться к камере'),
                                     index=0)

    if data_type == 'Загрузить видео':
        load_and_show_video(garbage_model, GARBAGE_CONFIG)

    elif data_type == 'Подключиться к камере':
        show_stream(garbage_model, GARBAGE_CONFIG)

elif task_type == 'Дорожник':
    data_type = st.sidebar.selectbox('Выберите способ передачи данных',
                                     ('Способ не выбран', 'Загрузить видео', 'Подключиться к камере'),
                                     index=0)

    if data_type == 'Загрузить видео':
        load_and_show_video(pothole_model, POTHOLE_CONFIG)

    elif data_type == 'Подключиться к камере':
        show_stream(pothole_model, POTHOLE_CONFIG)

elif task_type == 'Safety-прак':
    data_type = st.sidebar.selectbox('Выберите способ передачи данных',
                                     ('Способ не выбран', 'Загрузить видео'),
                                     index=0)

    if data_type == 'Загрузить видео':
        anomaly_model = get_anomaly_model()
        prepare_anomaly_video()

elif task_type == 'Teplo-maps':
    st.video(os.path.join("source", 'heatmap.mp4'))
    run = st.checkbox('Вывести тепловую карту передвижений')
    if run:
        st.image(os.path.join('source', 'prepared', 'heatmap.jpg'))

elif task_type == 'Паркинг':
    img_file = "source/photo.jpg"
    border_file = "source/border.jpg"
    st.image(img_file)
    run = st.checkbox('Построить 3D-боксы и проверить правильность парковки')
    if run:
        main(img_file, border_file)
        st.image(os.path.join('source', 'prepared', '3Dbox.jpg'))

