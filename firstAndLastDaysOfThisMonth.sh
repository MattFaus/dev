#!/bin/bash

# With help from http://www.linuxquestions.org/questions/linux-software-2/get-first-day-of-last-month-and-last-day-of-last-month-in-bash-524775/
today_day=$(date +%d)
days_to_subtract=$((${today_day}-1))

if [ "${days_to_subtract}" = "0" ]; then
    # If today is the first day of a new month, we want last month
    month_first_day=$(date --date "-1 month" '+%Y-%m-%d')
    month_last_day=$(date --date "-1 day" '+%Y-%m-%d')
else
    # Else, we can just do the math on today since it works the same as yesterday
    month_first_day=$(date --date "-${days_to_subtract} days" '+%Y-%m-%d')
    month_last_day=$(date --date "+1 month -${today_day} days" '+%Y-%m-%d')
fi

echo ${month_first_day} ${month_last_day}