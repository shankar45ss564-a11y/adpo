with DAG("orders_daily") as dag:
    ingest = PythonOperator(...)
    transform = PythonOperator(...)
    quality = PythonOperator(...)

    ingest >> transform >> quality
