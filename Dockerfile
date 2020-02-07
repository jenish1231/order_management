FROM python:3

#environment variables
ENV PYTHONUNBUFFERED 1


WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
EXPOSE 5000

ENTRYPOINT [ "python" ]
CMD ["ordermanagement/app.py"]


