# bbb
This is our submission for the Bloomberg Code B Hackathon at Waterloo. 

The goal was to make a game bot that would play in a game of king of the hill against the other
competitors. Your program has access to APIs that will only tell you about the elements on the map in
your bot's vicinity. Your goal is to maximize the number of hills that you capture throughout the game.
You get points for every hill that is captured for every second.

Usually how we'd approach this type of problem is to use heuristics to explore the map to find where
key elements are. I.e. where hills are located,etc.

But we decided to make our lives easier. Local search would take us a while to find hills. Heuristics would also
take us time to develop. Instead, what if we could figure out all the pieces on the map?

So with this in mind, we decided to look at the game board. The game board was visualized on a web app. The web app was updated
with real time data from a websocket that was provided by Bloomberg. We initially deconstructed the web app
to find out the structure of the data from the websocket. We were able to get all the real time data from the game
from this websocket. Unfortunately, the organizers felt this was unfair and didn't allow us to do this. Instead, they
proposed that we could use image processing to figure out what was on the board in real time. That's exactly what we did.

We used selenium to load the web app and allow the web app to load the game's real time data. We then took a screen shot of the map.
Then we used blob detection methods provided by Scikit image to extract all the location of the hills and other components of the game.
We scaled the location of these components. The data we got from our image processing techniques were relative to the size of the image. 
We had to scale our data points back to the map's actual size.

Then we just ran a graph search algorithm to have our bot traverse the map between the hills on the map.
