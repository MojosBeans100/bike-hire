# Battleships

## Portfolio Project 3 - Python Essentials

The purpose of this project was to build an interactive logic game for a user to play against the computer.

# Table of Contents
1. [Link to app](https://github.com/Michelle3334/battleships#link-to-app)
2. [Features](https://github.com/Michelle3334/battleships#features)
3. [Technologies Used](https://github.com/Michelle3334/battleships#technologies-used)
4. [Development](https://github.com/Michelle3334/battleships#development)
5. [Testing](https://github.com/Michelle3334/battleships#testing)
6. [Deployment](https://github.com/Michelle3334/battleships#deployment)
7. [Credits](https://github.com/Michelle3334/battleships#credits)
8. [Acknowledgements](https://github.com/Michelle3334/battleships#acknowledgements)

# Link to app
The app can be found <a href="https://battleships-py.herokuapp.com/" target="_blank" rel="noopener">here</a>. (Note: Right click on link to open a new tab).

<img src="images/program.PNG">

# Features
* The player can select grid size.
* The program warns the player if the input is invalid, and also if their input is off grid.
* The player inputs their name which is updated to a google sheet.
* Messages to the player are personalised with their name.
* The player is told what number player they are (information is obtained from the google sheet).
* Once all bombs are used the player can see where the ship was.
#### Future possible features
* Increased number ships depending on the grid size selected.
* Increased number of tries based on grid size.
* Option to play again once all tries used.
* Keep track of scores per player.

[Back to Table of Contents](https://github.com/Michelle3334/battleships#table-of-contents)

# Technologies Used:
### Programming Languages:
* Python
### Git
* Git was used for version control by utilizing the Gitpod terminal to commit to Git and Push to GitHub.
### Github
* GitHub is used to store the projects code after being pushed from Git.
### Lucidchart
* Lucidchart was used to map the workflow for the game.
<img src="images/workflow.PNG">

### Code Institutes mock terminal
* Code Institute provided a mock terminal for use for the project.
### Google Sheets
* Google Sheets was used to store the player names. The link to the sheet can be found <a href="https://docs.google.com/spreadsheets/d/1OPAWWCRL8g2KF1MZQvM3CO5YMLDQ9V1aOPwTJgWPhGc/edit#gid=0" target="_blank" rel="noopener">here</a>. (Note: Right click on link to open a new tab).

[Back to Table of Contents](https://github.com/Michelle3334/battleships#table-of-contents)

# Development
* In order to access google sheets I needed to import the gspread module and credentials from the google.oauth2.service_account.
* I wanted the battleship to be placed randomly on the game board, so for that functionality I imported the random library.
 
# Testing
## Functionality testing
* Each piece of code was tested in Gitpod as well as in Python Tutor (where possible).
* Family members and friends were asked to test the app once the final product was deployed.
## Code Validation
* The code was checked using Pep8online checker.
<img src="images/code-check.PNG">

[Back to Table of Contents](https://github.com/Michelle3334/battleships#table-of-contents)

# Deployment
The project was deployed to GitHub Pages using the following steps, I used Gitpod as a development environment where I commited all changes to git version control system. I used the push command in Gitpod to save changes into GitHub:

1. Log in to GitHub and locate the GitHub Repository.
2. At the top of the Repository, click on the "Settings" Button on the menu.
3. Scroll down the Settings page until you locate the "Pages" Section.
4. Under "Source", click the dropdown called "None" and select "Master Branch" and click on save.
5. The page will automatically refresh.
6. The now published site link shows at the top of the page.

The project was then deployed to Heroku using the following steps:

1. Log in to Heroku and add a new app.
2. Link the project from GitHub to Heroku.
3. Add the CREDS.JSON file to the ConfigVars in Settings.
4. Add the Python and NodeJS buildpacks.
5. Manually deploy the project (I used the manual deploy option in order to control what version was deployed to the live environment).

# Credits
* The code for the structure of the game board was adapted from the below example (right click to open in new tab).
https://codereview.stackexchange.com/questions/122970/python-simple-battleship-game
* Stackoverflow was great resource for answering questions I had. 

# Acknowledgements
* CSN tutors for their quick assistance.
* My mentor for support, advice and feedback.
* My friends and family for their support, feedback and user testing.

[Back to Table of Contents](https://github.com/Michelle3334/battleships#table-of-contents)
