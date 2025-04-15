#!/bin/bash

ollama serve &
python3 api/page.py &
wait