import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats as st

try:
    tab_visits = pd.read_csv('datasets/visits_log_us.csv', nrows=300)
    tab_orders = pd.read_csv('datasets/orders_log_us.csv', nrows=300)
    tab_costs = pd.read_csv('datasets/costs_us.csv', nrows=300)
except:
    tab_visits = pd.read_csv('../datasets/visits_log_us.csv', nrows=300)
    tab_orders = pd.read_csv('../datasets/orders_log_us.csv', nrows=300)
    tab_costs = pd.read_csv('../datasets/costs_us.csv', nrows=300)

db = {'visits': tab_visits, 'orders': tab_orders, 'costs': tab_costs}

def show_db_details(tables: dict) -> None:
    '''
    Display the table's details of a data set.
    '''
    for name, table in tables.items():
        print('-'*100)
        print(f'> Table: {name}\n> Name columns: {table.columns}')
        table.info(memory_usage='deep')
        print('> Rows duplicated: ', table.duplicated().sum())
        try:
            display(table.sample(3))
        except:
            print(table.sample(3))

show_db_details(db)

try:
    tab_visits = pd.read_csv('datasets/visits_log_us.csv', dtype={'Device': 'category'}, parse_dates=['Start Ts', 'End Ts'])
    tab_orders = pd.read_csv('datasets/orders_log_us.csv', parse_dates=['Buy Ts'])
    tab_costs = pd.read_csv('datasets/costs_us.csv', parse_dates=['dt'])
except:
    tab_visits = pd.read_csv('../datasets/visits_log_us.csv', dtype={'Device': 'category'}, parse_dates=['Start Ts', 'End Ts'])
    tab_orders = pd.read_csv('../datasets/orders_log_us.csv', parse_dates=['Buy Ts'])
    tab_costs = pd.read_csv('../datasets/costs_us.csv', parse_dates=['dt'])

db = {'visits': tab_visits, 'orders': tab_orders, 'costs': tab_costs}

def default_col_format(columns: list, sep: str = ' ') -> list:
    '''
    Changes strings to lower case and replace " " or other characters to "_".
    '''
    return list(map(lambda string: string.lower().replace(sep, '_'), columns))

for table in db.values():
    table.columns = default_col_format(list(table.columns))

del table

show_db_details(db)

tab_visits_2017 = db['visits'][db['visits']['start_ts'].dt.year == 2017].reset_index(drop=True)
tab_visits_2018 = db['visits'][db['visits']['start_ts'].dt.year == 2018].reset_index(drop=True)

del tab_visits

tab_orders_2017 = db['orders'][db['orders']['buy_ts'].dt.year == 2017].reset_index(drop=True)
tab_orders_2018 = db['orders'][db['orders']['buy_ts'].dt.year == 2018].reset_index(drop=True)

del tab_orders

tab_costs_2017 = db['costs'][db['costs']['dt'].dt.year == 2017].reset_index(drop=True)
tab_costs_2018 = db['costs'][db['costs']['dt'].dt.year == 2018].reset_index(drop=True)

del tab_costs, db

db_17 = {'visits': tab_visits_2017, 'orders': tab_orders_2017, 'costs': tab_costs_2017}
db_18 = {'visits': tab_visits_2018, 'orders': tab_orders_2018, 'costs': tab_costs_2018}


print(f'''> {2017:-^100}:
> Visits size: {len(db_17['visits']):,}
> Orders size: {len(db_17['orders']):,}
> Costs size: {len(db_17['orders']):,}
''')

print(f'''> {2018:-^100}:
> Visits size: {len(db_18['visits']):,}
> Orders size: {len(db_18['orders']):,}
> Costs size: {len(db_18['orders']):,}
''')

db_17['visits']['day'] = db_17['visits']['start_ts'].dt.date
db_17['visits']['week'] = db_17['visits']['start_ts'].dt.isocalendar().week
db_17['visits']['month'] = db_17['visits']['start_ts'].dt.month

db_18['visits']['day'] = db_18['visits']['start_ts'].dt.date
db_18['visits']['week'] = db_18['visits']['start_ts'].dt.isocalendar().week
db_18['visits']['month'] = db_18['visits']['start_ts'].dt.month

def two_stats(data: list, atrib: list, titles: list, method: str = 'count') -> None:
    '''
    Print the minimum, average and maximum of two tables.
    '''
    for i, table in enumerate(data):
        if method == 'nunique':
            group = table.groupby(atrib[0])[atrib[1]].nunique().reset_index()
            print(f'''> {f'{titles[2]} per {atrib[0]} in {titles[i]}':-^100}:
> Total active {atrib[0]}s: {len(group)}
> Minimun: {group[atrib[1]].min():,}
> Average: {group[atrib[1]].mean():,.2f}
> Maximum: {group[atrib[1]].max():,}
''')
        elif method == 'count':
            group = table.groupby(atrib[0])[atrib[1]].count().reset_index()
            print(f'''> {f'{titles[2]} per {atrib[0]} in {titles[i]}':-^100}:
> Total active {atrib[0]}s: {len(group)}
> Minimun: {group[atrib[1]].min():,}
> Average: {group[atrib[1]].mean():,.2f}
> Maximum: {group[atrib[1]].max():,}
''')
        elif method == 'sum':
            group = table.groupby(atrib[0])[atrib[1]].sum().reset_index()
            print(f'''> {f'{titles[2]} per {atrib[0]} in {titles[i]}':-^100}:
> Total active {atrib[0]}s: {len(group)}
> Minimun: {group[atrib[1]].min()}
> Average: {group[atrib[1]].mean()}
> Maximum: {group[atrib[1]].max()}
''')
        else:
            raise TypeError
        
