FROM python:3

#environment variables
ENV PYTHONUNBUFFERED 1
ENV FLASK_APP "ordermanagement/app.py"


WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
EXPOSE 5000
CMD flask run --host=0.0.0.0
