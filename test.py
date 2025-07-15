import os
from dotenv import load_dotenv

load_dotenv()  # this loads the .env file


test = os.getenv("OPEN_API_KEY")
print(test)