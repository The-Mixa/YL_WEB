from requests import post

# пустой запрос
print(post('http://localhost:5000/api/news', json={}).json())

# неполный запрос
print(post('http://localhost:5000/api/news',
           json={'job': 'работа'}).json())

# неверный ключ + неполный
print(post('http://localhost:5000/api/news',
           json={'wrong_key': 'job'}).json())

# корректный запрос
print(post('http://localhost:5000/api/news',
           json={'job': 'Работа 3',
                 'team_leader': 1,
                 'collaborators': '',
                 'work_size': 123,
                 'is_finished': False}).json())
