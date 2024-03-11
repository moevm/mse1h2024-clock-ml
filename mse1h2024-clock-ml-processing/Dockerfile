FROM python

WORKDIR /app
COPY . /app

RUN pip install -r requirements.txt

EXPOSE 22869

CMD [ "python", "main.py" ]