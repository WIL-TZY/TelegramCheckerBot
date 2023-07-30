# Price Checker
This is a web scraper made with Python that runs as cron job with GitHub Actions on a daily basis.

The purpose of this automation is to regularly check for price changes of certain electronic products on selected websites. I'm using the ScrapingDog API to manage the HTTP Requests.

The workflow is scheduled to start running at 00:00 and re-runs every 5 hours. The program's main loop checks the website every hour.

If any price decrease is detected, the program triggers a Telegram bot that responds by sending a message to a private chat.

<div align="center" >

#### L O G

</div>

```
>>> 2023-07-30 17:59:10 - __main__ - INFO - Running the routine. Loop count: 4
>>> 2023-07-30 17:59:18 - __main__ - DEBUG - Requisition status code: 200
>>> 2023-07-30 18:59:07 - __main__ - INFO - Running the routine. Loop count: 5
>>> 2023-07-30 18:59:13 - __main__ - DEBUG - Requisition status code: 200
>>> 2023-07-30 19:59:05 - __main__ - INFO - Running the routine. Loop count: 6
>>> 2023-07-30 19:59:09 - __main__ - DEBUG - Requisition status code: 200
```

You can check the full log in [`status.log`](./status.log).

## More Info

The `actions.yml` file can be found inside `.github/workflows/actions.yml`, it was taken from [this project](https://github.com/patrickloeber/python-github-action-template).

Check the `requirements.txt` file for pip third party packages to install.

<strong>Note:</strong> This project uses secret environment variables that only collaborators can see and use, but you can fork or clone the repo to make your own. 

## Disclaimer
This program is for personal use only, which falls under fair use. This isn't, in any way, used for massive data share, large scale web scraping, nor commercial purposes. It runs in a fair rate limit in order to respect the website's policy.