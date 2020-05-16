# Ethic-Blueprint Backend Server
A Python/Flask server to interface with our PostGreSQL database hosted on Heroku :)
- [General Backend Documentation](https://docs.google.com/document/d/1BplZcAn_fgPt9aQVchITaTtT2rrt0Mwa7w4oRuVK54w/edit#)
- [Scraper Documentation](https://docs.google.com/document/d/15sDqXgBlSW3cUScGSam7tZL6wnTwM-fWL0KoXvZTh-w/edit)
## Getting Started
- Set up the Heroku CLI on your computer: [Instructions](https://devcenter.heroku.com/categories/command-line)
## Accessing the PSQL Database Directly
- To access the database on your terminal, open it up and type these commands:
  - `heroku login`
  - `heroku pg:psql -a ethic-blueprint`
- To exit from the database, type `\q` while you are in the database.
## Making Changes to this Repo
- First, clone the repo if you haven't already
  - `git clone https://github.com/uciblueprint/Ethics-Project-Server`
- Next, make your changes in any code editor
- After you're done, test your changes locally by running this command:
  - `python app.py`
  - If your Mac defaults to Python 2 for some reason, make sure you're running Python 3 by doing this command:
  - `python3 app.py`
- This should start up your server on localhost:5000. In another terminal window, you can try running this command to test the default endpoint:
  - `curl localhost:5000/`
  - This should return 'Hello World!'
- After you've tested your changes locally, you're ready to update the repo. Type these commands in your terminal, while you're in the working directory for this repo:
  - `git add .` (This adds all files you made changes to. If you only want to add a certain file for some reason, do `git add file-name`)
  - `git commit -m "write what you updated or changed"` (Commit your changes and write a relevant message pertaining to your changes)
  - `git push origin master` (Updates our GitHub repo and deploys to Heroku automatically!)
  - We have it set up so that any updates to the `master` branch on this repo will trigger a deploy on Heroku and update the server.
