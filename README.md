# Граф музыкальных коллабораций.
В качестве источника дыннх мною был выбран сервис <b>Яндекс.Музыка</b>, которые предоставляет доступ к большому числу исполнителей и их трекам.

Граф формируется следующим образом:
 - Вершины --  уникальные исполнители
 - У вершин есть аттрибуты: название жанров в которых, согласно сервису выступает артист.
 - Ребро соеденияет две вершины, если у артистов есть совместная композиция
 - Колличество совместных композиций -- вес ребра
 ## Сбор данных
Я ограничил круг собираемых данных только артистами, представленными в жанре "<b>Иностранный рэп и хип-хоп</b>". (https://music.yandex.ru/genre/иностранный%20рэп%20и%20хип-хоп/artists).
Алгоритм сбора данных: 
1. Для каждого исполнителя в списке открывалась страница его альбомов (напрмиер https://music.yandex.ru/artist/611169/albums)
2. а) Если на странице альбомов исполнителя представлен сингл, то сразу смотрится кто исполнители.

   б) Если альбом, то происходит переход на его страницу и далее  выделяются исполнители каждой песни.

Сбор данных происходит при помощи библиотеки <b>Scrapy</b>.

Код паука в папке './yandexmusic/yandexmusic/spiders/spider.py'.

После данные с помощью библиотеки py2neo и отправляются в граф Neo4j ('./yandexmusic/yandexmusic/pipelines.py').

Чтобы уменьшить размер данных, из графа убираются артисты, которые имеют совместные композиции только с одним другим музыкантом. С помощью запроса в Neo4j
<code>
MATCH (a)
where size((a)-[]-())=1
MATCH (a)-[f]-(b)
DELETE f, a
 </code>
 
Итоги сбора данных:
| Число исполнителей  | Число связей |
| ------------- | ------------- |
| 4255  | 17466   |

1             |  2
:-------------------------:|:-------------------------:
![](https://i.ibb.co/0Dgtq1d/Screenshot-2020-03-19-at-00-09-05.png)  |  ![Рабоатет?](https://i.ibb.co/MBQnb9d/Screenshot-2020-03-18-at-22-59-52.png)
:-------------------------:|:-------------------------:
https://i.ibb.co/4P9Dhtw/Screenshot-2020-03-19-at-00-13-19.png | asdsad
