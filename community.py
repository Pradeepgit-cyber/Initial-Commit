from locust import HttpUser, between, task
from locust.web import logger

from Creategame import Create_game
from Creategroup import create_group

class user(HttpUser):
    wait_time = between(1,5)
    host = "https://test.api.hudle.in/"
    phone_number = "8888888888"
    otp_code = "48353"

    headers_auth = {
        "Api-Secret": "hudle-api1798@prod",
        "x-app-id": "TP1A.220905.001",
        "Content-Type": "application/json"
    }

    def on_start(self):
        self.game_id = None  # Will hold created game UUID

        data_request = {
            "phone_number": self.phone_number,
            "type": "2"
        }
        headers_auth = self.headers_auth

        with self.client.post("api/v1/otp/new", json=data_request, headers=headers_auth, name="Request_OTP") as response:
            if response.status_code in (200, 204):
                print("OTP Request API Pass")
                logger.warning("OTP Request API PASS")
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

        with self.client.post("api/v1/otp/verify", json=login_data, headers=self.headers_auth, name="Verify_OTP") as response:
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

    def _create_game(self):
        game_data = Create_game(self)
        url = "https://test.group-and-games.prod.hudle.in/api/v2/game/create"
        with self.client.post(url, json=game_data, headers=self.header_with_Authtoken, name="Create_Game") as response:
            if response.status_code in (200, 201):
                print("Game created successfully!")
                data = response.json()
                print("Game :  ", data)
                print(game_data)
                # Extract the game_uuid from the response and store it
                self.game_id = None
                if isinstance(data, dict):
                    if "data" in data and isinstance(data["data"], dict):
                        self.game_id = data["data"].get("game_uuid")
                    elif "game_uuid" in data:
                        self.game_id = data.get("game_uuid")
                print(f"Created game_id (game_uuid): {self.game_id}")
            else:
                print("Failed to create game")
                print(response.status_code, response.text)
                logger.info(response.text)

    def _create_groups(self):
        group_data = create_group(self)
        url = "https://test.group-and-games.prod.hudle.in/api/v1/groups"
        with self.client.post(url,json=group_data,headers=self.header_with_Authtoken,name="Create_Group") as response:
            if response.status_code in (200, 201):
                print("Group created successfully!")
                print("Group :  ", f"{response.json()}")
                print(group_data)
            else:
                print("Failed to create group")
                print(response.status_code, response.text)

    def _my_games(self):
        url = "https://test.group-and-games.prod.hudle.in/api/v2/users/my-games"
        with self.client.get(url,headers=self.header_with_Authtoken,name="my_games") as response:
            if response.status_code in (200, 201):
                print("List of my Created games")
                print("mygames :  ", f"{response.json()}")
            else:
                print("Failed to fetch my games")
                print(response.status_code, response.text)

    def _my_groups(self):
        url = "https://test.group-and-games.prod.hudle.in/api/v1/users/my-groups"
        with self.client.get(url,headers=self.header_with_Authtoken,name="my_groups") as response:
            if response.status_code in (200, 201):
                print("List of my groups")
                print("mygroups :  ", f"{response.json()}")
            else:
                print("Failed to fetch my groups")
                print(response.status_code, response.text)
                logger.info(response.text)

    def _discover_list(self):
        url_groups = "https://test.group-and-games.prod.hudle.in/api/v2/users/discover/groups"
        url_games = "https://test.group-and-games.prod.hudle.in/api/v2/users/discover/games"

        # Fetch discover groups
        with self.client.get(url_groups,headers=self.header_with_Authtoken,name="discover_groups") as response:
            if response.status_code in (200,201):
                print("List of Discovergroups")
                print("mygroup :  ", f"{response.json()}")
            else:
                print("Failed to fetch discover list")
                print(response.status_code, response.text)

        # Fetch discover games (no longer needed for game_id)

    def _sports_all(self):
        url = "https://test.group-and-games.prod.hudle.in/api/v2/sport/all"
        with self.client.get(url,headers=self.header_with_Authtoken,name="sport_all") as response:
            if response.status_code == 200:
                print("All sports")
                print("sportsall : ", f"{response.json()}")
            else:
                print("All sports API Failed")
                print(response.status_code, response.text)

    def _Fcm(self):
        fcm_data = {
            "fcm_id": "fZQ4_PM5QYGySRludrgdu4:APA91bHUpqolzFiNoctp6On0mYv7eGvbFycx9yUjkRzvzgNF-MPsQqVXEQB8kBOah7dqs5pMeGrItTAW5Ceca43lDqkYryDZ9EpChjB1MJ-tObBKo79x1x4"
        }
        url = "https://test.api.hudle.in/api/v1/user/fcm"
        with self.client.post(url,json=fcm_data,headers=self.header_with_Authtoken,name="Fcm_token") as response:
            if response.status_code == 200:
                print("FCM Token Pass")
                print("Fcm token : ", f"{response.json()}")
            else:
                print("Fcm token failed")
                print(response.status_code,response.text)

    def _user_friends(self):
        url = "https://test.group-and-games.prod.hudle.in/api/v2/user-friends"
        with self.client.get(url,headers=self.header_with_Authtoken,name="/user-friends") as response:
            if response.status_code in (200,201):
                print("List of Friends")
                print("userfriends : ", f"{response.json()}")
            else:
                print("No Data")
                print(response.status_code, response.text)

    def _people_you_may_know(self):
        url = "https://test.group-and-games.prod.hudle.in/api/v2/user-friends/people-you-may-know"
        with self.client.get(url,headers=self.header_with_Authtoken,name="/user-friends/people-you-may-know") as response:
            if response.status_code in (200,201):
                print("List of people")
                print("people_you_may_know : ", f"{response.json()}")
            else:
                print("No data")
                print(response.status_code, response.text)

    def _user_location(self):
        url = "https://test.hudle.in/api/v1/user-loction"
        with self.client.put(url,headers=self.header_with_Authtoken,name="user-location") as response:
            if response.status_code in (200,201):
                print("Location Updated")
                print("user-location : ", f"{response.json()}")
            else:
                print("Location update Failed")
                print(response.status_code,response.text)

    def _player_rating(self):
        url = "https://test.group-and-games.prod.hudle.in/api/v2/users/player-rating"
        params = {
            "sport_category_id" : 2
        }
        with self.client.get(url,headers=self.header_with_Authtoken,name="player-rating",params=params) as response:
            if response.status_code in (200,201):
                print("Successfull")
                print("player-rating : ", f"{response.json()}")
            else:
                print("Failed")
                print(response.status_code,response.text)

    def _additional_fields(self):
        url = "https://test.group-and-games.prod.hudle.in/api/v2/game/additional-fields"
        with self.client.get(url,headers=self.header_with_Authtoken,name="additional-fields") as response:
            if response.status_code in (200,201):
                print("Response passed")
                print("additional-fields : ", f"{response.json()}")
            else:
                print("Response failed")
                print(response.status_code,response.text)

    def _game_details(self):
        if not self.game_id:
            print("No game_id available for game_details!")
            return
        url = f"https://test.group-and-games.prod.hudle.in/api/v2/matches/game/{self.game_id}"
        with self.client.get(url, headers=self.header_with_Authtoken, name="game_details") as response:
            if response.status_code in (200,201):
                print("Game details response passed")
                print("game_details : ", f"{response.json()}")
            else:
                print("Game detail response failed")
                print(response.status_code,response.text)

    def _game_gameId_users(self):
        if not self.game_id:
            print("No game_id available for game_gameId_users!")
            return
        url = f"https://test.group-and-games.prod.hudle.in/api/v2/game/{self.game_id}/users"
        with self.client.get(url, headers=self.header_with_Authtoken, name="game_gameId_users") as response:
            if response.status_code in (200,201):
                print("Successfully fetched")
                print("game_gameId_users : ", f"{response.json()}")
            else:
                print("user details failed")
                print(response.status_code,response.text)

    def _game_gameId(self):
        if not self.game_id:
            print("No game_id available for game_gameId!")
            return
        url = f"https://test.group-and-games.prod.hudle.in/api/v2/game/{self.game_id}"
        with self.client.get(url, headers=self.header_with_Authtoken, name="game/gameID") as response:
            if response.status_code in (200,201):
                print("GameID successfully fetched")
                print("game_ID : ", f"{response.json()}")
            else:
                print("User ID response failed")
                print(response.status_code,response.text)

    @task
    def all_in_sequence(self):
        self._create_game()       # <-- This will set self.game_id for next steps
        self._create_groups()
        self._my_games()
        self._my_groups()
        self._discover_list()     # <-- No longer fetches game_id
        self._sports_all()
        self._Fcm()
        self._user_friends()
        self._people_you_may_know()
        self._user_location()
        self._player_rating()
        self._additional_fields()
        self._game_details()      # <-- These will use the created game_id
        self._game_gameId_users()
        self._game_gameId()