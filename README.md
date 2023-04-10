# Anomalies Anonymous

In light of the recent news of [alien life](https://www.independent.co.uk/space/alien-life-planet-radio-signal-b2315126.html) and the declassification of U.S. intelligence [documentation of UFO's](https://abcnews.go.com/Politics/new-ufo-report-number-incidents-reported-increasing/story?id=96389000), we decided to create a website for those who want to believe.

Our project builds upon a database of nearly 65,000 sightings from around the United States dating from 1910-2014. Users are able to browse those records and read the details of each one. By making an account, users can add their own sightings to the database and leave comments on sighting reports. A heat map offers a handy geo-spatial representation of sightings.

# Screenshot

![Landing Page](https://user-images.githubusercontent.com/98293872/230804913-a1758efd-40f2-45b4-9623-1666b9ebd7d8.png)


# Technologies Used

## Languages

- Python
- HTML
- JavaScript
- CSS

## Frameworks

- Django

## Libraries

- Bootstrap
- jQuery
- geocoder
- florium
- Crispy Forms

# APIs

- Google API

# Challenges

## Styling

While Bootstrap5 and Crispy Forms provided a tremendous amount of styling infrastructure for us, overriding the built-ins was often a challenge for us. Because both Django and Bootstrap are highly opinionated, there were some aspects of styling that required creative problem solving to achieve desired results.

## Dataload

After finding and cleaning up a Google Sheet of more than 60,000 reports of alien or UFO sightings, we turned the sheet into a Google API endpoint to handle to massive dataload and (relatively) quickly seed our database with those records.

However, the size of our database posed rendering issues for our sightings index and our heat index map. We resolved the browser-crashing load on our sightings index page by implementing an aynchronous JS function that created an infinite scroll interface.

On our heat index map, we utilized the folium plugin, FastMarkerCluster to more quickly render markers indicicating the exact location of each sighting. Each Marker has its own popup with the Report # of that sighting. Unfortunately, FastMarkerCluster is not a a very active project and we were unable to implement markers that link to a given sighting's detail page.

## Sighting Form Fields

The original list of sightings we were able to find included columns for both latitude and longitude, which inspired our vision of a heat map. However, we realized that a typical user would not be familiar with their exact coordinates. Geocoder came to the rescue. We redifined the Sighting Model's save method and used Geocoder's `osm()`, `lat`, and `lng` methods to generate a coordinate set from the user's inputed city and state.

# Getting Started

[Click to View Project Planning](https://trello.com/b/tnR021Si/project-3)<br>
[Link To Deployed App](http://www.anomaliesanonymous.com/)

# Next Steps

- Upvoting/downvoting capabilites for a ranking system of popular sightings 
- Use some sort of news API to have a page for articles linking to sightings in the news
- Add photo upload to Report A Sighting form
- Build out the user model to include more information (first/last name, photo, occupation, watched sightings, etc)
- Be able to delete individuals photos on your sighting without needing to delete the report and file a new one with correct picture
- Carousel for sightings with multiple photos
- Built out comment model to be able to reply to certain comments, upload photos to comments, tag other users, etc.
