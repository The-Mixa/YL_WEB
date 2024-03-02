from requests import get

print(get('http://localhost:800/api/jobs').json())  # получение всех работ

print(get('http://localhost:800/api/jobs/1').json())  # получение работы по id

print(get('http://localhost:800/api/jobs/999').json())  # запрос id, которого нету в базе

print(get('http://localhost:800/api/jobs/Victor').json())  # некорреектный запрос (строка)
