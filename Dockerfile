FROM python:3.6.4
RUN pip install pynacl gevent requests
ENTRYPOINT ["python", "app.py"]