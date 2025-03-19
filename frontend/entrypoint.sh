#!/bin/sh

if [ "$ENV" = "development" ]; then
    exec npm run dev
else
    exec npm run build && npm run serve
fi