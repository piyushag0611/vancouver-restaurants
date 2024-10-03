# Vancouver-Restaurants
Let's explore the restaurants in Vancouver together.
Vancouver is pretty much an immigrant city just like the rest of Canada. It has different types of cuisines, you name it and you'll have it. Japanese, Mexican, Indian, Chinese and even more not so well known ones like Ethiopian cuisine restaurants are here. Now, since you are so spoiled with choice, How do you make it? How do you decide. 

Even starting off this project looks a bit tricky, because the base of this project is DATA. How do I get the list of restaurants in metro vancouver? One convenient way to do this is using API, and there seems to be three useful APIs that could be used to get such a list:

1. Google Maps API
2. Yelp API
3. FourSquare API

Since this is a **hobby** project, and not really an **enterprise** object, where I would be making money out of it, I am not willing to spend dollars for making API calls. All the above APIs charge per 1000 calls. Luckily, Google Maps and FourSqaure offer an initial credit, whereas Yelp gives a month free, so I can use these free offerings to build my initial database. And since this is only a hobby project, I don't have to maintain the dataset regularly. I can schedule it to refresh once a year!!

So, now that I have three options to make my database from (Google places, Yelp, FourSquare). ChatGPT's recommendation based on my use-case was Yelp, as it had rich information, detailed restaurant information and since I was limiting myself to Metro Vancouver, so Yelp is good to go. Also, I could use it without any hassles at least for the first month. 

Another challenge in using these APIs is that they limit the search results to a maximum of 50. Both yelp and foursquare have a limit of 50, whereas google maps has a limit of 20. 

I have decided to use both Yelp and FourSquare API to create a Metro Vancouver database. I'll keep documenting on how it goes.

There have been lots of challenges in getting the list of restaurants. The first and the biggest challenge has been that all the three APIs only index a few results, even when they know lots of restaurants satisfy the conditions. 
1. Yelp indexes 240 restaurants, though will return only 50 at maximum.
2. FourSquare and Google API are worse because they index only 50 and 20 at a time.

To bypass this, I have decided to break down Metro Vancouver into a smaller grid. If the number of restaurants is less than 240, great I can use the grid and if not then I can break down the box further. If even in a small grid the number of restaurants are still too large, I can break it down by price (at least in Yelp).

