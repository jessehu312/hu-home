from radar import RadarClient
from app import settings

radar_client = RadarClient(settings.RADAR_SECRET_KEY)