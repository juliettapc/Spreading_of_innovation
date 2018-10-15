 #plottools.py

'''
Goodies included in this file, with usage:

import plottools as pt

pt.linegraph(x,y,xTitle,yTitle,title,subtitle,filename)
    Plot a simple line graph
    x and y are lists of points.

pt.linegraphwpts(x,y,xTitle,yTitle,title,subtitle,filename)
    A linegraph with symbols

pt.multilinegraph(x,ys,xTitle,yTitle,yLabel,graphTitle,subtitle,filename)
    A multiple line graph where all y-series use the same x-values.
    x is a list of points, ys is a list of lists.

pt.realmultilinegraph(xs,ys,xTitle,yTitle,yLabel,graphTitle,subtitle,filename)
    A multiple line graph where each series has its own x and y values. 
    xis is a list of lists, ys is a list of lists.

pt.pointlinegraph(x_points,y_points,x,y,xTitle,yTitle,graphTitle,graphSubtitle,filename)
    Plot data points and a line on the same graph.

pt.pointjgraph(x_points,y_points,xTitle,yTitle,graphTitle,graphSubtitle,filename)
    Plot data points

pt.loglogpointgraph(x_points,y_points,xTitle,yTitle,graphTitle,subTitle,filename)
    Plot data points on log scale.

More code at the bottom... either not finished or very specific application.
'''

# IMPORTS ----------------------------------------------------------------------------------
from PyGrace.grace import Grace
from PyGrace.colors import ColorBrewerScheme

#-----------------------------------------------------------------------------------------------

# Series of colors to use throughout.
colors = [2,4,15,14,8,11]


#1:black
#2:red
#3: light green
#4:dark blue
#5:yellow
#6:light brown
#7:grey
#8:purple
#9:cyan
#10:pink
#11:orange
#12: purple2
#13:maroon
#14:cyan2
#15:dark green


#-----------------------------------------------------------------------------------------------

def linegraph(x,y,xTitle,yTitle,title,subtitle,filename):

    data = zip(x,y)
    
    grace = Grace()
    graph = grace.add_graph()
    
    graph.xaxis.label.text = xTitle
    graph.xaxis.label.char_size = .8
    graph.xaxis.ticklabel.format = 'Decimal'
    graph.xaxis.ticklabel.char_size = .8
    graph.xaxis.ticklabel.prec = 0
    
    graph.yaxis.label.text = yTitle
    graph.yaxis.label.char_size = .8 
    graph.yaxis.ticklabel.char_size = .8
    graph.yaxis.ticklabel.format = 'Decimal'
    graph.yaxis.ticklabel.prec = 0

    graph.title.text = title
    graph.title.size = .9 
    graph.subtitle.text = subtitle
    graph.subtitle.size = .7
   
    
    dataset1 = graph.add_dataset(data)
    dataset1.symbol.shape = 0
    grace.autoscale()
    grace.write_file(filename) 
    
#-----------------------------------------------------------------------------------------------

def linegraphwpts(x,y,xTitle,yTitle,title,subtitle,filename):

    data = zip(x,y)
    
    grace = Grace()
    graph = grace.add_graph()
    
    graph.xaxis.label.text = xTitle
    graph.xaxis.label.char_size = .8 
    graph.xaxis.ticklabel.format = 'Decimal'
    graph.xaxis.ticklabel.char_size = .8
    graph.xaxis.ticklabel.prec = 0
    
    graph.yaxis.label.text = yTitle
    graph.yaxis.label.char_size = .8 
    graph.yaxis.ticklabel.char_size = .8
    graph.yaxis.ticklabel.format = 'Decimal'
    graph.yaxis.ticklabel.prec = 0

    graph.title.text = title
    graph.title.size = 1.2
    graph.subtitle.text = subtitle
    graph.subtitle.size = .7
   
    
    dataset1 = graph.add_dataset(data)
    dataset1.symbol.shape = 1
    dataset1.symbol.size = 1.1
    grace.autoscale()
    grace.write_file(filename)
    
#-----------------------------------------------------------------------------------------------


def multilinegraph(x,ys,xTitle,yTitle,yLabel,graphTitle,subtitle,filename):
#ys is a list of y-series
    
    grace = Grace()
    graph = grace.add_graph()
    graph.title.text = graphTitle 
    graph.title.size = .8
    graph.subtitle.text = subtitle
    graph.subtitle.size = .6
    
    graph.xaxis.label.text = xTitle
    graph.xaxis.label.char_size = 1
    graph.xaxis.ticklabel.format = 'Decimal'
    graph.xaxis.ticklabel.char_size = .8
    graph.xaxis.ticklabel.prec = 2
    
    graph.yaxis.label.text = yTitle
    graph.yaxis.label.char_size = 1
    graph.yaxis.ticklabel.char_size = .8
    graph.yaxis.ticklabel.format = 'Decimal'
    graph.yaxis.ticklabel.prec = 2

    for [i,y] in enumerate(ys):
        dataset = graph.add_dataset(zip(x,y),legend=yLabel[i])
        dataset.symbol.shape = 0
        dataset.line.color = 1 

    grace.autoscale()
    grace.write_file(filename)

