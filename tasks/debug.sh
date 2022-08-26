#!/bin/sh
# ---
# help-text: Run the app in debug mode
# ---
vg --var "PUBLISH=$VG_PORT:5000" run flask --debug run --host 0.0.0.0
