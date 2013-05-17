#!/bin/bash

# With help from http://www.linuxquestions.org/questions/linux-software-2/get-first-day-of-last-month-and-last-day-of-last-month-in-bash-524775/

today_day=$(date +%d)
days_to_subtract=$((${today_day}-1))
cur_month_first_day=$(date --date "-${days_to_subtract} days" '+%Y-%m-%d')
cur_month_last_day=$(date --date "+1 month -${today_day} days" '+%Y-%m-%d')

echo ${cur_month_first_day} ${cur_month_last_day}