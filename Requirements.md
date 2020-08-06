# software requirements 
## VISION
* To have a web application that allows the user to plan trips based of  price and not dates. By showing the cheapest price in a much larger date range. The application also notifies the user by email on price changes for other possible trips.
* Most web applications for flight travel make the user select exact dates for our trips. Well this web application allows the user to plan their vacation around them getting the cheapest flight possible so ultimately they save more money on their trip. 
* People should care about this because they will not only be able to target the cheapest flights possible but also be notified when the price drops. 

## Scope in/out
### IN
* It will search for a cheap plane ticket
* It will provide cheapest ticket
* Notify user when price drops
* Allow user to login in and out of app
* Store user info to keep track of their flight data
* Have a user friendly front end 

### Out 

* This app will never be mobile because we are building this app using django
* It won't check multiple airlines 
* Won’t check duration of flight 

## MVP:
* Have a deployed web-app that allows a user to specify date range and stay duration, targets a website of a specific airline to request the data, stores it and refreshes it to keep the data current. Create user accounts so that the app can be used by multiple users.
### stretch
1)  stretch goal - add multiple airlines
2)  stretch goal - provide the tickets from nearby airports if they are cheaper

## Functional requirements 
1) As a user i want to find the cheapest flight so i can choose the dates when to travel.
2) As a user i want the flight prices to update so that i can be updated when the  prices drop.
3) As a user i want to target a specific airline that isn't present in most common searches. 
4) As a developer i want to be able to manage and control the users of my application. 
5) As a developer i want to build the user-facing web application built in Django so that we can apply all the benefits that Django gives us for example extra security.

## Data Flow
1) User will goes to start page and they are asked to login/register
2) Logged in user is asked for destination, duration of stay , and date range of all that is possible to travel. 
3) To accomplish this we use selenium to pull data from the specific airline site.
4) Once data is retrieved user is directed to the results page and it shows a sorted list of cheapest flights available.
## Non-functional requirements
* Django will solve our need for security because of its high level features on security.
* Django will ease the usability by making a user friendly page so the user can navigate the page with ease. 
