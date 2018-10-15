import plottools_pygrace_Laura

x=[0,1,2,3,4,6,8,9]
y=[0,2,4,6,8,9,10,11]

xs=[[0,1,2,3,4,6,8,9],[0,2,4,6,8,9,10,11]]
ys=[[0,2,4,6,8,9,10,11],[0,12,14,16,18,19,20,21]]



xTitle="xTitle"
yTitle="yTitle"
title="titulo"
subtitle="subtitulo"
filename="./preba_plot_line.png"

plottools_pygrace_Laura.linegraph(x,y,xTitle,yTitle,title,subtitle,filename)



filename="./preba_plot_line_symbols.agr"  # or eps, ps, png, ...
plottools_pygrace_Laura.linegraphwpts(x,y,xTitle,yTitle,title,subtitle,filename)


list_yLegends=["whatever1","whatever2"]  # list of legends for the different series
filename="./preba_plot_multiple_lines.eps"
plottools_pygrace_Laura.realmultilinegraph(xs,ys,xTitle,yTitle,list_yLegends,title,subtitle,filename)



filename="./preba_plot_barplot.agr"
plottools_pygrace_Laura.bargraph(x,y,xTitle,yTitle,title,subtitle,filename)
