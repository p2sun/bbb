# bbb
This is our submission for the Bloomberg Code B Hackathon at Waterloo. 

The goal was to make a game bot that would play in a game of king of the hill against the other
competitors. Your program has access to APIs that will only tell you about the elements on the map in
your bot's vicinity. Your goal is to maximize the number of hills that you capture throughout the game.
A point is given every second that you own a hill.

Usually you would figure out some sort of heuristic to explore the map and find the location of the hills
on the map.

But we decided to make our lives easier. Local search might take us a while to find hills and wouldn't guarantee that we'd find any. Developing heuristics is sort of a skill on its own. If you've built such heuristics for game bots before, you would have much more context on what would work and what wouldn't. We wanted to find the most efficient way to find the greatest return on investment. So we asked, what if we could figure out all the pieces on the map within the first minute of the game?

So, we decided to look at the game board. The game board was visualized on a web app. The web app was updated
with real time data from Bloomberg's websocket. As hackers at a hackathon, we initially deconstructed the web app
to find out how the web app's game board was being populated and updated. We were able to get all the real time data from the game
from this websocket. We could've just went with this, but realized that if we won, we might get disqualified for this type of hack. So we talked to the organizers about it. Unfortunately, the organizers felt this was unfair and didn't allow us to do this. Instead, they
proposed that we could use image processing to figure out what was on the board in real time. That's exactly what we did.

We used Selenium to load the web app, this would allow us to load the UI elements of the web app that were generated via javascript. Once the whole map was loaded, all we needed to do is take a screen shot of the map and run it through our image processing algorithms.
With the image of the map, we used blob detection methods provided by Scikit image to extract all the location of the hills and other components of the game. We initially used canny edge detection with hough transforms to find circles, since all the map's elements were circles. However, this was a much simpler problem. The map was a blank canvas that had circles drop on top of, blob detection was a much simplier, faster and accurate method to extract components of the map from the image. We scaled the location of these components. The data we got from our image processing techniques were relative to the size of the image. We had to scale our data points back to the map's actual size.

Then we just ran a graph search algorithm to have our bot traverse the map between the hills on the map.
