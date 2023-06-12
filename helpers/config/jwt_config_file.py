import os
from dotenv import load_dotenv
load_dotenv()

jwt_config = {
  "TOKEN_KEY": os.getenv("TOKEN_KEY"),
  "EXP_TIME_HRS": int(os.getenv("EXP_TIME_HRS")),
  "REFRESH_TIME_HRS": int(os.getenv("REFRESH_TIME_HRS"))
}