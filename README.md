# Functionality:
1. Registration
2. Authorization
3. Refill
4. Refund
5. Create Game
6. Buy Game

# How to run the system:
1. Clone code
2. Create venv and .env file with your secret key
3. Run "sudo docker-compose up"

# Unauthorized users can:
- Register: ("registraion/")
- Get their token: ("token/")

# Authorized users can:
- Check their profile: ("profile/")
- Refill the balance: ("deposit/")
- Check all deposits: ("deposits/")
- Refund money for specific deposit: ("rollback/<uuid:id>/")
- Create game: ("game/create/")
- Buy game: ("game/buy/")
