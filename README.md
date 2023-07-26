# Price Checker
This is a python project that runs as a cron job with GitHub Actions on a daily basis. 

The purpose of this automation is to regularly check for price changes of certain products on the web.

It's scheduled to start running at 12pm and re-checking the website every 5 hours.

<!-- Log Console -->

<div align="center" >

#### L O G

</div>

```
>>> 2023-07-25 01:01:07 - __main__ - INFO - The script ran
>>> 2023-07-25 04:01:00 - __main__ - INFO - The script ran
>>> 2023-07-26 01:40:42 - __main__ - INFO - The script ran
```

You can check the full log in `status.log`.

## More Info

The `actions.yml` file can be found inside `.github/workflows/actions.yml`, it was taken from [this project](https://github.com/patrickloeber/python-github-action-template).

Check the `requirements.txt` file for pip third party packages to install.

<strong>Note:</strong> This project uses secret environment variables that only collaborators can see and use, but you can fork or clone the repo to make your own. 
