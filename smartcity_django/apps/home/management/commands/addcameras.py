from django.core.management.base import BaseCommand
from apps.home.models import Pothole
import random


data = [['Альметьевск; Белоглазова 131', 54.902532,52.289729],
        ['Альметьевск; Белоглазова 151', 54.900249,52.287286],
        ['Альметьевск; Джалиля 15', 54.897003,52.296601],
        ['Альметьевск; Гафиатуллина 29Б', 54.905891,52.270927],
        ['Альметьевск; Гафиатуллина 39', 54.906383,52.266427],
        ['Альметьевск; Гафиатуллина 45', 54.905829,52.264387],
        ['Альметьевск; Гафиатуллина 47 (1)', 54.906518,52.263822],
        ['Альметьевск; Гафиатуллина 47 (2)', 54.906518,52.263822],
        ['Альметьевск; Гафиатуллина 51Б', 54.906678,52.262923],
        ['Альметьевск; Ленина 109', 54.898013,52.273757],
        ['Альметьевск; Ленина 66', 54.900078,52.290205],
        ['Альметьевск; Ленина 90', 54.89867,52.285722],
        ['Альметьевск; Шевченко 80', 54.896071,52.28839],
        ['Альметьевск; Строителей 20А', 54.901207,52.268888],
        ['Альметьевск; Строителей 20Б', 54.900777,52.26746],
        ['Альметьевск; Строителей 20', 54.902294,52.270047],
        ['Казань; Блюхера 79', 55.827555,49.067499],
        ['Казань; Чистопольская 61А', 55.819934,49.132546],
        ['Казань; Химиков 19', 55.867799,49.015936],
        ['Казань; Кариева 4а к2', 55.784364,49.185636],
        ['Казань; Кариева 4а к2', 55.784364,49.185636],
        ['Казань; Родины 26Е', 55.763169,49.191296],
        ['Казань; Родины 26Е', 55.763169,49.191296],
        ['Казань; Симонова 15', 55.865637,49.086444],
        ['Казань; ул. Чапаева 11', 55.862323,49.080875],
        ['Казань; ул. Чапаева 16', 55.863581,49.083282],
        ['Казань; ул. Чапаева 16', 55.863581,49.083282],
        ['Казань; ул. Побежимова 36 1 подъезд', 55.860292,49.082115],
        ['Казань; ул. Побежимова 36 2 подъезд', 55.860292,49.082115],
        ['Казань; ул. Побежимова 36 3 подъезд', 55.860292,49.082115],
        ['Казань; ул. Побежимова 36 4 подъезд', 55.860292,49.082115],
        ['Казань; ул. Побежимова 36 5 подъезд', 55.860292,49.082115],
        ['Казань; ул. Побежимова 36 6 подъезд', 55.860292,49.082115],
        ['Казань; ул. Побежимова 36 7 подъезд', 55.860292,49.082115],
        ['Казань; ул. Побежимова 36 дет. площадка', 55.860292,49.082115],
        ['Казань; ул. Побежимова 36 обзор вдоль дома (1)', 55.860292,49.082115],
        ['Казань; ул. Побежимова 36 обзор вдоль дома (2)', 55.860292,49.082115],
        ['Казань; ул. Побежимова 36 парковка 1', 55.860292,49.082115],
        ['Казань; ул. Побежимова 36 парковка 2', 55.860292,49.082115],
        ['Казань; ул. Побежимова 36 въезд', 55.860292,49.082115],
        ['Казань; ул. Побежимова 36 вниз перпендикулярно дому', 55.860292,49.082115],
        ['Казань Проспект Победы д. 139 корпус 3', 55.775768,49.216467],
        ['Казань ул. Вишневского д. 49', 55.785174,49.151042],
        ['Казань Аметьевская магистраль-ул. Даурская (рядом с ж/д тоннелем)', 55.768334,49.170482],
        ['Казань ул. Амирхана Еники - ул. Рабочей Молодежи (1)', 55.78237,49.154492],
        ['Казань ул. Амирхана Еники - ул. Рабочей Молодежи (2)', 55.78237,49.154492],
        ['Казань ул. Амирхана Еники - ул. Рабочей Молодежи', 55.78237,49.154492],
        ['Казань ул. Баумана д.47', 55.788171,49.120383],
        ['Казань ул. Богатырева- ул. Лазарева перекресток', 55.815549,49.052874],
        ['Казань ул. Б. Шахиди – Саид Галеева – Р. Яхина - 1', 55.793247,49.09673],
        ['Казань ул. Чернышевского – Баумана - 1', 55.791385,49.108049],
        ['Казань ул. Чернышевского – Баумана - 2', 55.791385,49.108049],
        ['Казань ул. Дементьева д. 33', 55.860105,49.101806],
        ['Казань ул. Горьковское шоссе (оз. Лебяжье) – подземный переход (2)', 55.856513,38.519229],
        ['Казань ул. Кремлевская д. 2 Нац. Музей Спасская башня', 55.795762,49.109603],
        ['Казань ул. Молодежная д.8', 55.862793,49.099731],
        ['Казань ул. Н. Ершова - ул. Вишневского проезжая часть по ул. Н. Ершова', 55.792706,49.153315],
        ['Казань ул. Пушкина д.17', 55.788844,49.123437],
        ['Казань ул. Р. Яхина – ул. Г. Исхаки - 1', 55.790671,49.102848]]

class Command(BaseCommand):

    def handle(self, *args, **options):
        print('Обновление данных...')
        Pothole.objects.all().delete()

        for i, d in enumerate(data):
            cameraUrl = f'rtsp://admin:admin@192.162.{random.randint(0,2)}.{random.randint(1,10)}:{random.randint(100, 100000)}/{random.randint(0,10)}'
            address = d[0]
            value = round(random.random(), 2)
            longitude = d[1]
            latitude = d[2]
            pothole = Pothole.create(i, cameraUrl, address, value, longitude, latitude)
            pothole.save()
        print('Done')