#-----------------------------------------------------------------------------------------------

def realmultilinegraph(xs,ys,xTitle,yTitle,list_yLegends,graphTitle,subtitle,filename):
#ys is a list of y-series
#xs is a list of x-series
    
    colors = [1,10,2,14,4]  # for each series


#1:black
#2:red
#3: light green
#4:dark blue
#5:yellow
#6:light brown
#7:grey
#8:purple
#9:cyan
#10:pink
#11:orange
#12: purple2
#13:maroon
#14:cyan2
#15:dark green

    grace = Grace()
    graph = grace.add_graph()
    graph.title.text = graphTitle 
    graph.title.size = 1.2
    graph.subtitle.text = subtitle
    graph.subtitle.size = .6
    
    graph.xaxis.label.text = xTitle
    graph.xaxis.label.char_size =  1
    graph.xaxis.ticklabel.format = 'Decimal'
    graph.xaxis.ticklabel.char_size = 1
    graph.xaxis.ticklabel.prec = 2
    
    graph.yaxis.label.text = yTitle
    graph.yaxis.label.char_size = 1
    graph.yaxis.ticklabel.char_size = 1
    graph.yaxis.ticklabel.format = 'Decimal'
    graph.yaxis.ticklabel.prec = 2

    for [i,y] in enumerate(ys):
        dataset = graph.add_dataset(zip(xs[i],y),legend=list_yLegends[i])
        dataset.symbol.shape = 1
        dataset.symbol.size = 0.5
        dataset.symbol.color = colors[i]
        dataset.symbol.fill_color = colors[i]
        dataset.line.color = colors[i]

    graph.legend.char_size = .6
    graph.legend.loc = (.2,.75)

    grace.autoscale()
    grace.write_file(filename)






#----------------------------------------------------------------------------------------------------

def pointlinegraph(x_points,y_points,x,y,xTitle,yTitle,graphTitle,graphSubtitle,filename):
#I think this adds datasets in the reverse order that I want? Fix me!

    grace = Grace()
    graph = grace.add_graph()
    graph.title.text = graphTitle
    graph.title.size = .8
    graph.subtitle.text = graphSubtitle
    graph.subtitle.size = .6
    
    graph.xaxis.label.text = xTitle
    graph.xaxis.label.char_size = 1
    graph.xaxis.ticklabel.format = 'Decimal'
    graph.xaxis.ticklabel.char_size = .8
    graph.xaxis.ticklabel.prec = 2
    
    graph.yaxis.label.text = yTitle
    graph.yaxis.label.char_size = 1
    graph.yaxis.ticklabel.char_size = .8
    graph.yaxis.ticklabel.format = 'Decimal'
    graph.yaxis.ticklabel.prec = 2

    points = graph.add_dataset(zip(x_points,y_points))
    points.symbol.shape = 3
    points.line.type = 0 
 
    line = graph.add_dataset(zip(x,y))
    line.symbol.shape = 0
    line.line.color = 1

    grace.autoscale()
    grace.write_file(filename)


#----------------------------------------------------------------------------------------------------

def pointgraph(x_points,y_points,xTitle,yTitle,graphTitle,subTitle,filename):

    grace = Grace()
    graph = grace.add_graph()
    graph.title.text = graphTitle
    graph.title.size = .9
    graph.subtitle.text = subTitle
    graph.subtitle.size = .7
    
    graph.xaxis.label.text = xTitle
    graph.xaxis.label.char_size = .8 
    graph.xaxis.ticklabel.format = 'Decimal'
    graph.xaxis.ticklabel.char_size = .8
    graph.xaxis.ticklabel.prec = 2
    
    graph.yaxis.label.text = yTitle
    graph.yaxis.label.char_size = .8 
    graph.yaxis.ticklabel.char_size = .8
    graph.yaxis.ticklabel.format = 'Decimal'
    graph.yaxis.ticklabel.prec = 2

    points = graph.add_dataset(zip(x_points,y_points))
    points.symbol.shape = 1
    points.line.color = 0
 
    grace.autoscale()
    grace.write_file(filename)



  #----------------------------------------------------------------------------------------------------

