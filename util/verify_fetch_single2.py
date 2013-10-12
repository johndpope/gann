#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Verify tool for fetch_taiex.py -- fetch_single2.

Usage:
    verify_fetch_single2.py verify html [--start=<start>] [--end=<end>]
    verify_fetch_single2.py count days [--start=<start>] [--end=<end>]
    verify_fetch_single2.py -h | --help
    verify_fetch_single2.py -v | --version

Options:
    -h, --help         Show this screen.
    -v, --version      Show version.
    --start=<start>    Fetch start date [default: 2004-10-15]
    --end=<end>        Fetch end date [default: 2011-01-15]
"""

###
### project libraries
###
from fetch_taiex import *


###
### contants
###
ERROR_INVALID_ARGUMENT = 1


###
### helper functions
###
def setup_date_boundaries(start, end):
    LOWER = date(2004, 10, 15)
    UPPER = date(2011, 1, 15)
    if start > UPPER or end < LOWER:
        return None, None
    start = max(start, LOWER)
    end = min(end, UPPER)
    return start, end


def _fetch_one(day):
    url = 'http://www.twse.com.tw/ch/trading/exchange/MI_5MINS_INDEX/genpage/Report{year}{month:02d}/A121{year}{month:02d}{day:02d}.php?chk_date={taiex_date}'.format(year=day.year, month=day.month, day=day.day, taiex_date=convert_date(day))
    resp = requests.get(url)
    return PyQuery(decode_page(resp.text))


###
### test functions
###
def verify_html(start, end):
    """Verify the HTML structures day by day are keep the same."""
    print "Verifying.. "
    flag = start.replace(year=start.year-1, month=1, day=1)
    for day in days_range(start, end):
        if flag.year != day.year:
            print day.year
            flag = day
        data = _fetch_one(day)
        if u'查無資料' in data('body').text():
            continue
        if not data('table.board_trad') and \
           not data('div#tbl-container'):
            print "verify success until %s" % day
            break


def count_days(start, end):
    total = (end - start).days + 1
    trade = holiday = 0
    for day in days_range(start, end):
        data = _fetch_one(day)
        if u'查無資料' in data('body').text():
            holiday += 1
        else:
            trade += 1
    assert total == (trade + holiday), \
        "days number are not match"
    print "Total: %d, trade: %d, holiday: %d" % (total, trade, holiday)


###
### main procedure
###
if __name__ == '__main__':
    args = docopt(__doc__, version="fetch_taiex_single2.py 1.0")
    # setup the date range
    start = normalize_date(args['--start'])
    end = normalize_date(args['--end'])
    start, end = setup_date_boundaries(start, end)
    assert start or end, "*** Error: Date range is not correct!"
    # start verifying
    if args['verify']:
        verify_html(start, end)
    elif args['count']:
        if args['days']:
            count_days(start, end)
