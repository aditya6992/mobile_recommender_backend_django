# mobile_recommender_backend_django
provides top 10 mobiles based on importance ranking given by user for each specification of mobile

you need mongoDB up and running and pymongo installed in your system
scrape gsmarena using scraper.py

```python scraper.py```

then run
```python manager.py runserver```

example request:

```http://localhost:8000/?camera=10&ram=10&storage=10&battery=10```

where camera, ram, storage and battery have corresponding ranking given by user
