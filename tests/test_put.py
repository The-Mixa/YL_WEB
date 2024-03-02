from requests import get, put

# новость сначала
print(get('http://localhost:800/api/jobs/2').json())

# пустой запрос
print(put('http://localhost:800/api/jobs/2', json={}).json())

# неполный запрос
print(put('http://localhost:800/api/jobs/2',
           json={'job': 'работа'}).json())

# неверный ключ + неполный
print(put('http://localhost:800/api/jobs/2',
           json={'wrong_key': 'job'}).json())

# корректный запрос
print(put('http://localhost:800/api/jobs/2',
           json={'job': 'Работа 1',
                 'team_leader': 1,
                 'collaborators': '',
                 'work_size': 123123,
                 'is_finished': False}).json())


# новость в конце
print(get('http://localhost:800/api/jobs/2').json())
