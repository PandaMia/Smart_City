from yolov5.detect import yolo
from helper import background, get_mask, merge
from speed_x10 import change_speed_1
import argparse


class Create_Heatmap():
    '''
    Аргументы которые можно менять:  
        - input_path (str) - путь к видео которое нужно обработать  
        - output_path (str) - путь где сохранить фото тепловой карты  
        - speed_x  (int) - во сколько раз ускорить видео  
        - intensity  (int) - какая интенсивность пикселя(heatmap) для одного ББ  
        - threshold  (int) - какая ширина пикселя(heatmap) для одного ББ  
        - background_count (int) - количество фреймов для получения фона без движущихся объектов  
        - transparency  (float) - коэффициент прозрачности heatmap 
    '''

    def __init__(self,
                    input_path='./input.mp4', 
                    speed_x=0, 
                    background_count=50,  
                    ):

        if speed_x:
            change_speed_1(input_path=input_path, 
                        speed=speed_x,
                        out_path='./input.mp4')
            input_path = './input.mp4'



        # self.path_labels = yolo(input_path)

        self.path_labels = 'yolov5/runs/detect/exp/labels'

        self.height, self.width = background(input_path, 
                                            background_count=background_count)


    def get_heatmap(self,
                    intensity=3,
                    threshold=5,
                    output_path='./heatmap.jpg',
                    transparency=0.7,
                    ):
                    
        get_mask(self.path_labels, 
                    height = self.height, 
                    width = self.width, 
                    threshold=threshold, 
                    intensity=intensity)

        merge(output_path, 
                transparency=transparency)


def parse_opt():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_path', type=str, default='./input.mp4', help='')
    parser.add_argument('--output_path', type=str, default='./heatmap.jpg', help='')
    parser.add_argument('--speed_x', type=int, default=0, help='')
    parser.add_argument('--intensity',type=int, default=3, help='')
    parser.add_argument('--threshold', type=int, default=5, help='')
    parser.add_argument('--background_count',type=int, default=50, help='')
    parser.add_argument('--transparency', type=float, default=0.7, help='')

    opt = parser.parse_args()
    return opt


def main(opt):
    create_heatmap = Create_Heatmap(opt.input_path, 
                                    opt.speed_x, 
                                    opt.background_count)

    create_heatmap.get_heatmap(opt.intensity,
                            opt.threshold,
                            opt.output_path,
                            opt.transparency
                            )



if __name__ == "__main__":
    opt = parse_opt()
    main(opt)

# python create_heatmap.py  --input_path "2.mp4" --speed_x 10
