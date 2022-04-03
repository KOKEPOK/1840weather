FROM python
RUN mkdir -p /Projects/1840pogoda/
WORKDIR /Projects/1840pogoda/

#EXPOSE 8000
#WORKDIR /usr/src/app

COPY . .

CMD ["python", "weather_api.py"]