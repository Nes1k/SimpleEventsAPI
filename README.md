#Simple REST service

Connection parameters in file db.py
```python
con_params = {
    'db': '',
    'host': 'localhost',
    'user': '',
    'passwd': ''
}
```
Before run app you should create table
```sh
$ python app.py --migrate
```
Run app:
```sh
$ python app.py --run
```
Functionality:
- it’s possible to push new event to the top of the stream. 
- REST service consumes events in the form of a string
```
“I just won a lottery #update @all”
```
- parses them to JSON / Object format and stores somewhere.

- it’s possible to get 10 last events from the top of the stream
    * by category (#update, #poll, #warn)
    * by person (@all, @john, @all-friends)
    * by time

### Use with httpie
- Get event by id
```
http GET 127.0.0.1:8000/1/
```

- Add event item
```
http POST 127.0.0.1:8000/ event='I just won alottery #warn @john'
```

- Update event by id
```
http PUT 127.0.0.1:8000/1/ event='I just won alottery #update @all'
```

- Remove item by id
```
http DELETE 127.0.0.1:8000/1/
```

- Get last 5 event
```
http GET 127.0.0.1:8000/last/5/
```

- Get last by person
```
http GET 127.0.0.1:8000/person/john/0/
127.0.0.1:8000/person/{name}/{count}/
```

- Get last by category
```
http GET 127.0.0.1:8000/category/warn/0/
127.0.0.1:8000/category/{name-category}/{count}/
```

- Get all after
```
http GET 127.0.0.1:8000/time/150129/
127.0.0.1:8000/time/{%y%m%d}/
```

