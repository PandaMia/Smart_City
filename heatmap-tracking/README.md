# heatmap-tracking

## Для запуска необходимо:
- Перейти в корневую директорию   
  
    ```
    cd ./heatmap-tracking
    ```
- Устоновить все зависимости  
  
    ```
    pip install -r requirements.txt
    ```
- Скачать подходящее видео можно по [ссылке.](https://drive.google.com/file/d/1k_as4tLd-8s3BygwvdgV5xeq8S_w49hn/view?usp=sharing) Или подобрать свое

- Проверить и запустить скрипт с cwd  
   
    ```
    python create_heatmap.py  --input_path <путь_до_файла.mp4>
    ```

-----

## Для включения в пайплайн этой модели, нужно инициализировать класс Create_Heatmap() в скрипте create_heatmap.py   
    
Аргументы которые можно менять:  
- input_path (str) - путь к видео которое нужно обработать  
- output_path (str) - путь где сохранить фото тепловой карты  
- speed_x  (int) - во сколько раз ускорить видео  
- intensity  (int) - какая интенсивность пикселя(heatmap) для одного ББ  
- threshold  (int) - какая ширина пикселя(heatmap) для одного ББ  
- background_count (int) - количество фреймов для получения фона без движущихся объектов  
- transparency  (float) - коэффициент прозрачности heatmap  
     
-------  
  
## Важно понимать, что в зависимости от ракурса, продолжительности и интенсивности трафика людей. Нужно менять параметры: intensity, threshold, transparency, background_count  
  
-------


