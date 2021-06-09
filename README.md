# bentley-ottmann-api
The project implements the Bentley Ottmann algorithm using the FastAPI framework. </br>
Project to pass the course analytical geometry. </br>

## Data structures
The following data structures were used in the algorithm:

1. Priority Queue based on heap.
2. AVL Tree

More information:
1. https://en.wikipedia.org/wiki/Priority_queue
2. https://en.wikipedia.org/wiki/AVL_tree
3. https://docs.python.org/3/library/heapq.html 

## Algorithm assumptions
1. **No two line segment endpoints or crossings have the same x-coordinate.**
2. **No line segment endpoint lies upon another line segment.**
3. **No three line segments intersect at a single point.**

More information: 
1. https://en.wikipedia.org/wiki/Bentley%E2%80%93Ottmann_algorithm
2. https://en.wikipedia.org/wiki/Line%E2%80%93line_intersection

## How to run?

1. Install docker
2. Install docker-compose
3. Create `.env` file in main folder `bentley-ottmann-api/.env`. (Complete the `.env` file according to the `.example_env` file)
4. `docker-compose up --build`

## Endpoints at a glance

1. Board
    - GET `/boards/` list all boards name
    - POST `/boards/` create board
    - GET  `/boards/{name}/` get details board (name and line coordinates)
    - DELETE `/boards/{name}/` delete board with details
    
2. Line
    - POST `/boards/{name}/line/` add line to board
    - POST `/boards/{name}/generate-random-lines/` generate random lines on board
    - DELETE `/boards/{name}/clear-lines/` clear all lines from board
    
3. Draw
    - POST `/boards/{name}/draw/` draw lines on board
    - POST `/boards/{name}/intersection-points/draw/` draw all intersections points on board
    
4. Intersection Points
    - GET  `/boards/{name}/intersection-points/` get all intersection points coordinate
    - POST  `/boards/{name}/intersection-points/` find all intersection points (Bentley-Ottmann algorithm)
    
## How to read docs?
1. Open in browser `docs/_build/html/index.html`