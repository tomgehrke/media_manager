# Media Manager

"Media Manager" is a project developed for Udacity's Full Stack Web Developer course. This Python/Flask/SQLite application is intended to demonstrate the ability to create a CRUD application from scratch relying on an OAuth2.0 provider for authentication.

The application concept is to manage a collection of media (video content). One may categorize items by type (movie, TV, etc.) and format (DVD, Blu-Ray, etc.).

Users may only manage those items that they themselves created. This means that the ability to add items will not be available until the user has logged in.

## Requirements

The application requires Python 3 and the following modules:

* Flask
* SQLAlchemy
* oauth2client
* requests
* httplib2

## Setup

From the application's root folder type **python database_setup.py** to initialize the database. If the command completed successfully, you should find that a "mediamanager.db" file has been created.

The next step is optional. Type **python loadSampleData.py** to pre-load the database with sample data. If you want to skip this and start with a blank slate, that is completely up to you.

Finally, type **python application.py** to start the Flask web server. Point your web browser to **http://localhost:5000** and you should see the main dashboard which.

