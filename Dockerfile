FROM python:3.7
COPY . /app
RUN pip install -r /app/requirements.txt
EXPOSE 8888
CMD python /app/main.py