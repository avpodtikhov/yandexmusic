# Граф музыкальных колобораций.
В качестве источника дыннх мною был выбран сервис Яндекс.Музыка, которые предоставляет доступ к большому числу исполнителей и их трекам.

Граф формируется следующим образом:
 - Вершины --  уникальные исполнители
 - Ребро соеденияет две вершины, если у артистов есть совместная песня
 - Колличество совместных композиций -- вес ребра
 - У вершин есть аттрибуты: название жанров в которых, согласно сервису выступает артист.
![Рабоатет?](https://i.ibb.co/MBQnb9d/Screenshot-2020-03-18-at-22-59-52.png)
