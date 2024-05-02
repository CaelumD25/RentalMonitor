import datetime
from time import sleep
import json
import telebot

from Database.sqlDatabase import SQL
from API.craigslist import digest_main_url as digest_craigslist
from API.kijiji import digest_main_url as digest_kijiji
from API.usedVic import digest_main_url as digest_vic_used
from TelegramBot.telegramBot import TelegramBot

_config = "cfg.json" # Location of the config file

def generate(database: SQL) -> None:
    """
    Generate data for all the rental sources
    :param database: SQL type object that holds the data for all the rentals
    :return: Nothing, adds to database in place
    """
    # Gets the data from the config file for the urls used for rental data
    with open(_config, "r") as config_file:
        config_data = json.load(config_file)

    # Process all the websites
    for current_website in ["craigslist","kijiji","vic_used"]:
        results = []
        # Process craigslist
        if current_website == "craigslist":
            results = digest_craigslist(config_data["websites"]["craigslist"])
        # Process kijiji
        elif current_website == "kijiji":
            results = digest_kijiji(config_data["websites"]["kijiji"])
        # Process Used Victoria
        elif current_website == "vic_used":
            results = digest_vic_used(config_data["websites"]["used"])
        for result_unit in results:
            if not database.unit_exists(unit=result_unit):
                result_unit.digest_url()
                database.add(unit=result_unit)
                sleep(1)


def send_messages(database: SQL, tb: TelegramBot) -> None:
    """
    Sends rentals that haven't been sent in the SQL database to the tb Telegram bot
    :param database: The database containing rental information
    :param tb: The telegram bot, pre-configured
    :return: returns nothing
    """
    # Processes every non-sent rental, non-sent rentals have a status of 0
    for row in database.get_new_additions():
        rental_id = row[0]
        date_time = row[1]
        host_website = row[2]
        url = row[3]
        title = row[4]
        cost = row[5]
        bedrooms = row[6]
        bathrooms = row[7]
        rental_size = row[8]
        location = row[9]
        description = row[10]
        # Verifies that the rental has not already been sent
        if database.has_been_sent(rental_id):
            print(f"Rental already sent, ID: {rental_id}")
            continue
        else:
            sleep(1)
            try:
                tb.send_message(url,
                                title,
                                cost,
                                bedrooms,
                                bathrooms,
                                rental_size,
                                location,
                                description,
                                date_time,
                                host_website)
                # Mark rental as sent in DB
                database.mark_sent_by_id(rental_id)
            except telebot.apihelper.ApiTelegramException as tele_exception:
                # Sending a message may fail for various reasons,
                # This will catch the error and try one more time, if it fails again it will attempt
                # Next generation loop
                print("Going too fast, waiting 5s\n", tele_exception)
                sleep(5)
                try:
                    tb.send_message(url,
                                    title,
                                    cost,
                                    bedrooms,
                                    bathrooms,
                                    rental_size,
                                    location,
                                    description,
                                    date_time,
                                    host_website)
                    # Mark rental as sent in DB
                    database.mark_sent_by_id(rental_id)
                except telebot.apihelper.ApiTelegramException:
                    return

def main():
    # Load initial configuration data
    while True:
        try:
            with open(_config, "r") as config_file:
                config_data = json.load(config_file)
            config_data["refresh_period"]
            break
        except AssertionError:
            print("No refresh period, waiting 300s")
            sleep(300)
        except IOError:
            print("File locked, waiting 300s")
            sleep(300)
        except KeyError as e:
            print("File likely empty, waiting 300s")
            sleep(300)
    # Configure Telegram Bot for Connecting to Specific Group Chat, see telegram docs for more details
    tb = TelegramBot(config_data["token"], config_data["chat_id"])

    # Connect to SQL Database
    sql_lite = SQL("Database/Rentals.db")

    # Set times so that bot does not run at night
    time_11pm = datetime.time(23, 0).hour  # 11 PM
    time_6am = datetime.time(6, 0).hour  # 6 AM
    print("Rental Monitoring Starting")
    # Run main loop
    while True:
        # Reload config every loop of application so that edits can change anything
        with open(_config, "r") as config_file:
            config_data = json.load(config_file)

        # Retrieve the delay between requests
        delay = config_data["refresh_period"] * 60
        # Get current time
        now = datetime.datetime.now().time().hour
        print(now)
        try:
            # If the current time is after 11pm or before 6am program suspends until time over
            if (now>=time_11pm or now<=time_6am) and False:
                print("Sleeping until morning")
                if now >= time_11pm:
                    sleep(3600*(time_6am+(24-time_11pm)))
                elif now <= time_6am:
                    sleep(3600*(time_6am-now))
                print("Good morning, monitoring resumed")
            # If current time is valid, generate data from websites and then send messages
            else:
                # Generate the data for each website and store it in the database
                generate(sql_lite)
                send_messages(sql_lite, tb)
                # Delay program so that requests aren't blocked and websites aren't overloaded
                print("Safe to stop")
                sleep(delay)
                print("Please wait for the \"Safe to stop\" message")
        except KeyboardInterrupt as ki_exception:
            print(f"Excepted due to keyboard interrupt", ki_exception)
            sql_lite.close()
            break
    print("Finished")

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
