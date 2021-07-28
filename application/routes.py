from application import app
from flask.wrappers import Response
from flask import render_template, request, Response
import pandas as pd
import matplotlib.pyplot as plt
import mpld3
from flask import Markup
import numpy as np
import random
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.tri as mtri
import base64
from io import BytesIO
from matplotlib.figure import Figure

data = ([2000000,	0.01],[3000000,	0.02],[3200000,	0.03],[4500000,	0.04],[5000000,	0.05],[5500000,	0.06],[6500000,	0.07],[8000000,	0.08],[11000000,	0.09],[12000000,	0.1])

@app.route('/')
@app.route('/index')
def index():

    a = np.array(data)

    fig, ax = plt.subplots()  # Create a figure containing a single axes.

    ax.plot(a[:,1],a[:,0]/1000000, label='Pareto Frontier',marker='o')
    ax.plot([.08], [5], marker="o", markersize=12, markeredgecolor="green", markerfacecolor="red")
    ax.annotate("<< Your Senario", xy=(0.08,5.0), xytext=(.08+0.003, 5.0), size=14, color='red')
    ax.plot([.07], [6.5], marker="o", markersize=12, markeredgecolor="green", markerfacecolor="blue")
    ax.annotate("<< ADAS Optimal", xy=(0.07,6.5), xytext=(.07+0.003, 6.5), size=14, color='darkblue')

    ax.set_xlabel('Risk')  # Add an x-label to the axes.
    ax.set_ylabel('Revenue ($M)')  # Add a y-label to the axes.
    ax.set_title("Risk/Revenue Pareto View")  # Add a title to the axes.
    ax.legend()

    script = mpld3.fig_to_html(fig)

    return render_template("index.html", tabtitle='ASAS', graphScript=Markup(script))

@app.route('/boa')
def boa():
    s = pd.Series([1, 2, 3])
    fig, ax = plt.subplots()
    s.plot.bar()
    fig.savefig('my_plot.png')
    print(type(fig))
    script = mpld3.fig_to_html(fig)
    print(type(script))
    return render_template("boasite.html", tabtitle='BoA Site', myscript=Markup(script))

########################################
########################################
def simple_cull(inputPoints, dominates):
    paretoPoints = set()
    candidateRowNr = 0
    dominatedPoints = set()
    while True:
        candidateRow = inputPoints[candidateRowNr]
        inputPoints.remove(candidateRow)
        rowNr = 0
        nonDominated = True
        while len(inputPoints) != 0 and rowNr < len(inputPoints):
            row = inputPoints[rowNr]
            if dominates(candidateRow, row):
                # If it is worse on all features remove the row from the array
                inputPoints.remove(row)
                dominatedPoints.add(tuple(row))
            elif dominates(row, candidateRow):
                nonDominated = False
                dominatedPoints.add(tuple(candidateRow))
                rowNr += 1
            else:
                rowNr += 1

        if nonDominated:
            # add the non-dominated point to the Pareto frontier
            paretoPoints.add(tuple(candidateRow))

        if len(inputPoints) == 0:
            break
    return paretoPoints, dominatedPoints

def dominates(row, candidateRow):
    return sum([row[x] >= candidateRow[x] for x in range(len(row))]) == len(row)  
########################################
########################################

@app.route('/test')
def test():

    a = np.array(data)

    fig, ax = plt.subplots()  # Create a figure containing a single axes.

    ax.plot(a[:,1],a[:,0]/1000000, label='Pareto Frontier',marker='o')
    ax.plot([.08], [5], marker="o", markersize=12, markeredgecolor="green", markerfacecolor="red")
    ax.annotate("<< Your Senario", xy=(0.08,5.0), xytext=(.08+0.003, 5.0), size=14, color='red')
    ax.plot([.07], [6.5], marker="o", markersize=12, markeredgecolor="green", markerfacecolor="blue")
    ax.annotate("<< ADAS Optimal", xy=(0.07,6.5), xytext=(.07+0.003, 6.5), size=14, color='darkblue')

    ax.set_xlabel('Risk')  # Add an x-label to the axes.
    ax.set_ylabel('Revenue ($M)')  # Add a y-label to the axes.
    ax.set_title("Risk/Revenue Pareto View")  # Add a title to the axes.
    ax.legend()

    script = mpld3.fig_to_html(fig)

    # stuff = Markup("<h4>Stuff goes here</h4>")
    return render_template("test.html", stuff=Markup(script))

@app.route("/test2")
def hello():
    # Generate the figure **without using pyplot**.
    fig = Figure()
    ax = fig.subplots()
    ax.plot([[1, 2,3,4,5],[3,1,5,2,6]])
    
    # Save it to a temporary buffer.
    buf = BytesIO()
    fig.savefig(buf, format="png")
    # Embed the result in the html output.
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    # print(data)
    # return f"<img src='data:image/png;base64,{data}'/>"
    retval = f"<img src='data:image/png;base64,{data}'/>"
    return render_template("test2.html", pic=Markup(retval))

@app.route("/proto")
def proto():

    ## add graph
    a = np.array(data)

    fig, ax = plt.subplots()  # Create a figure containing a single axes.

    ax.plot(a[:,1],a[:,0]/1000000, label='Pareto Frontier',marker='o')
    ax.plot([.08], [5], marker="o", markersize=12, markeredgecolor="green", markerfacecolor="red")
    ax.annotate("<< Your Scenario", xy=(0.08,5.0), xytext=(.08+0.003, 5.0), size=14, color='red')
    ax.plot([.07], [6.5], marker="o", markersize=12, markeredgecolor="green", markerfacecolor="blue")
    ax.annotate("<< ADAS Recommendation", xy=(0.07,6.5), xytext=(.07+0.003, 6.5), size=14, color='darkblue')

    ax.set_xlabel('Risk')  # Add an x-label to the axes.
    ax.set_ylabel('Revenue ($M)')  # Add a y-label to the axes.
    ax.set_title("Pareto Front: Risk – Revenue Tradeoff")  # Add a title to the axes.
    ax.legend()

    script = mpld3.fig_to_html(fig)    
    return render_template("proto.html", tabtitle='ASAS', graphScript=Markup(script))



