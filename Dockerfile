FROM python:3

#environment variables
ENV PYTHONUNBUFFERED 1
ENV FLASK_APP "ordermanagement/app.py"

WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
EXPOSE 5000

RUN chmod +x run.sh
# RUN chmod u+x wait-for-it.sh

# CMD ["/bin/bash","run.sh"]