def loglogpointgraph(x_points,y_points,xTitle,yTitle,graphTitle,subTitle,filename):

    grace = Grace()
    graph = grace.add_graph()
    graph.title.text = graphTitle
    graph.title.size = .8
    graph.subtitle.text = subTitle
    graph.subtitle.size = .6
    
    graph.xaxis.label.text = xTitle
    graph.xaxis.label.char_size = 1
    graph.xaxis.ticklabel.format = 'Decimal'
    graph.xaxis.ticklabel.char_size = .8
    graph.xaxis.ticklabel.prec = 2
    graph.xaxis.scale = 'Logarithmic'
    
    graph.yaxis.label.text = yTitle
    graph.yaxis.label.char_size = 1
    graph.yaxis.ticklabel.char_size = .8
    graph.yaxis.ticklabel.format = 'Decimal'
    graph.yaxis.ticklabel.prec = 2
    graph.yaxis.scale = 'Logarithmic'

    points = graph.add_dataset(zip(x_points,y_points))
    points.symbol.shape = 1
    points.line.color = 0
 
    grace.autoscale()
    grace.write_file(filename)


  #----------------------------------------------------------------------------------------------------

def bargraph(x,y,xTitle,yTitle,title,subtitle,filename):

    data = zip(x,y)
    
    grace = Grace()
    graph = grace.add_graph()
    
    graph.xaxis.label.text = xTitle
    graph.xaxis.label.char_size = .9 
    graph.xaxis.ticklabel.format = 'Decimal'
    graph.xaxis.ticklabel.char_size = .7
    graph.xaxis.ticklabel.prec = 0
    
    graph.yaxis.label.text = yTitle
    graph.yaxis.label.char_size = .9 
    graph.yaxis.ticklabel.char_size = .7
    graph.yaxis.ticklabel.format = 'Decimal'
    graph.yaxis.ticklabel.prec = 0

    graph.title.text = title
    graph.title.size = 1 
    graph.subtitle.text = subtitle
    graph.subtitle.size = .8
    
    dataset1 = graph.add_dataset(data,type = 'bar')
    dataset1.symbol.shape = 0
    dataset1.line.type = 0
    grace.autoscale()
    grace.write_file(filename)

  #----------------------------------------------------------------------------------------------------

def sectionedbargraph(ys,xTitle,yTitle,yLabel,title,subtitle,filename):

    grace = Grace()
    graph = grace.add_graph()
    
    graph.xaxis.label.text = xTitle
    graph.xaxis.label.char_size = .8
    graph.xaxis.ticklabel.char_size = .8 
    graph.xaxis.ticklabel.format = 'Decimal'
    graph.xaxis.ticklabel.prec = 0
    
    
    graph.yaxis.label.text = yTitle
    graph.yaxis.label.char_size = .8 
    graph.yaxis.ticklabel.char_size = .8
    graph.yaxis.ticklabel.format = 'Decimal'
    graph.yaxis.ticklabel.prec = 0

    graph.title.text = title
    graph.title.size = .9
    graph.subtitle.text = subtitle
    graph.subtitle.size = .7

    base = 0
    for [i,y] in enumerate(ys):
        ylen = len(y)
        x = range(base, base + ylen)
        base += ylen - 1
        dataset = graph.add_dataset(zip(x,y), type = 'bar', legend=yLabel[i])
        dataset.line.type = 0
        dataset.symbol.color = colors[i]
        dataset.symbol.fill_color = colors[i]
        dataset.symbol.size = .2

    graph.legend.char_size = .6
    graph.legend.loc = (.8,.75)

    grace.autoscale()
    grace.write_file(filename)



  #----------------------------------------------------------------------------------------------------

def realmultilinegraph_log(xs,ys,xTitle,yTitle,yLabel,graphTitle,subtitle,filename):
#ys is a list of y-series
    
    grace = Grace()
    graph = grace.add_graph()
    graph.title.text = graphTitle 
    graph.title.size = .8
    graph.subtitle.text = subtitle
    graph.subtitle.size = .6
    
    graph.xaxis.label.text = xTitle
    graph.xaxis.label.char_size = .8
    graph.xaxis.ticklabel.format = 'Scientific'
    graph.xaxis.ticklabel.char_size = .6
    graph.xaxis.ticklabel.prec = 2
    graph.xaxis.scale = 'Logarithmic'
    
    graph.yaxis.label.text = yTitle
    graph.yaxis.label.char_size = .8
    graph.yaxis.ticklabel.char_size = .6
    graph.yaxis.ticklabel.format = 'Scientific'
    graph.yaxis.ticklabel.prec = 2
    graph.yaxis.scale = 'Logarithmic'

    for [i,y] in enumerate(ys):
        dataset = graph.add_dataset(zip(xs[i],y),legend=yLabel[i])
        dataset.symbol.shape = 3
        dataset.line.color = colors[i]
        dataset.symbol.color = colors[i]
        dataset.symbol.fill_color = colors[i]

    graph.legend.char_size = .6
    graph.legend.loc = (.2,.75)

    grace.autoscale()
    grace.write_file(filename)


