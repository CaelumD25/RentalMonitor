# Rental Monitor

This project is about saving immense amounts of stress from constantly checking postings from websites used to commonly post rentals in BC.

It works by checking each website on a set interval, and then sending that information to a telegram bot which can update you on any new postings.

In order to get the bot to work, you will need a config file in the form of the following

```json
{
  "websites": {
    "craigslist": "https://victoria.craigslist.org/search/apa?max_bedrooms=1&max_price=1200&min_bedrooms=0&min_price=850&postal=V2S4L6&search_distance=8.75&sort=date#search=1~thumb~0~0",
    "kijiji": "https://www.kijiji.ca/b-apartments-condos/abbotsford/1+bedroom__bachelor+studio/c37l1700140a27949001?radius=14.0&price=850__1200&address=Eleanor+Avenue%2C+Abbotsford%2C+BC&ll=49.0391224%2C-122.2669024",
    "used": "https://www.usedfraservalley.com/real-estate-rentals?r=abbotsfordmission&ca=%7B%227%22%3A%5B%220%22,%221%22%5D%7D&priceTo=1200&priceFrom=850"
  },
  "token": "<token here>",
  "refresh_period": 60,
  "chat_id": "<chat id here>"
}
```