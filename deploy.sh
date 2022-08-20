#!/bin/bash

datasette publish fly oakland_minutes.db --metadata metadata.json --plugins-dir=plugins --app="oakland-datasette"