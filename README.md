# Price Checker
This is a python project that runs as a cron job with GitHub Actions on a daily basis. 

The purpose of this automation is to regularly check for price changes of certain products on the web.

It's scheduled to start running at 12pm and re-checking the website every 5 hours.

<!-- Log Console -->
<div style="background-color: black; padding: 2%; border-radius: 5px 5px 0 0">
<span style="color: green; text-decoration: underline">>>> L O G</span>
</div>


<pre lang="text" style="color: green; background-color: black; padding: 5%; border-radius: 0 0 5px 5px">
# Contents of status.log
# Must be formatted to go here
</pre>

You can check the full log in `status.log`.

## More Info

The `actions.yml` file can be found inside `.github/workflows/actions.yml`, it was taken from [this project](https://github.com/patrickloeber/python-github-action-template).

Check the `requirements.txt` file for pip third party packages to install.

This project uses secret environment variables that only collaborators can see and use, but you can fork or clone the repo to make your own. 
