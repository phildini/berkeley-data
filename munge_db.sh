#!/bin/bash

cp oakland_minutes.db oakland_minutes.db.bak

sqlite-utils convert oakland_minutes.db pages path \
'date = value.split("/")[1].replace(".pdf", "")
return {
    "date": date
}' --multi
sqlite-utils transform oakland_minutes.db pages --rename folder body
sqlite-utils transform oakland_minutes.db pages -o body -o date -o text -o page
# Because we're going to be reordering columns, we'll need to rebuild FTS
sqlite-utils drop-table oakland_minutes.db pages_fts
sqlite-utils enable-fts oakland_minutes.db pages text
