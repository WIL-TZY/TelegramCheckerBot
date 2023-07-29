# Price Checker
This is a python project that runs as a cron job with GitHub Actions on a daily basis. 

The purpose of this automation is to regularly check for price changes of certain electronic products on the web.

It's scheduled to run every 5 hours and runs a main loop to check the website constantly.
<!-- Log Console -->

<div align="center" >

#### L O G

</div>

```
>>> 2023-07-29 03:25:45 - __main__ - INFO - Running the routine. Loop count: 1
>>> 2023-07-29 03:25:46 - __main__ - DEBUG - Requisition status code: 403
>>> 2023-07-29 03:25:46 - __main__ - WARNING - Price element not found. Stopping the script.
>>> 2023-07-29 03:27:07 - __main__ - INFO - The script ran
>>> 2023-07-29 03:27:07 - __main__ - INFO - Running the routine. Loop count: 1
>>> 2023-07-29 03:27:14 - __main__ - DEBUG - Requisition status code: 200
```

You can check the full log in `status.log`.

## More Info

The `actions.yml` file can be found inside `.github/workflows/actions.yml`, it was taken from [this project](https://github.com/patrickloeber/python-github-action-template).

Check the `requirements.txt` file for pip third party packages to install.

<strong>Note:</strong> This project uses secret environment variables that only collaborators can see and use, but you can fork or clone the repo to make your own. 
