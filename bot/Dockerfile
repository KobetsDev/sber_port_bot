FROM python:3.10

WORKDIR /usr/src/tg_oso

COPY . .

RUN pip install -r requirements.txt
RUN echo "create logs\n" > logs.log
CMD ["python", "app.py"]