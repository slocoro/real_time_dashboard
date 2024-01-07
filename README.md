A simple tutorial real-time dashboard using Kafka and Pinot.

To Run

Set-up env:
```
python -m venv venv && venv/bin/activate
pip install -r requirements.txt
```

Set-up infra:
```
docker-compose up
```

Start fake events producer:
```
python consumer.py
```

Start dashboard:
```
streamlit run streamlit/app.py
```

Navigate to localhost:8501 to view dashboard.

