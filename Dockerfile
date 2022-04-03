FROM python:3
COPY . .
WORKDIR /1840weather
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["weather_api.py"]