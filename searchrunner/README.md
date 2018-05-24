# Building a Flight Search API

This API shows how I would containerize and organize the various services at play, and along those lines I did make some minor modifications to the scraper and test files. However these changes just updated import paths, and in the case of the test file, updated the url it is hitting to reflect that it's no longer hitting localhost, but another container directly. Everything to do with the logic for both the scraperapi and scraperapi_test has been unchanged.

To run services:
`make up`

To run test (after starting services):
`make test`

To clean up at the end:
`make clean`

You can still hit the aggregator and scraperapi services directly at localhost:8000 and localhost:9000 respectively.

Requirements: Docker, docker-compose, the ability to download python images from Docker Hub


