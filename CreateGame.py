from locust import HttpUser, between, task


class user(HttpUser):
    wait_time = between(1,5)
    host = "https://test.group-and-games.prod.hudle.in/"

    @task(1)
    def Creategame(self):

        data ={
            "name": "Badminton",
            "desc": "This is for testing.",
            "per_player_share": 100.0,
            "no_of_participants": 2,
            "from": "2025-06-30 11:00:00",
            "to": "2025-06-30 12:00:00",
            "address": "Delhi",
            "latitude": 28.5535094,
            "longitude": 77.2670094,
            "venue_id": null,
            "sport_id": 2,
            "sport_category_id": 5,
            "is_paid": 1,
            "additional_fields": [
                0,
                1,
                3,
                2,
                4
            ],
            "skill_level_min": 5.0,
            "skill_level_max": 7.0,
            "tag_group_ids": [
                "01317891-d6b2-480c-8653-5b4609ef2d86"
            ],
            "users": [],
            "numbers": [],
            "access_type": 0,
            "type": 0,
            "place_id": null,
            "is_friendly": false
        }

        headers_auth = {

        }