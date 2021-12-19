# Fampay Backend Assignment

This project was made as an assignment for github externship.
It is a django server which fetches youtube data and stores it and return to user when requested.
It is made using django , rest_framework.



## License

[MIT](https://choosealicense.com/licenses/mit/)

  
## Installation

* Make a virtual environment using virtualenv. You can install virtualenv using package manager.
```bash
  virtualenv venv
```
* Activat the virtualenv 
```bash 
source venv/bin/activate 
```
* Go inside the directory. `cd videolog`
* Install the required packages.
```bash
pip install -r requirements.txt
```
* Rename `.env.sample` to `.env`.
* Add the required fields. Multiple developer keys can be added by seperating them with a `,`
* You can use [https://djecrety.ir/] to generate your secret key
* After the above setup run.
```bash
python manage.py migrate
```
* Run the django server using
```bash
python manage.py runserver
```
It runs the backend server at default port 8000. As well schedules a job on a different thread to fetch youtube videos and store it in the database after specific intervals.
Open http://localhost:8000 to view it in the browser.

## Demo

Go to http://localhost:8000/videodata. \
You will see list of records sorted in descinding order.\
[API View](API_View.png) \
It is a template of rest framework. \
Click on filters. You will see a dialog which you can use to search or sort the data. \
The api is cursor based paginated. \
[Dialog Box](Filter_Dialog.png) \


  
## API Reference

#### Get videos

```http
  GET /videodata/
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `cursor` | `string` | Cursor for pagination|
| `ordering` | `string` | For sorting the data.|
| `search` | `string` | For searching the data.|

**srdering the following values**
* published
* title
* channel_name
Add `-` infront of it to make it descinding.

**search works on the following fields.**
* title
* description
* video_id


## Possible Improvements
Currently the server uses in memory caching. Considering the scope of the project it is fine. But we can shift to something like redis.
Only the cache settings needs to be changed inside the `settings.py` file.
