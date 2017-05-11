#!/usr/bin/env bash
sudo su root -c "cd /scraper && scrapy runspider car_quotz_spider.py > scraper.log"
