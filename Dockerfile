FROM python:3.8
RUN pip install flask
COPY app.py .
COPY marusya ./marusya
CMD [ "python", "./app.py" ]
