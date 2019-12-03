FROM python:3
ADD . /app
WORKDIR /app

RUN pip install -r requirements.txt
RUN pip install flask gunicorn
EXPOSE 8000
CMD ["gunicorn", "server:app", "-b",  "0.0.0.0:8000"]