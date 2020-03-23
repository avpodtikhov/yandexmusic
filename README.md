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
| Число исполнителей  | Число связей | Число жанров
| ------------- | ------------- | ------------- | 
| 4255  | 17466   |  47 | 

1             |  2
:-------------------------:|:-------------------------:
![](https://camo.githubusercontent.com/e46b1e76ea1247ac7842b35a76dc3c0935c10881/68747470733a2f2f692e6962622e636f2f304467747131642f53637265656e73686f742d323032302d30332d31392d61742d30302d30392d30352e706e67)  |  ![Рабоатет?](https://i.ibb.co/MBQnb9d/Screenshot-2020-03-18-at-22-59-52.png)
3             |  4
![](https://i.ibb.co/4P9Dhtw/Screenshot-2020-03-19-at-00-13-19.png) | ![](https://i.ibb.co/9GrxcLb/Screenshot-2020-03-19-at-00-27-29.png)
# Алгоритм визуализации.
В качестве алгоритма для визуализации графа я выбрал <b>Fruchterman-Reingold</b>.
Его основная идея состоит в предположении, что на любую вершину воздействуют две силы: сила притяжения - пртиягивающая соседние вершины и сила отталкивания, которая рассеивает все вершины. То есть во время работы алгоритм пытается минимизировать расстояния между соседними вершинами и максимизировать расстояние вершинами не соедененными ребром.

Алгоритм (http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.13.8444&rep=rep1&type=pdf):
![](https://i.imgur.com/X2z4OnQ.png)
Я добавил несколько изменений к описанному выше алгоритму:
1. W = L = 1.
2. После каждого подсчета |/delta| пришлось сравнивать его с 0, так как инчае часто происходило деление на ноль.
3. Начальныое значение температуры равно 0.1 * W
4. Убрал два последних ограничения на выход за границы поля (Просто стало выглядеть красивее, часть точек больше не примыкает к краям изображения).

Результаты на стандартных графах:
## Karate_club
Моя реализация             |  Networkx
:-------------------------:|:-------------------------:
![](./images/karate_my.png) | ![]()
