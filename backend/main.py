from http.server import HTTPServer, BaseHTTPRequestHandler
import json


class Handler(BaseHTTPRequestHandler):
    """Базовый Класс. 
    Принмает HTTP GET, POST, PATCH, DELETE запросы."""

    todo_id = 1
    database_json = {}
    
    def do_OPTIONS(self):
        """ Метод OPTIONS.
        Метод определяет разрешенные заголовки HTTP методов и настраивает CORS запросы.
        """        

        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, PATCH, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')  
        self.end_headers()
            

    def create_db(self):
        """ Метод create_db.
        Метод создает изначальный файлы с задачами - todos.json, и пользователяеми - users.json.
        Используются эти файлы в качестве базы данных, которые и будут редактироваться/удаляться. 
        """

        # Если изначально файла todos.json нет, то он создается и в него записывается первая задача
        # С базовой струрой данных.
        # В которой есть ID задачи, ID пользователя, создавшего задачу, название задачи и состояние - выполнена/не выполнена. 
        with open('./todos.json', 'a+') as file_todos:
            
            file_todos.seek(0)
            
            if file_todos.read() == '':

                database = {
                    "userId": 1,
                    "id": 1,
                    "title": "Первая задача",
                    "completed": True
                }

                file_todos.write(json.dumps([database], ensure_ascii=False, indent=4))

        # Так же создается файл с пользователяеми - users.json, если отсутствует. 
        # В файл записывается ID пользователя и его имя.
        with open('./users.json', 'a+') as file_users:
            
            file_users.seek(0)
            
            if file_users.read() == '':

                database_user = {
                    "id": 1,
                    "name": "Yan",
                }

                file_users.write(json.dumps([database_user], ensure_ascii=False, indent=4))


    def do_GET(self):
        """ Переопределение метода GET.
        Метод принимает GET запрос, и отдает json  фронтенду списки задач и пользователей.
        """
        
        self.create_db()

        if self.path == '/users':

            # Определяем заголовки запроса.
            self.send_response(200)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            # Открываем и Дессериализуем JSON из файла с пользователями.
            with open('./users.json', 'r', encoding='utf-8') as file:
            
                # Проводим Сериализацию и Дессериализию JSON.
                # И отправляем данные с пользователями на фронтенд.
                data = json.load(file)
            
                json_data = json.dumps(data)
                
                self.wfile.write(json_data.encode('utf-8'))
        

        if self.path == '/todos':

            # Определяем заголовки запроса.
            self.send_response(200)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            # Открываем и Дессериализуем JSON из файла с задачами.
            with open('./todos.json', 'r') as file:
                
                # Проводим Сериализацию и Дессериализию JSON.
                # И отправляем данные с задачами на фронтенд.
                data = json.load(file)
                
                json_data = json.dumps(data)
                
                self.wfile.write(json_data.encode('utf-8'))


    def do_POST(self):
        """ Переопределение метода POST.
        Метод принимает POST json запрос и записывает его в файл с задачами.
        """
        
        # Читаем данные и Дессериализуем JSON 
        length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(length).decode('utf-8')
        data_json = json.loads(post_data)

        
        # Открываем и Дессериализуем JSON из файла
        with open('./todos.json', 'r+') as file:
            
            data_file = json.load(file)
            
            # Индексируем ID в файле
            for index in data_file:

                index['id'] = self.todo_id
                self.todo_id += 1

            # Готовим новые данные для записи в файл
            self.database_json = {
            'userId': data_json['userId'],
            'id': self.todo_id,
            'title': data_json['title'],
            'completed': data_json['completed'],
            }
            
            # Обновляем данные, Сериализуем JSON и записываем новые данные в файл.
            data_file.append(self.database_json)
            json_file = json.dumps(data_file, ensure_ascii=False, indent=4)
            
            file.seek(0)
            file.write(json_file)

            # Отправляем обновленный файл
            self.wfile.write(json_file.encode('utf-8'))


    def do_PATCH(self):
        """ Переопределение метода PATCH.
        Метод принимает PATCH запрос с задачей. Статус которой необходимо изменить. 
        """
        
        # Получаем Индекс задачи из запроса.
        index_id = int(self.path[-1])


        # Читаем данные из запроса и проводим Дессериализацию JSON.
        content_length = int(self.headers['Content-Length'])
        patch_data = self.rfile.read(content_length)
        data = json.loads(patch_data.decode('utf-8'))

        
        # Читаем данные из файла с задачами
        with open('./todos.json', 'r') as file:

            existing_data = json.load(file)


        # Формируем новые данные
        self.database_json = {
        'userId': existing_data[index_id - 1]['userId'],
        'id': existing_data[index_id - 1]['id'],
        'title': existing_data[index_id - 1]['title'],
        'completed': data['completed'],
        }

        # Удаляем данные по Индексу и вставляем новую структуру.
        existing_data.pop(index_id - 1)
        existing_data.insert(index_id - 1, self.database_json)


        # Записываем новые данные
        with open('./todos.json', 'w') as file:
        
            json.dump(existing_data, file, ensure_ascii=False, indent=4)


        # готовим ответ
        json_response = json.dumps(existing_data)
            
        self.wfile.write(json_response.encode('utf-8'))


    def do_DELETE(self):
        """ Переопределение метода DELETE.
        Метод принимает ID задачи, которую необходимо удалить.
        """
        
        # Получаем ID из запроса.
        index_id = int(self.path[-1])


        # читаем данные из файла
        with open('./todos.json', 'r') as file:

            existing_data = json.load(file)


        # Удаляем данные по индексу
        existing_data.pop(index_id - 1)

        # Индексируем все объекты 
        self.todo_id = 1
        for index in existing_data:

            index['id'] = self.todo_id
            self.todo_id += 1

    
        # Записываем новые данные
        with open('./todos.json', 'w') as file:
        
            
            
            json_file = json.dumps(existing_data, ensure_ascii=False, indent=4)
            
            file.seek(0)
            file.write(json_file)

            # готовим ответ с новыми данными
            self.wfile.write(json_file.encode('utf-8'))



if __name__ == '__main__':

    # Запускаем HTTP Сервер для принятия запросов
    with HTTPServer(('127.0.0.1', 9000), Handler) as server:
        print('Сервер запущен и принимает запросы по адресу - http://127.0.0.1:9000')
        server.serve_forever()