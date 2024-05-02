import unittest
from TelegramBot.telegramBot import TelegramBot


def test_telegram_bot_basic():
    tb = TelegramBot()
    tb.send_message("https://victoria.craigslist.org/apa/d/victoria-micro-suite-min-walk-to-uvic/7646342302.html",
                    "MICRO-SUITE (5 min walk to UVic): Available Sep 1",
                    1200,
                    1,
                    1,
                    -1,
                    "Victoria",
                    "QR Code Link to This PostPrivate beautiful MICRO-suite (with separate entrance) in an owner-occupied quiet home.Available from Sep 1, 2023.Fully furnished with a private full bathroom and 2 closets.Small kitchenette area with a large countertop, sink, refrigerator, microwave, and portable induction cooktop. One Parking on driveway, and shared laundry (once/week).Rent: $1200/month for one year lease. Rent includes all utilities.5-8 min walk to UVic or Mt Doug High school. 1 min walk to Arbutus Middle. 5 min walk to take buses to anywhere in Victoria (#4, 7, 9, 11, 12, 13, 14, 15, 17, 26, 27 & 39).    Shopping nearby (Tuscany Village, University Heights, Cadboro Bay Village, Shelbourne Plaza).Located in the best, safe, beautiful, residential neighbourhood near beaches & parks! The suite is above ground, bright and attached to the side of the house (not in the basement).  No other tenants at home, only the two adult owners (full time working professionals) live in.MUST BE A NON-SMOKER! Strictly NO smoking, NO drugs, NO vaping anywhere!   NO parties, NO overnight visitors (as this is a micro-suite). NO pets. Sorry!Ideally suited for one person. Making light/simple meals without strong smells is possible, but not the right place for a cooking enthusiast.Inquiries with details about yourself are required  and will be responded to quickly.If the ad is up its available.",
                    1690102371.863059,
                    "craigslist",
                    1)




if __name__ == '__main__':
    unittest.main()
