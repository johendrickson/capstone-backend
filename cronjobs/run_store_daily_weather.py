from app import create_app
from cronjobs.store_daily_weather import fetch_and_store_daily_weather

app = create_app()

if __name__ == "__main__":
    with app.app_context():
        fetch_and_store_daily_weather()
        print("Finished fetching and storing daily weather.")
