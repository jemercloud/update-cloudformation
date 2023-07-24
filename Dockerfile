FROM python:3

COPY requirements.txt /requirements.txt

RUN pip install -r requirements.txt

COPY update.py /update.py

CMD ["python", "/update.py"]