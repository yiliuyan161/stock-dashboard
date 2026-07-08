#!/bin/bash
# Verify stock-dashboard is running
docker ps --filter name=stock-dashboard --format '{{.Status}}' | grep -q Up && echo 'container running'
