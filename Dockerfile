FROM python
RUN mkdir -p /Projects/1840weather/
WORKDIR /Projects/1840weather/

COPY . .

CMD ["python", "weather_api.py"]