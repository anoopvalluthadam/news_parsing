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
* Accept the User search and respond with results(URL from  https://www.theguardian.com/au) from  the DB
