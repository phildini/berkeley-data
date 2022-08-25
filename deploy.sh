#!/bin/bash

datasette publish fly city_minutes.db --metadata metadata.json --plugins-dir=plugins --app="berkeley-datasette"