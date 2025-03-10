import requests

class APIClient:
    BASE_URL = "https://reqres.in/api/users"

    @staticmethod
    def create_user(user_data: dict):
        """Envía una solicitud POST para crear un usuario"""
        response = requests.post(APIClient.BASE_URL, json=user_data)
        return response

