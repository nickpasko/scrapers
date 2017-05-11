#!/usr/bin/env bash
sudo su root -c "cd /scraper && python3 sender.py > sender.log && rm crawl_result/*"
