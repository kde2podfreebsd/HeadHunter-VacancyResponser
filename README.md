# HeadHunter-VacancyResponser
### Как работать с Oauth2.0 HeadHunter API
При создании приложения в https://dev.hh.ru/admin - вам выдается пара хэш-ключей приложния.

 - client_id
 - client_secret

Что бы ваш скрипт мог работать автономно, то нужно сделать запрос к hh.ru через залогиненую сессию, после чего браузер сделает редирект на Redirect URI + code в URL параметрах, который нужно будет достать. (В скрипте это будет работать только при pickle дампе cookies и передаче ее в теле запроса. Не рекомендуется это делать, тк 1) Безопасность 2) Этот код нужно получить единожды, дальнейшие действия помогают сделать ваш скрипт автономным"
```
GET https://hh.ru/oauth/authorize?response_type=code&client_id=<client_id>&redirect_uri=https://<redirect_uri>/
```
```
Redirect on -> https://<redirect_uri>/?code=<Your personal one-time code>
```
Далее необходимо получить пару токенов для работы с  OAuth2.0:

 - access_token
 - refresh_token

Для этого делаем POST запрос, где меняем personal_code на пару токенов. 
```
POST https://hh.ru/oauth/token?grant_type=authorization_code&client_id=<client_id>&client_secret=<client_secret>&redirect_uri=https://<redirectURL>/&code=<Your personal one-time code>
```
Response:
```
{
"access_token":  "access_token",
"token_type":  "bearer",
"refresh_token":  "refresh_token",
"expires_in":  1209599
}
```

access_token это ваш Bearer Access токен для запросов, требующих авторизации для OAuth2.0

***Важно!*** access_token имеет срок экспирации, по истечению которого вы можете обменять невалидную пару токенов на валидную используя refresh_token. refresh_token можно использовать только 1 раз и только по сроку истчения access_token в данной паре токенов.

Для рефреша пары токенов используйте данный запрос
```
https://hh.ru/oauth/token?grant_type=refresh_token&client_id=<client_id>&client_secret=<client_secret>&refresh_token=<refresh_token>
```
Response:
```
{
"access_token":  "access_token",
"token_type":  "bearer",
"refresh_token":  "refresh_token",
"expires_in":  1209599
}
```

### Первоначальная настройка проекта
#### Клонируем проект 
```
git clone https://github.com/kde2podfreebsd/HeadHunter-VacancyResponser.git
cd HeadHunter-VacancyResponser
```
#### Создаем виртуальное окружение и делаем настройку 
```
python -m venv venv
source venv/bin/activate
export PYTHONPATH=$PYTHONPATH:$(pwd)
```
#### Устанавливаем зависимости 
```
pip install -r requirements.txt
```

### Настраиваем конфиг
Заходим в config,json (через nano или vim если вы в CLI)
```
{  
	"items":[  
		{  
			"vacancy_id": 86786586,  
			"message": "Добрый день, {name}! Нас очень заинтересовало ваше резюме. Приглашаем вас зарегистрироваться на нашей платформе для помощи студентам: https://edumsg.org/?rid=9312da25f16e074c&ulp=https%3A%2F%2Fauthor24.expert%2Fauthors%2Fface%2F"  
		}  
	]  
}
```
Вот такой код, это один объект вакансии и сообщения для этой вакансии.
```
{  
	"vacancy_id": 86786586,  
	"message": "Добрый день, {name}! Нас очень заинтересовало ваше резюме. Приглашаем вас зарегистрироваться на нашей платформе для помощи студентам: https://edumsg.org/?rid=9312da25f16e074c&ulp=https%3A%2F%2Fauthor24.expert%2Fauthors%2Fface%2F"  
}
```
Добавляйте их в массив items для каждой вакансии.

##### Настройка имени!!!
Для автоматической подстановки имени пишите в текст сообщения ```{name}``` - скрипт будет его автоматически заменять.
Если не написать ``` {name} ``` , то скрипт проигнорирует подстановку имени и ошибки не будет, так что можно не указывать имя в сообщении для рассылки.

#### Запуск скрипта
```
python main.py
```


#### Шаблон tokens.json и .env
##### .env
```
client_id=
client_secret=
redirect_uri=https://
```
##### tokens.json
```json
{
  "access_token": "",
  "refresh_token": "",
  "expires_in": "2023-10-19 15:24:03.064206"
}
```
