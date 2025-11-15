# WEC-2025
CR themed trading in 1450

The GUI that has multiple features:
1) A map of all the villages in our kingdom (Thinking about 5-11). Each city is connected to adjacent cities through trade routes. We have a total of 5 resources in our kingdom. The resources are iron, wood, livetsock and grain, and additionally, we have gold as a currency, which is produced by every city. Each city should produce gold as well as 1 other resource, and the rate of production depends on the current population of the city.

2) Every city has a pool of the 5 resources and a threshold for each resource depending on its populatio (behind the scenes, there is the idea that each city needs a minimum resource value to operate (like an initial value or the constant term of a function) + resource per person (the linear value depending on the number on the population value)). If the resource value drops below the threshold for any resource in that city, the growth rate of the that city goes into the negatives. If its higher for all, it will increase. How much higher or lower it is will determine the negative or positive growth rate. We need to create an algorithm that archives this. One feature of the algorithm is that if the resource drops below the minimum survival rate for the city, which is the constant term in the linear function, the city is effectively dead and removed from the map. Every city also consumes resources based on their population.

3) We need an algorithm to balance resources. Every city is connected by a trade route.  Keep in mind that every city only produces 2 out of 5 required resources for survival. As a result, we need to trade resources between every city. These resources go through the trade routes. We need another algorithm to manage how the resources are traded between the city.

4) I want the simulation to start in the year 1450 and run until 1470. In real time, it should take 10 minutes, so each year is 30 seconds. For the resource management (resource deficit calculations, total stock, etc), I want the algorithm to run calculations every month. So that means in real time, the simulation makes calculations every (30/12 = 2.5) seconds. 

5) I want to show trade happening in real time. Whenever the algorithm indicates that a city should be sending resources to another, an actual trade cart should set off from the sending city to the receiving city and take (30/12 = 2.5) seconds. As the cart reaches the city, the resources get added to their stockpile as the new refresh happens. The population growth/decline should be decided by the values of the previous refresh, not the current addition.

6) There should be an element of random natural disasters. Here is a list of all the ones that can happen and they should only affect 1 to a few cities at a time. Here are the following disasters and their corresponding affects:
1) Drought (No livestock or grain is produced)
2) Pirate raid (Pirates raid half of the current stockpile of resources)
3) Lightning storm (Blocks that trade route)
4) Plague (cuts trade routes to a city for 4 months and kills 10% of the population per month)
5) Labor strike (No wood or iron is produced)
The program must be able to dynamically account for these events and keep the cities from dying. Note that all these 5 events should have corresponding animations that happen and remain for the duration of their existence at the correct cities. 

7) There should be a way for the ruler (me in this case), to add, modify my kingdom during the simulation. This means that I can order a project to be built at any point during the simulation in any city. These projects all require extra resources which the algorithm will have to find a way to provide. There are 5 actions that I can do for any city and there are:
Build a city wall (Costs iron, wood, and gold): decreases affects of plague by 30%
Build a refugee camp on the outskirts of the city (Costs, wood, livestock, grain, and gold): increases production by 5%
Build a monument of the king (Costs gold and iron): does nothing
Create a granary complex (costs gold, wood, and grain): city can still produce grain at 50% capacity during a drought.
Build a hotel (costs gold and iron): increases gold production by 5%
These should all have permanent icons beside the city whenever they are built by the king. Again, this is user-controlled.

8) There should be a map of all the cities and you should be able to pan in and zoom out. At zoom out, we should only see city names, the resources produced (just the icons) and the location denoted by a dot. By zooming in, we should see basic things like how many resources are being produced at the moment, as well as population and growth rate. By clicking on the city, we should be taken to a new page that displays a map of the city and gives a detailed layout of the variables:
current reserves displayed as 5 bars (kind of like a bar graph), with threshold lines showing the minimum requirement for citizens (below which pop would decrease) as well as the minimum threshold for when the city would die.
A chart of the growth rate since 1450
A chart of the population total since 1450
The option to build any of the 5 things mentioned above
The log of all the previous random events
Other info/data we can display that I'm missing

9) There should also be a bar on the side of the map that indicates the sustainability score that looks at a mostly environmental and/or ethical metric. I have no idea how this algorithm with work but an algorithm needs to be created for this. This will just be a score out of 1000 that is displayed as a bar on the side of our GUI that is colour-coated to show how good/bad it is. Red being low scores and green being high scores.

10) At the end of the simulation, we need to present a clear output — either text-based or graphical — showing how resources flow, how decisions are made, and the resulting state of the kingdom over time. Maybe similar to how each city is displayed once we click on it but for the entire kingdom. It should visualize the flow of resources and other things, such as population, growth, etc. It should essentially be a way more detailed verision of the city view and should have multiple tabs we can click on to view even more details.

