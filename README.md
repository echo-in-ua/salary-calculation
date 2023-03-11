# Salary calculation

## Description

Python script that use Wordpress Plugin [Daily sales report](https://github.com/echo-in-ua/gp-daily-sales-report) for filling Google Spread Sheet with data about sales. Use google service accont from https://console.cloud.google.com.  On first start create new spread sheet with title in "Y-m" format (like 2022-02) and fill data from first day of cuurent month.

## Usage

Run like Docker container with schedul start once a day by cron.d. All environmant variables shold be placed in cron.job file.

## Debuging and testing

Can be run in docker by script [up_env.sh](up_env.sh). 


