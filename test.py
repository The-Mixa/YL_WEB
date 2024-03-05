from requests import get, post, delete


# Проверка запроса get

print(get('http://localhost:800/api/v2/jobs').json())  # получение всех работ

print(get('http://localhost:800/api/v2/jobs/1').json())  # получение работы по id

print(get('http://localhost:800/api/jobs/v2/999').json())  # запрос id, которого нету в базе

#

#

# Проверка запроса post

# пустой запрос
print(post('http://localhost:800/api/v2/jobs', json={}).json())

# неполный запрос
print(post('http://localhost:800/api/v2/jobs',
           json={'job': 'работа'}).json())

# неверный ключ + неполный
print(post('http://localhost:800/api/v2/jobs',
           json={'wrong_key': 'job'}).json())

# корректный запрос
print(post('http://localhost:800/api/v2/jobs',
           json={'job': 'Работа 3',
                 'team_leader': 1,
                 'collaborators': '',
                 'work_size': 123,
                 'is_finished': False}).json())
#

#

# Проверка запроса delete

# список работ сначала
print(get('http://localhost:800/api/v2/jobs').json())

# некорректный | новости с id = 999 нет в базе
print(delete('http://localhost:800/api/v2/jobs/999').json())

# неверный формат
print(delete('http://localhost:800/api/v2/jobs/Victor').json())

# корректный
print(delete('http://localhost:800/api/v2/jobs/1').json())

# список работ в конце
print(get('http://localhost:800/api/v2/jobs').json())