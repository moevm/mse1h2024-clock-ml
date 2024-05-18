FROM python

WORKDIR /app

RUN pip install torch>=2.2.0
RUN pip install easyocr==1.7.1

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . /app

EXPOSE 745

CMD [ "python", "main.py" ]