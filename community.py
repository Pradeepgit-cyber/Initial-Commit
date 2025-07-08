from locust import HttpUser, between, task
from locust.user.inspectuser import print_task_ratio
from locust.web import logger


class user(HttpUser):
    wait_time = between(1,5)
    host = "https://test.api.hudle.in/"
    phone_number = "9034226868"
    otp_code = "48353"
    #auth_token = ""
    #header_with_Authtoken = ""

    headers_auth = {
        "Api-Secret": "hudle-api1798@prod",
        "x-app-id": "TP1A.220905.001",
        "Content-Type": "application/json"
    }

    def on_start(self):
        data_request = {
            "phone_number": self.phone_number,
            "type": "2"
        }
        headers_auth = {
            "Api-Secret": "hudle-api1798@prod",
            "x-app-id": "TP1A.220905.001",
            "Content-Type": "application/json"
        }

        with self.client.post("api/v1/otp/new", json=data_request, headers=headers_auth,
                              name="Request OTP") as response:
            if response.status_code in (200, 204):
                print("OTP Request API Pass")

            else:
                print("OTP Request API fail")
                print(response.text)
                logger.warning(response.text)
                return
        login_data = {
            "phone_number": self.phone_number,
            "code": self.otp_code,
            "type": "2"

        }

        with self.client.post("api/v1/otp/verify", json=login_data, headers=self.headers_auth, name="Verify OTP") as response:
            if response.status_code in (200,201):
                res_data= response.json().get("data")
                self.auth_token= res_data.get("token")
                header_with_Authtoken = headers_auth.copy()
                header_with_Authtoken['Authorization'] = f"Bearer {self.auth_token}"
                self.header_with_Authtoken = header_with_Authtoken

                print("Auth successful, token fetched.")
                print(self.auth_token)
                print(f"this is header: {self.header_with_Authtoken}")



            else:
                print("Failed to authenticate.")

                print(response.text)


    @task                       #create Game
    def Create_game(self, headers_with_token=None):
        game_data ={
            "name": "Badminton",
            "desc": "This is for testing.",
            "per_player_share": 100.0,
            "no_of_participants": 2,
            "from": "2025-06-30 11:00:00",
            "to": "2025-06-30 12:00:00",
            "address": "Delhi",
            "latitude": 28.5535094,
            "longitude": 77.2670094,
            "venue_id": None,
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
            "place_id": None,
            "is_friendly": False
        }

        url = "https://test.group-and-games.prod.hudle.in/api/v2/game/create"

        with self.client.post(url, json=game_data, headers=self.header_with_Authtoken,
                              name="Create Game") as response:
            if response.status_code in (200, 201):
                print("Game created successfully!")
                print("Game :  ", f"{response.json()}")
                print(game_data)
            else:
                print("Failed to create game")
                print(response.status_code, response.text)


    @task
    def create_groups(self):
        group_data = {
            "success": true,
            "code": 201,
            "data": {
                "id": "2374b8b4-2c62-424d-b8cb-0ae54694fb67",
                "name": "Padel Group",
                "address": "28, Okhla Phase III, Okhla Industrial Estate, New Delhi, Delhi 110020, India",
                "city": {
                    "id": 1,
                    "name": "Delhi",
                    "is_active": true
                },
                "sports": [
                    {
                        "id": 44,
                        "name": "Padel",
                        "photo": {
                            "small": "https://d1x0266vd61ta8.cloudfront.net/compressed/photos/sport/44/1750679155-1654175712-padel.png",
                            "normal": "https://d1x0266vd61ta8.cloudfront.net/original/photos/sport/44/1750679155-1654175712-padel.png"
                        }
                    }
                ],
                "type": 0,
                "skill_level": None,
                "description": "This is a optional field.",
                "members_count": 1,
                "games_count": 0,
                "upcoming_games_count": 0,
                "join_status": 0,
                "my_role": 1,
                "share_url": {
                    "url": "https://hudle.page.link/tPBCsbvYUte9KR4u8"
                },
                "latitude": 28.5535072,
                "longitude": 77.2670258,
                "is_active": 0
            }
        }

        url = "https://test.group-and-games.prod.hudle.in/api/v1/groups"
        with self.client.post(url,headers=self.header_with_Authtoken,name="Create_Group") as response:
            if response.status_code in (200, 201):
                print("Group created successfully!")
                print("Group :  ", f"{response.json()}")
                print(group_data)
            else:
                print("Failed to create group")
                print(response.status_code, response.text)


    @task                   #Community - my games
    def my_games(self):
        url = "https://test.group-and-games.prod.hudle.in/api/v2/users/my-games"

        with self.client.get(url,headers=self.header_with_Authtoken,name="mygames") as response:
            if response.status_code in (200, 201):
                print("List of my Created games")
                print("mygames :  ", f"{response.json()}")
            else:
                print("Failed to fetch my games")
                print(response.status_code, response.text)

    @task                  #Community - my groups
    def my_groups(self):
        url = "https://test.group-and-games.prod.hudle.in/api/v1/users/my-groups"

        with self.client.get(url,headers=self.header_with_Authtoken,name="mygroups") as response:
            if response.status_code in (200, 201):
                print("List of my groups")
                print("mygroups :  ", f"{response.json()}")
            else:
                print("Failed to fetch my groups")
                print(response.status_code, response.text)
                logger.info(response.json())


    @task               #Discover - Upcoming Games & Discover Groups
    def discover_list(self):
        url_groups = "https://test.group-and-games.prod.hudle.in/api/v2/users/discover/groups"  #Discover groups
        url_games = "https://test.group-and-games.prod.hudle.in/api/v2/users/discover/games"    #Upcoming games

        with self.client.get(url_groups,headers=self.header_with_Authtoken,name="discovergroups") as response:
            if response.status_code == 200 :
                print("List of Discovergroups")
                print("mygroup :  ", f"{response.json()}")
            else:
                print("Failed to fetch discover list")
                print(response.status_code, response.text)

        with self.client.get(url_games,headers=self.header_with_Authtoken,name="discover_games") as response:
            if response.status_code == 200 :
                print("List of discovergames")
                print("mygames :  ", f"{response.json()}")
            else:
                print("Failed to fetch discover list")
                print(response.status_code, response.text)



