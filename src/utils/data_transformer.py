from datetime import datetime

class DataTransformer:
    @staticmethod
    def transform_covid_data(raw_data):
        """Transform raw COVID data into the required format"""
        return {
            'timestamp': datetime.now().isoformat(),
            'country': raw_data.get('country', ''),
            'cases': raw_data.get('cases', 0),
            'deaths': raw_data.get('deaths', 0),
            'recovered': raw_data.get('recovered', 0),
            'active': raw_data.get('active', 0),
            'coordinates': {
                'latitude': raw_data.get('countryInfo', {}).get('lat', 0),
                'longitude': raw_data.get('countryInfo', {}).get('long', 0)
            }
        }