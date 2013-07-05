## This file is where you write your event handlers in Python.
## Define functions named like element_id__event(dom) e.g.
#   btn_mybutton__click(dom):
#       dom['txt_textbox']['value'] = "Button clicked."
#   return dom
#
## You can delete this comment once you've read it.
import os, os.path
import time

import pandas as pd
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
# Globals are kinda okay...

AAPL = pd.DataFrame.from_csv("aapl.csv")
GOOG = pd.DataFrame.from_csv("goog.csv")

def btn_update__click(dom):
    symbol = dom['select_stock']['value']
    if symbol == 'AAPL':
        df = AAPL
    elif symbol == 'GOOG':
        df = GOOG
    else:
        return dom
    df.sort(inplace=True)
    bounds = [dom[x]['value'] if dom[x]['value'] else None 
              for x in ['date_start', 'date_end']] 
    ts = df['Close'][bounds[0]:bounds[1]]
    if not ts.any():
        # Error message?
        return dom
    try:
        ts.plot()
        for win in [int(dom[x]['value']) 
                    for x in ['slider_window_1', 'slider_window_2']]:
            pd.rolling_mean(ts, win).plot()
        plt.title("Weekly closing prices for {}".format(symbol))
        
        fname_parts = ('static','img','tmp',
            '{}-{}.png'.format(symbol, int(time.time())))
        fname = os.path.join(*fname_parts)
        if not os.path.exists(os.path.join(*fname_parts[:-1])):
            os.makedirs(os.path.join(*fname_parts[:-1]))
        plt.savefig(fname)
        
        dom['img_plot']['src'] = '/'.join(fname_parts)
    finally:
        plt.close()

    return dom
