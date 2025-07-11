from locust import HttpUser, between, task
from locust.user.inspectuser import print_task_ratio
from locust.web import logger

from Creategame import Create_game
from Creategroup import create_group


class user(HttpUser):
    wait_time = between(1,5)
    host = "https://test.api.hudle.in/"
    phone_number = "8888888888"
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
                              name="Request_OTP") as response:
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


    @task                       #Community - create Game
    def Create_game(self, headers_with_token=None):
        game_data = Create_game(self)

        url = "https://test.group-and-games.prod.hudle.in/api/v2/game/create"

        with self.client.post(url, json=game_data, headers=self.header_with_Authtoken,
                              name="Create_Game") as response:
            if response.status_code in (200, 201):
                print("Game created successfully!")
                print("Game :  ", f"{response.json()}")
                print(game_data)

            else:
                print("Failed to create game")
                print(response.status_code, response.text)
                logger.info(response.json())


    @task             #Community - Create Group
    def create_groups(self):
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


    @task                   #Community - my games
    def my_games(self):
        url = "https://test.group-and-games.prod.hudle.in/api/v2/users/my-games"

        with self.client.get(url,headers=self.header_with_Authtoken,name="my_games") as response:
            if response.status_code in (200, 201):
                print("List of my Created games")
                print("mygames :  ", f"{response.json()}")
            else:
                print("Failed to fetch my games")
                print(response.status_code, response.text)

    @task                  #Community - my groups
    def my_groups(self):
        url = "https://test.group-and-games.prod.hudle.in/api/v1/users/my-groups"

        with self.client.get(url,headers=self.header_with_Authtoken,name="my_groups") as response:
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

        with self.client.get(url_groups,headers=self.header_with_Authtoken,name="discover_groups") as response:
            if response.status_code in (200,201):
                print("List of Discovergroups")
                print("mygroup :  ", f"{response.json()}")
            else:
                print("Failed to fetch discover list")
                print(response.status_code, response.text)

        with self.client.get(url_games,headers=self.header_with_Authtoken,name="Upcoming_games") as response:
            if response.status_code in (200,201):
                print("List of discovergames")
                print("mygames :  ", f"{response.json()}")
            else:
                print("Failed to fetch discover list")
                print(response.status_code, response.text)


    @task            #All sports
    def sports_all(self):
        url = "https://test.group-and-games.prod.hudle.in/api/v2/sport/all"
        with self.client.get(url,headers=self.header_with_Authtoken,name="sport_all") as response:
            if response.status_code == 200:
                print("All sports")
                print("sportsall : ", f"{response.json()}")
            else:
                print("All sports API Failed")
                print(response.status_code, response.text)


    @task        #Fcm Token
    def Fcm(self):
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


    @task          #User_Friends
    def user_friends(self):
        url = "https://test.group-and-games.prod.hudle.in/api/v2/user-friends"
        with self.client.get(url,headers=self.header_with_Authtoken,name="/user-friends") as response:
            if response.status_code in (200,201):
                print("List of Friends")
                print("userfriends : ", f"{response.json()}")
            else:
                print("No Data")
                print(response.status_code, response.text)


    @task           #people-you-may-know
    def people_you_may_know(self):
        url = "https://test.group-and-games.prod.hudle.in/api/v2/user-friends/people-you-may-know"
        with self.client.get(url,headers=self.header_with_Authtoken,name="/user-friends/people-you-may-know") as response:
            if response.status_code in (200,201):
                print("List of people")
                print("people_you_may_know : ", f"{response.json()}")
            else:
                print("No data")
                print(response.status_code, response.text)

    @task        #user-location
    def user_location(self):
        url = "https://test.hudle.in/api/v1/user-loction"
        with self.client.put(url,headers=self.header_with_Authtoken,name="user-location") as response:
            if response.status_code in (200,201):
                print("Location Updated")
                print("user-location : ", f"{response.json()}")
            else:
                print("Location update Failed")
                print(response.status_code,response.text)


    @task      #player-rating
    def player_rating(self):
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


    @task     #additional-fields
    def additional_fields(self):
        url = "https://test.group-and-games.prod.hudle.in/api/v2/game/additional-fields"
        with self.client.get(url,headers=self.header_with_Authtoken,name="additional-fields") as response:
            if response.status_code in (200,201):
                print("Response passed")
                print("additional-fields : ", f"{response.json()}")
            else:
                print("Response failed")
                print(response.status_code,response.text)


    @task       #game_details
    def game_details(self):
        url = "https://test.group-and-games.prod.hudle.in/api/v2/matches/game/7da50cb0-446b-4bd4-a564-0103f0331ab5"
        with self.client.get(url,headers=self.header_with_Authtoken,name="game_details") as response:
            if response.status_code in (200,201):
                print("Game details response passed")
                print("game_details : ", f"{response.json()}")
            else:
                print("Game detail response failed")
                print(response.status_code,response.text)


    @task       #game_gameId_users
    def game_gameId_users(self):
        url = "https://test.group-and-games.prod.hudle.in/api/v2/game/7da50cb0-446b-4bd4-a564-0103f0331ab5/users"
        with self.client.get(url,headers=self.header_with_Authtoken,name="game_gameId_users") as response:
            if response.status_code in (200,201):
                print("Successfully fetched")
                print("game_gameId_users : ", f"{response.json()}")
            else:
                print("user details failed")
                print(response.status_code,response.text)


    @task       #game/gameID
    def game_gameId(self):
        url = "https://test.group-and-games.prod.hudle.in/api/v2/game/7da50cb0-446b-4bd4-a564-0103f0331ab5"
        with self.client.get(url,headers=self.header_with_Authtoken,name="game/gameID") as response:
            if response.status_code in (200,201):
                print("GameID successfully fetched")
                print("game_ID : ", f"{response.json()}")
            else:
                print("User ID response failed")
                print(response.status_code,response.text)

















