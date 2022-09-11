# Requirements:
The whole system must be implemented using REST API JSON.

# Functionality:
1. Registration
2. Authorization
3. Refill
4. Refund
5. Create Game
6. Buy Game

# How to run the system(Linux):
1. Clone code 
3. Create virtual enviroment and .env file with your Django secret key
4. Run "cd gameproject"
5. Run "sudo docker-compose up"

# Unauthorized users can:
- Register: ("registraion/")
- Get their token: ("token/")

# Authorized users can:
(The following methods work only with the "Bearer &lt;your access token&gt;", which must be in the header "Authorization")
- Check their profile: ("profile/")
- Refill the balance: ("deposit/")
- Check all deposits: ("deposits/")
- Refund money for specific deposit: ("rollback/<uuid:id>/")
- Create game: ("game/create/")
- Buy game: ("game/buy/")
