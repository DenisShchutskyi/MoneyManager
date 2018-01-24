
import matplotlib as mpl
import matplotlib.pyplot as plt
# import matplotlib.dates as mdates
# import datetime as dt
# import csv
import binascii
import os


def bars_diagramm():
    data_names = ['cafe', 'pharmacy', 'fuel', 'bank', 'waste_disposal',
                  'atm', 'bench', 'parking', 'restaurant',
                  'place_of_worship']
    data_values = [9124, 8652, 7592, 7515, 7041, 6487, 6374, 6277,
                   5092, 3629]

    dpi = 80
    fig = plt.figure(dpi = dpi, figsize = (512 / dpi, 384 / dpi) )
    mpl.rcParams.update({'font.size': 10})

    plt.title('OpenStreetMap Point Types')

    ax = plt.axes()
    ax.yaxis.grid(True, zorder = 1)

    xs = range(len(data_names))

    plt.bar([x + 0.05 for x in xs], [ d * 0.9 for d in data_values],
            width = 0.2, color = 'red', alpha = 0.7, label = '2016',
            zorder = 2)
    plt.bar([x + 0.3 for x in xs], data_values,
            width = 0.2, color = 'blue', alpha = 0.7, label = '2017',
            zorder = 2)
    plt.xticks(xs, data_names)

    fig.autofmt_xdate(rotation = 25)

    plt.legend(loc='upper right')
    fig.savefig('bars.png')


def pie_diagram(categories):
    name = 'temps/' + (str(binascii.hexlify(os.urandom(20)))[2:42]) + '.png'
    data_names = []
    data_values = []
    for k in list(categories.keys()):
        data_names.append(k+' ({})'.format(categories[k]))
        data_values.append(categories[k])
    # print(data_values)
    # print(data_names)
    dpi = 80
    fig = plt.figure(dpi = dpi, figsize = (640 / dpi, 640 / dpi) )
    mpl.rcParams.update({'font.size': 9})

    plt.title('Ваши затраты в текущем месяце(%)')

    xs = range(len(data_names))

    plt.pie(
        data_values, autopct='%.1f', radius = 1.1,
        explode = [0 for _ in range(len(data_names))] )
    plt.legend(
        bbox_to_anchor = (-0.16, 0.45, 0.25, 0.25),
        loc = 'lower left', labels = data_names )
    fig.savefig(name)
    return name

