# weather-api

Get simplified information about weather forecast
* [Website endpoint](https://django-weatherapi.herokuapp.com/weather-forecast/)

## Usage
* via ```GET``` request on the following endpoint: [https://django-weatherapi.herokuapp.com/weather-forecast/?date={YYYY-MM-DD}&country_code={ISO_CODE_2}](https://django-weatherapi.herokuapp.com/weather-forecast/?date={YYYY-MM-DD}&country_code={ISO_CODE_2})
* via [django management command](https://docs.djangoproject.com/en/3.2/howto/custom-management-commands/): ```python weather_api/manage.py weather_forecast 2021-06-16 CZ```

## License
* Developed under the [MIT](https://github.com/kucera-lukas/weather-api/blob/main/LICENSE) license
