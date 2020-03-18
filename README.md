# Граф музыкальных колобораций.
В качестве источника дыннх мною был выбран сервис Яндекс.Музыка, которые предоставляет доступ к большому числу исполнителей и их трекам.

Граф формируется следующим образом:
 - Вершины --  уникальные исполнители
 - У вершин есть аттрибуты: название жанров в которых, согласно сервису выступает артист.
 - Ребро соеденияет две вершины, если у артистов есть совместная композиция
 - Колличество совместных композиций -- вес ребра
 ## Сбор данных
Я ограничил круг собираемых данных только артистами, представленными в жанре "Иностранный рэп и хип-хоп". (https://music.yandex.ru/genre/иностранный%20рэп%20и%20хип-хоп/artists)
![Рабоатет?](https://i.ibb.co/MBQnb9d/Screenshot-2020-03-18-at-22-59-52.png)
