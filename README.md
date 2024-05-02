# Cheer Up!
#### Video Demo: https://youtu.be/AQ14U8hyvK4
#### Description: A mini Web app made to bring people together and help each other through hard times.
## Purpose of the Webapp
I'm Tony from Myanmar. With the Covid Crisis and the Military Coup in our country, the number of people around the globe and from Myanmar struggling with mental health issues has skyrocketed. Thus, emotional support to help each other through their hardships is needed now more than ever. Though some people might have friends, families, and loved ones to turn to for emotional support, there are people not fortunate enough to have someone by their side during the darkest times of their lives. The major purpose of this web app is to provide people in that situation— as well as everyone else, of course— the feeling that someone is there for them, giving them strength and encouragement to carry on with their lives.

## Technologies Used
 - HTML
 - CSS
 - Bootstrap
 - JavaScript
 - Python(Flask)
 - SQLite

## Development Environment of the App
For this web app, I tried getting out of my comfort zone and avoided using CS50 codespace, intending to learn about the requirements and experience in developing a web app from scratch. I tried developing the app on my local machine, which is running Windows OS, and it turned out to be a huge burden just to set up and install the dependencies required for the app. With the advice of Jaiden from the CS50 discord community, I decided to do developments and install dependencies using the WSL as my working environment, inside which I used virtual environments to install the required python modules for the app.

 ## General Structure of the Program
For this project, instead of getting my hands on new technologies, I used this as an opportunity to take a deeper dive into the topics I've learnt from the course and implement them in this project. I used Flask as a backend Python framework, SQLite as a database engine, HTML, CSS, and Bootstrap for design purposes, and a bit of Javascript for functionality. The project folder layout is structured according to the Flask Folder system with the python modules installed within the virtual environment. Though the program is fairly minimalistic in design and has limited functionalities, I've built the app compact enough to serve its purpose and not overwhelm users with unnecessarily sophisticated features and ‌designs.

## Parts of the Program
There are mainly three parts to the program when abstracted.
1. Login
2. Sign-Up
3. Home

In terms of templates, there's one extra HTML file (layout.html) in addition to the three templates for each individual part of the program, containing the components required to be rendered on every program template, such as link tags, navbar, and footer.

### **1. Login**
 Whenever a user tries to access the web app, this is the first route that they will be directed to before being able to use any functionalities of the app.

The Login page accepts two HTTP methods, 'Get' and 'Post'. When the users request the Login page, the program will render the login HTML file, prompting them to enter the username and password they used during sign-up. Upon submission of the user's username and password, the program checks the inputted credentials against the credentials from the 'users' table of the SQLite database 'data.db', which are recorded during the user sign-up. If the sign-in was unsuccessful i.e. the user inputs the incorrect credentials, the user isn't registered, or one of the input boxes is left blank, the program will display the appropriate alert messages, but if the log-in was successful, the log of  the users will be remembered using Flask session and will be redirected towards the homepage of the app.

What if the users aren't signed up? No worries! They can do so by pressing the "Sign-Up" button, and they will be redirected right towards the sign-up page.

### **2. Sign-Up**

The Sign-Up page also accepts two HTTP methods, "Get" and "Post". When the user sends a request, they will be presented with this great-looking page, where they will be prompted to enter all the required inputs to be successfully registered into the database. The password inputted are hashed using the (generate_password_hash) function from Flask before saving them in a database, enhancing the security and reducing the risk of exposing users' passwords to adversaries. Once the user is successfully registered, the program will insert all the credentials inside the "user" table in data.db, use Flask sessions to remember the log-in activity of the user and redirect them to the Homepage.

### **3. Home**
This is where all the magic happens. I designed the application to hide the components keeping the design nice and simple, limiting the startup rendering to just two elements—the greeting and the mood choice. The software will first greet the user by retrieving their name from the database and saying "Hello." Then there is the mood selector, which offers several moods for them to select from. Depending on the mood they select, the JavaScript function that was built will display a variety of items on the website.

### Cheering Others Up
The program will display an input box where the user can type a message to cheer up people who are unhappy, lonely, or depressed if they choose the "Happy" mood. Following submission, the user's message will be added to the database's "messages" table and a "Thank You" message will be presented to show appreciation for their contribution.

### Cheering Yourself Up
If a mood other than "Happy" is chosen, the program will show a button that, when pressed, will show a motivational message from a stranger other than the user. In order for the sender and receiver to feel more connected and real to one another, the name and username of the sender are also displayed together with message.

### Cheer others up if you're feeling better
A feature has been implemented to keep track of how many Cheer Up requests the users have made, and if the number reaches five, the program will ask if the user would care to cheer others up together with the message the user requests for. This feature is intended to keep the web app alive and active by allowing fresh messages to be received often.


### Report System
Users will have the option to report output messages that appear to be out of context, suspected of spamming, or contain profanity whenever they request one. The "reports" column of the database's "messages" table keeps track of how many reports each specific message has received. Once there are five reports on a particular message, it will temporarily be moved from the "messages" table to the "review" table where the moderators can review and take necessary actions and if required, delete them.

## Additional Informations
Although this web application was created with a very limited number of fundamental technologies and is relatively small in size, I am proud to say that the program is designed properly to go through extensive error handling both on the client and server sides to prevent problems caused by user error and software bugs. For instance, on the sign-up page, the "required" attributes are added to the input element in the HTML file, together with the error-checking conditional statements in Flask's route, to make sure the user doesn't leave any required input fields blank.

There are still many areas where I feel the need for improvement, so when I have the opportunity in the future, I will definitely come back to this and make some enhancements to both the program's design and functionalities with better technologies and implementations.

## Special Thanks
I would like to thank the CS50 staff for making the course and this project possible, as well as all the helpful staffs, lab partners, and members of the CS50 discord community who assisted me with the problems I got stuck on throughout the course. Again, I would like to thank each and every one of you who made this project possible, and This is "Cheer Up!"




