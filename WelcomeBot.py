import inflect
import praw
import prawcore
import prawcore.exceptions
import LoginInfo
import json
import time
import configparser

import logging
import logging.config
from layer7_utilities import LoggerConfig

botconfig = configparser.ConfigParser()
botconfig.read("botconfig.ini")

__botname__ = "Eulogy612-WelcomeBot"
__description__ = "Sets user flair in r/TheApexCollective. Made by /u/QuantumBrute"
__author__ = "/u/QuantumBrute"
__version__ = "1.0.0"
__dsn__ = botconfig.get("BotConfig", "DSN")

# Created by u/QuantumBrute


class Bot(object):
    def __init__(self):
        self.reddit = None
        self.canRun = False

        # Create the logger
        loggerconfig = LoggerConfig(__dsn__, __botname__, __version__)
        logging.config.dictConfig(loggerconfig.get_config())
        self.log = logging.getLogger("root")
        self.log.info("/*********Starting App*********\\")
        self.log.info("App Name: {} | Version: {}".format(__botname__, __version__))

        self.__init_configs()
        self.login()
        if self.canRun:
            self.subreddit = self.reddit.subreddit("TheApexCollective")

    def __init_configs(self):
        config = configparser.ConfigParser()
        config.read("/opt/skynet/Configs/config.ini")
        self.DatabaseName = "TheTraveler"
        self.DB_USERNAME = config.get("Database", "Username")
        self.DB_PASSWORD = config.get("Database", "Password")
        self.DB_HOST = config.get("Database", "Host")

    def login(self):
        try:
            self.reddit = praw.Reddit(
                client_id=LoginInfo.client_id,
                client_secret=LoginInfo.client_secret,
                username=LoginInfo.username,
                password=LoginInfo.password,
                user_agent=LoginInfo.user_agent,
            )
            self.log.info("Connected to account: {}".format(self.reddit.user.me()))
            self.canRun = True
        except Exception:
            self.log.exception("Failed to log in.")
            self.canRun = False

    def load_file(self, filename):
        try:
            with open(filename, "r") as infile:
                return json.load(infile)
        except Exception as err:
            self.log.exception(f"Error loading file '{filename}'. Err: {err}")

    def save_file(self, filename, data):
        try:
            with open(filename, "w") as outfile:
                json.dump(data, outfile, indent=2)
            self.log.info("User appended successfully!")
        except Exception as err:
            self.log.exception(f"Error saving file '{filename}'. Err: {err}")

    def unflaired(self):
        data = []
        itemname = []
        self.log.info("Looking for new and unflaired users...")
        info = self.load_file("LastApprovedUser.txt")

        n = len(info) + 1
        m = info[n - 2].get("Number")
        mnew1 = m + 1

        self.log.info(f"Current number of existing users: {m}")
        flag = 0

        checknew = 0
        for contributor1 in self.subreddit.contributor():
            for flair in self.subreddit.flair(redditor=contributor1):
                if flair.get("flair_text") is None:
                    self.log.info(f"Unflaired user found - {contributor1}")
                    itemname.append(contributor1)
                    checknew = 1
                else:
                    flag = 1
                    break
            if flag == 1:
                break
        itemname.reverse()
        if checknew == 1:
            for user in range(len(itemname)):
                # Initiate the inflect engine
                inflectengine = inflect.engine()
                # Convert the number (1, 5, etc) to words (1st, 5th, etc)
                current_num_text = inflectengine.ordinal(mnew1)
                newflair = f"Mortal ({current_num_text})"
                self.log.info(f"{itemname[user]} will be flaired: {newflair}")

                self.subreddit.flair.set(itemname[user], newflair)
                itemfinal = {"Name": str(itemname[user]), "Number": mnew1}
                data.append(itemfinal)
                mnew1 = mnew1 + 1
            self.save_file("LastApprovedUser.txt", data)

            self.log.info(f"New number of existing users: {mnew1 - 1}")

        elif flag == 1:
            self.log.info("No new users found!")

    def main(self):
        try:
            self.unflaired()
            time.sleep(60)

        except prawcore.exceptions.RequestException as err:
            self.log.warning(f"Reddit API error. Reddit may be unstable. Error: {err}")

        except praw.exceptions.APIException as err:
            self.log.exception(f"API Error! - Sleeping. Error: {err}")
            time.sleep(120)

        except praw.exceptions.ClientException as err:
            self.log.exception(f"PRAW Client Error! - Sleeping. Error: {err}")
            time.sleep(120)

        except prawcore.exceptions.ServerError as err:
            self.log.warning(f"PRAW Server Error! - Sleeping. Error: {err}")
            time.sleep(120)

        except prawcore.exceptions.NotFound as err:
            self.log.exception(f"PRAW NotFound Error! - Sleeping. Error: {err}")
            time.sleep(120)

        except KeyboardInterrupt:
            self.log.warning("Caught KeyboardInterrupt")
            self.canRun = False

        except Exception as err:
            self.log.critical(
                f"General Exception in main loop - sleeping 5 min. Error: {err}"
            )
            time.sleep(300)


if __name__ == "__main__":
    bot = Bot()

    while bot.canRun:
        bot.main()
