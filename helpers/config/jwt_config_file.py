from os import getenv
from dotenv import load_dotenv
load_dotenv()

jwt_config = {
  "TOKEN_KEY": getenv("TOKEN_KEY"),
  "EXP_TIME_HRS": int(getenv("EXP_TIME_HRS")),
  "REFRESH_TIME_HRS": int(getenv("REFRESH_TIME_HRS"))
}
