# news parsing

                                    +------------------+             +-------------------------+ Response
                                    |      DB(Mongo)   |             |                         +-------------->
                                    |                  +------------->   webserver(Tornado)    |
                                    +--------+---------+             |                         <--------------+
                                             ^                       +-------------------------+ User Req
                                             |
                                             |
                +------------+               |            +-------------+
                |            |               |            |             |
                |            |               |            |             |
                |            |               |            |             |
                |            |               |            |             |
                |  Spider    |               |            |  Crawler    |
                |            |               +------------+             |
                |            |                            |             |
                |            |                            |             |
                |            |                            |             |
                |            |                            |             |
                +-----+------+                            +------+------+
                      |                                          ^
                      |                                          |
                      |                                          |
                      |                                          |
                      |                                          |
                      |                                          |
                      |        +---------------------+           |
                      |        |                     |           |
                      +--------> Queue(Redis)        +-----------+
                               |                     |
                               +---------------------+


Spider (Producer)
-----------------
* Continuous crawling through the Home page of https://www.theguardian.com/au and find URLs. After finding URL, it will add URLS to the Queue

Crawler(Consumer)
-----------------
* It will read the URLs from the queue and process it. Save the result in the DB(MongoDB)

Webserver(Tornado)
------------------
* Accept the User search and respond with results(URL, date, Text from  https://www.theguardian.com/au) from  the DB

How to Setup locally
--------------------
- Installation
    ```
    - cd news_parsing
    - sudo ./install
    ```

    NOTE: - make sure that NLKT is installed and downloaded the data
          - Test Redis setup and verify its connectivity in the default PORT
- Run
    We have to run 3 components otgether
    1. Spider
    2. Crawler
    3. webserver
    ```
    - # python3 server.py
    - # python3 server.py
    - # python3 np_crawler.py
    ```
