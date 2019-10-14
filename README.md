# gogoanimeapi
https://gogoanimeapi.herokuapp.com/

A simple flask application to scrape gogoanime website. Used for demo and learning purposes only.

How to use the API

The base api url is https://gogoanimeapi.herokuapp.com/

1. To search for an anime, call the endpoint '/search/{anime_name}'
    for example, https://gogoanimeapi.herokuapp.com/search/One Piece
    
    Note that you get a unique anime_id for each anime, which you use to retrieve more details about the anime. 
    
   
2. To fetch a detail of an anime, call the endpoint '/anime/{anime_id}'
    for example, https://gogoanimeapi.herokuapp.com/api/anime/one-piece
    
3. To fetch watchable cdn links, call the endpoint '/watch/{anime_id}/{episode_number}'
    for example, https://gogoanimeapi.herokuapp.com/api/watch/one-piece/2
    
4. To fetch anime list belonging to a certain genre, use the endpoint '/genre/{genre_name}/{page_number}'
    for example, https://gogoanimeapi.herokuapp.com/api/genre/action/2
    (for now you must define the page_number even if you are asking for the first page :()


That's it.

It is a simple project I created to learn about python and web scraping. If you have any issues, please email me.
