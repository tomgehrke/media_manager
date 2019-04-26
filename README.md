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

Finally, type **python application.py** to start the Flask web server. Point your web browser to **http://localhost:5000** and you should see the main dashboard.

## Usage

### Main Dashboard

Usage is fairly straightforward. The main/start page displays a dashboard breaking the catalog down by both media type and media format. A count of items currently being stored in that category is also shown.

### Listings

Clicking a category will pull up a page that lists all of the associated media. The information displayed may vary depending on what data was entered for the item (e.g. you will see a link to its IMDb entry if and IMDb ID was provided).

### Logging In

Media Manager takes advantage of Google OAuth as its authentication provider. Clicking the Login link at the upper right will provide you with a secure path to authentication.

> **NOTE**
>
>Logging in is a requirement for adding, editing and deleting items to the catalog.

### Adding Media

When adding media, the only information that is _absolutely_ required is the Title.

> **NOTE**
>
>The IMDb ID for media can be found on the IMDb website ([https://www.imdb.com](https://www.imdb.com)). The easiest way to determine it is to look at the URL for a particular item.
>
>Example:
>
>The link to the 2009 release of Star Trek is `https://www.imdb.com/title/tt0796366/`. The ID is the number that comes after the title. So in this case, the IMDb ID would be `tt0796366`.

### Editing/Deleting Media

If you "own" the item on the media listing page (meaning that you are the one who created the item in the first place), you will find Edit and Delete buttons attached the the media "card".

## Web API

Media Manager can provide JSON formatted listings of media in the catalog. There are three endpoints.

| Endpoint                                                   | Result                                       |
| ---------------------------------------------------------- | -------------------------------------------- |
| `http://localhost:8000/media/json`                         | Full catalog listing.                        |
| `http://localhost:8000/mediatype/<media type id>/json/`    | Listing filtered by a specific media type.   |
| `http://localhost:8000/mediaformat/<media format id/json/` | Listing filtered by a specific media format. |

>**NOTE**
>
>For your convenience, you will find a link to a link to the associated JSON enpoint for type/format-filtered listings immediately following the category title.
