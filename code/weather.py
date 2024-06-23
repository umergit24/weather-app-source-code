from flask import Flask, request, render_template
import requests
import datetime as dt

app = Flask(__name__)

# Your API Key
API_KEY = '007d68128ef4ec788f611c7c0cc7f68a'

@app.route('/', methods=["POST", "GET"])
def search_city():
    if request.method == "POST":
        city = request.form.get("city")
        if city == "" or len(city) <= 1:
            error_message = "City is required."
            return render_template("weather.html", error_message=error_message)

        units = 'Metric'
        url = f'http://api.openweathermap.org/data/2.5/forecast?q={city}&APPID={API_KEY}&units={units}'
        response = requests.get(url).json()

        if response["cod"] != "200":
            error_message = "City not found."
            return render_template("weather.html", error_message=error_message)

        forecast_data = response["list"]
        forecast = []
        for item in forecast_data:
            forecast_date = dt.datetime.fromtimestamp(item["dt"]).strftime('%d-%m-%Y')
            forecast_temp = item["main"]["temp"]
            forecast_desc = item["weather"][0]["description"]
            forecast_icon = item["weather"][0]["icon"]
            forecast.append({"date": forecast_date, "temp": forecast_temp, "desc": forecast_desc, "icon": forecast_icon})

        return render_template("weather.html", city=city, forecast=forecast)

    return render_template("weather.html")


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=3000, debug=True)