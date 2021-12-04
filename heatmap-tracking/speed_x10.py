import cv2
import tqdm
# ===============================
# Первая функция работает гораздо быстрее, но иногда подвисает на больших файлах... 
# Вторая надежнее но медленее 
# =================================

# import subprocess
# def change_speed(input_path='1.mp4', 
#                     speed='0.10',
#                     out_path='input.mp4'):
#     command = f'ffmpeg -i {input_path} -vf  "setpts={speed}*PTS" {out_path}'
#     subprocess.run(command, shell=True)


def change_speed_1(input_path='1.mp4', 
                    speed=10,
                    out_path='input.mp4'):

    video_reader = cv2.VideoCapture(input_path)

    nb_frames = int(video_reader.get(cv2.CAP_PROP_FRAME_COUNT))
    frame_h   = int(video_reader.get(cv2.CAP_PROP_FRAME_HEIGHT))
    frame_w   = int(video_reader.get(cv2.CAP_PROP_FRAME_WIDTH))
    fps       = int(video_reader.get(cv2.CAP_PROP_FPS))

    video_writer = cv2.VideoWriter(out_path,
                            cv2.VideoWriter_fourcc(*'MP4V'), 
                            fps, 
                            (frame_w, frame_h))

    for i, n in tqdm.tqdm(enumerate(range(nb_frames))):
        _, img = video_reader.read()
        if i%speed == 0:
            video_writer.write(img)

    video_reader.release()
    video_writer.release()

if __name__=='__main__':
    # change_speed()
    change_speed_1()
