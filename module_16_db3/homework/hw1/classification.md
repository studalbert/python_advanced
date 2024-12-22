## Типы связей между таблицами в схеме

![](../img/cinema_schema_diagram.png)

|   Тип связи    | Таблица 1 | Таблица 2       |
|:--------------:|-----------|-----------------|
| один-ко-многим | director  | movie_direction |
| один-к-одному  | movie     | movie_direction |
| один-ко-многим | movie     | oscar_awarded   |
| один-ко-многим | movie     | movie_cast      |
| один-ко-многим | actors    | movie_cast      |