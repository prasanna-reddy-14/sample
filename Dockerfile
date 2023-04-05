
FROM python:3.9



WORKDIR /app


COPY . .


RUN pip install -r requirements.txt



COPY . .


ENV FLASK_APP app.py
ENV FLASK_ENV production
ENV SECRET_KEY=your_secret_key_here


EXPOSE 5000


CMD ["flask", "run", "--host", "0.0.0.0"]