two_stats([db_17['visits'], db_18['visits']], ['day', 'uid'], ['2017', '2018', 'Clients'], 'nunique')

def two_plots(data: list, atrib: list, y_label: str = 'Items', method: str = 'count') -> None:
    '''
    Plot two tables acording to its atributes. Requires pyplot of Matplotlib imported as plt.
    '''
    for table in data:
        if method == 'nunique':
            group = table.groupby(atrib[0])[atrib[1]].nunique().reset_index()
        elif method == 'count':
            group = table.groupby(atrib[0])[atrib[1]].count().reset_index()
        elif method == 'sum':
            group = table.groupby(atrib[0])[atrib[1]].sum().reset_index()
        else:
            raise TypeError
        plt.plot(group[atrib[0]], group[atrib[1]])

    plt.title(f'{y_label} per {atrib[0]}')
    plt.ylabel(y_label)
    plt.show()

two_plots([db_17['visits'], db_18['visits']], ['day', 'uid'], 'Users', 'nunique')


two_stats([db_17['visits'], db_18['visits']], ['week', 'uid'], ['2017', '2018', 'Clients'], 'nunique')

two_plots([db_17['visits'], db_18['visits']], ['week', 'uid'], 'Users', 'nunique')


two_stats([db_17['visits'], db_18['visits']], ['month', 'uid'], ['2017', '2018', 'Clients'], 'nunique')

two_plots([db_17['visits'], db_18['visits']], ['month', 'uid'], 'Users', 'nunique')

two_stats([db_17['visits'], db_18['visits']], ['day', 'start_ts'], ['2017', '2018', 'Sessions'])
two_stats([db_17['visits'], db_18['visits']], ['day', 'uid'], ['2017', '2018', 'Clients'], 'nunique')

db_17['visits']['session_time'] = (db_17['visits']['end_ts'] - db_17['visits']['start_ts'])
db_18['visits']['session_time'] = (db_18['visits']['end_ts'] - db_18['visits']['start_ts']).reset_index(drop=True)

two_stats([db_17['visits'][db_17['visits']['session_time'] > '0 days 00:00:00'], db_18['visits'][db_18['visits']['session_time'] > '0 days 00:00:00']], ['start_ts', 'session_time'], ['2017', '2018', 'Session time'], 'sum')

two_plots([db_17['visits'][db_17['visits']['session_time'] > '0 days 00:00:00'], db_18['visits'][db_18['visits']['session_time'] > '0 days 00:00:00']], ['start_ts', 'session_time'], 'Session time', 'sum')

two_stats([db_17['visits'], db_18['visits']], ['uid', 'start_ts'], ['2017', '2018', 'Visits'])

two_plots([db_17['visits'], db_18['visits']], ['uid', 'start_ts'], 'Time')

first_session_17 = db_17['visits'].groupby('uid')['start_ts'].min().reset_index()
first_session_17.columns = ['uid', 'first_session']
first_session_17['first_session'] = first_session_17['first_session'].dt.date

first_session_18 = db_18['visits'].groupby('uid')['start_ts'].min().reset_index()
first_session_18.columns = ['uid', 'first_session']
first_session_18['first_session'] = first_session_18['first_session'].dt.date

first_session = pd.concat([first_session_17, first_session_18])

del first_session_17, first_session_18, db_17, tab_costs_2017, tab_orders_2017, tab_visits_2017

first_session = first_session.groupby('uid')['first_session'].min().reset_index()

db_18['orders'] = db_18['orders'].merge(first_session, on='uid', how='left')

del first_session

db_18['orders']['client_conv'] = list(map(lambda series: series.days, (db_18['orders']['buy_ts'].dt.date - db_18['orders']['first_session'])))

client_conv = db_18['orders'].groupby('uid')['client_conv'].min().reset_index()
sales_revenue = db_18['orders'].groupby('uid')['revenue'].sum().reset_index()
first_session = db_18['orders'].groupby('uid')['first_session'].min().reset_index()
first_buy = db_18['orders'].groupby('uid')['buy_ts'].min().reset_index()
first_buy.columns = ['uid', 'first_buy']
sales_number = db_18['orders'].groupby('uid')['buy_ts'].count().reset_index()
sales_number.columns = ['uid', 'sales_number']


clients = pd.merge(client_conv, sales_revenue, on='uid')
del client_conv, sales_revenue
clients = clients.merge(sales_number, on='uid')
del sales_number
clients = clients.merge(first_session, on='uid')
del first_session
clients = clients.merge(first_buy, on='uid')
del first_buy

print(clients['client_conv'].value_counts().reset_index().head(100))