from app import create_app
from app.cronjobs import run_daily_alerts

app = create_app()

with app.app_context():
    run_daily_alerts()
