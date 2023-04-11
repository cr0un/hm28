# Урок 28. Postgres, Модели с relations и QuerySet. Домашнее задание


На этой неделе мы будем делать наш «Авито» лучше!

# Шаг 1

Из прошлого задания вы уже знаете, что у нас будут объявления и категории. А в этом уроке вы научились их связывать. 

Но это еще не всё! Также в этой домашке мы добавим пользователей и их локации. 

1. Используя знания из урока, подключите к вашему проекту PostgreSQL.
2. Изучите предложенный вам [датасет](https://github.com/skypro-008/lesson28_project_sourse/tree/main/datasets), создайте по нему модели и загрузите данные в таблицы. HINT: некоторые модели и поля у вас уже есть, так что можно дописать только то, чего недостает. А вот данные придется удалить и залить заново.
3. Не забудьте про админку! Ваши модели должны быть с русскими названиями, а в качестве ссылки на запись должны отображаться:
    1. для категории — `name`,
    2. для локации — `name`,
    3. для пользователя — `username`,
    4. для объявления — `name.`
    
    HINT: Мы обсуждали, как это делается, в уроке 27, часть 2.
    

# Шаг 2

Перепишите свои View на наследников ListView, DetailView и CreateView (в зависимости от назначения каждой из них) и реализуйте недостающие для категорий и объявлений методы: 

- для  `/cat/:id` — методы PATCH/DELETE,
- для `/ad/:id` — методы PATCH/DELETE.

```json
Request
PATCH /cat/1/update/

{
	"name": "Молочная продукция"
}

Response
200
{
	"id": 1,
	"name": "Молочная продукция"
}

Request
PATCH /ad/1/update/
{
	"name": "Толстовка",
	"author_id": 1,
	"price": 500,
	"description": "Продаю кофту на рост 115 см по всем вопросам пишите", 
	"category_id": 1
}

Response
200
{
	"id": 1,
	"name": "Толстовка",
	"author_id": 1,
	"author": "Мария",
	"price": 500,
	"description": "Продаю кофту на рост 115 см по всем вопросам пишите", 
	"is_published": True,
	"category_id": 1,
	"image": "ads/image.png"
}

Request
DELETE /cat/1/delete/

Response
{
	"status": "ok"
}

Request
DELETE /ad/1/delete/

Response
{
	"status": "ok"
}
```

После этого список `urlpatterns` станет достаточно большим, так что если вы храните его в главном файле `[urls.py](http://urls.py)`, то создайте в своем приложении еще один и перенести все URL приложения в него, как мы делали это на уроке.

И не забудьте добавить отображение новых полей во view для объявлений!

# Шаг 3

Добавьте URL `/ad/1/upload_image` для загрузки картинок к объявлениям аналогично тому, как мы делали это в уроке.

Должно получиться вот так:

```json
Request
POST /ad/1/upload_image/
ContentType 'multipart/form-data'
FILES: "image" 

Response
200
{
	"id": 1,
	"name": "Толстовка",
	"author_id": 1,
	"author": "Мария",
	"price": 500,
	"description": "Продаю кофту на рост 115 см по всем вопросам пишите"
	"is_published": True,
	"category_id": 1,
	"image": "ads/image.png"
} 
```

Кстати, для записей, которые у вас уже лежа в базе у нас есть [картинки](https://github.com/skypro-008/PD_008_course5/tree/main/images). Потренироваться с отображением можно на них.

# Шаг 4

Добавьте пагинацию в отображение списков объявлений. У вас должно получиться следующее: 

```json
Request
GET /ad/

Response
200
{
	"items":
		[
			{
					"id": 1,
					"name": "Толстовка",
					"author_id": 1,
					"author": "Мария",
					"price": 500,
					"description": "Продаю кофту на рост 115 см по всем вопросам пишите",
					"is_published": True,
					"category_id": 1,
					"image": "ads/image.png"
			} 
			...
		]
	"total": 20,
	"num_pages": 10
} 
```

# Шаг 5

Реализуйте CRUD для пользователей. Не забудьте сделать добавление локации при создании и редактировании профиля, чтобы пользователи не мучались.

NOTE: подумайте, так ли сильно связаны пользователи с объявлениями? или они могут жить отдельно?

```json
Request
GET /user/

Response
200
{
	"items":
		[
			{
				"id": 1,
				"username": "palexandrov",
				"first_name": "Павел",
				"last_name": "Александров",
				"role": "member",
				"age": 18,
				"locations": [
						"Москва",  # поле name из location
				]
			},
			...
		],
	"total": 20,
	"num_pages": 10
}

Request
GET /user/1/

Response
200
{
	"id": 1,
	"username": "palexandrov",
	"first_name": "Павел",
	"last_name": "Александров",
	"role": "member",
	"age": 18,
	"locations": [
			"Москва",  # поле name из location
	]
}

404

Request
POST /user/create/
{
	"username": "palexandrov",
	"password": "password",
	"first_name": "Павел",
	"last_name": "Александров",
	"role": "member",
	"age": 18,
  "locations": ["Москва", "м. Авиастроительная"]
}

Response
200
{
	"id": 1,
	"username": "palexandrov",
	"first_name": "Павел",
	"last_name": "Александров",
	"role": "member",
	"age": 18,
	"locations": [
			"Москва",  # поле name из location
			"м. Авиастроительная"
	]
}

Request
PATCH /user/1/update/
{
	"username": "palexandrov",
	"password": "password",
	"first_name": "Павел",
	"last_name": "Александров",
	"age": 18,
  "locations": ["Москва", "м. Авиастроительная"]
}

Response
200
{
	"id": 1,
	"username": "palexandrov",
	"first_name": "Павел",
	"last_name": "Александров",
	"age": 18,
	"locations": [
			"Москва",  # поле name из location
			"м. Авиастроительная"
	]
}

Request
DELETE /user/1/delete/

Response
{
	"status": "ok"
}
```

# Шаг 6

Давайте еще добавим сортировок: 

- для пользователей: пользователи должны по умолчанию сортироваться по полю `username` (по алфавиту);
- для объявлений: только при выдаче списка объявлений сортируйте их по убыванию цены (сначала самые дорогие);
- для категорий: только при выдаче списка категорий сортируйте их по полю `name` (по алфавиту).

# Шаг 7

Добавьте в список пользователей поле с количеством опубликованных пользователем объявлений (`is_published=True`). Должно получиться вот так:

```json
Request
GET /user/Z 

Response
200
{
	"items":
		[
			{
				"id": 1,
				"username": "palexandrov",
				"first_name": "Павел",
				"last_name": "Александров",
				"role": "member",
				"age": 18,
				"location": "Москва",  # поле name из location
				"total_ads": 10,
			},
			...
		],
	"total": 20,
	"per_page": 10
}
```

**Критерии выполнения:**

- [ ]  В проекте подключен PostgreSQL.
- [ ]  В моделях есть все поля из CSV.
- [ ]  В моделях используются ForeignKey и ManyToManyField.
- [ ]  Во всех моделях определен `class Meta` и переопределен метод `__str__`.
- [ ]  Картинки, прикрепленные к объявлениям, корректно открываются.
- [ ]  Использованы ListView, DetailView, CreateView, UpdateView, DeleteView.
- [ ]  Типы данных в JSON отдаются корректно.
- [ ]  Методы из спецификации работают.
- [ ]  Используются атрибут `ordering` и метод `order_by`.
- [ ]  В списках пользователей и объявлений есть пагинация.
- [ ]  Локации могут формироваться прямо в методах создания и редактирования пользователей.
- [ ]  Используется хотя бы один из методов `aggregate` / `annotate`.
- [ ]  Используется метод `select_relation`.
- [ ]  Используются методы `get_or_create`, `get_object_or_404`.
- [ ]  URL разнесены по разным директориям.