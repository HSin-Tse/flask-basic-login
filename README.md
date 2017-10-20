1. Install requisite packages:
```shell
$ pip install -r pip.txt
```
2. Create tables:
```shell
python3 manage.py init
python3 manage.py migtate
python3 manage.py upgrade

```
3. Run service:
```
python3 manage.py runserver
```