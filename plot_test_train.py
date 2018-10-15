import csv
import libreria_plottools_pygrace


def main():




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











    #####################
    # Train-test figure #
    #####################

    filename1="../Results/network_final_schedule_withTeam3_local/Time_evolutions_Persuasion_training_alpha0.1_damping0.2_mutual_encourg0.1_threshold0.2_unif_distr_100iter_2012_seed31Oct_finalnetwork.dat"

    list_x1, list_y1 = read_file_return_listXY(filename1, 0,1,' ')
    

  #  for i in range(len(list_x1)):
   #     print list_x1[i], list_y1[i] 


    filename2="../Results/network_final_schedule_withTeam3_local/Time_evolutions_Persuasion_testing_avg_ic_alpha0.1_damping0.2_mutual_encourg0.1_threshold0.2_unif_distr_100iter_2012_seed31Oct_finalnetwork.dat"

   
    list_x2, list_y2 = read_file_return_listXY(filename2, 0,1, ' ')
   

   # for i in range(len(list_x2)):
    #    print list_x2[i], list_y2[i] 


    filename3="../Results/actual_time_evol_for_gnuplot.dat"

   
    list_x3, list_y3 = read_file_return_listXY(filename3, 0, 3,'\t')  # columns where the data is, delimeter fields

   # for i in range(len(list_x3)):
    #    print list_x3[i], list_y3[i] 




    filename4="../Results/network_final_schedule_withTeam3_local/infection/Average_time_evolution_Infection_training_p0.99_Immune0.7_1000iter_2012_avg_ic.dat"
    list_x4, list_y4 = read_file_return_listXY(filename4, 0, 1,' ') 



    filename5="../Results/network_final_schedule_withTeam3_local/infection/Average_time_evolution_Infection_testing_avg_ic_p0.9_Immune0.7_1000iter_2012_avg_ic.dat"
    list_x5, list_y5 = read_file_return_listXY(filename5, 0, 1,' ')  # columns where the data is, delimeter fields









    list_xs=[]
    list_xs.append(list_x3)
    list_xs.append(list_x1)
    list_xs.append(list_x2)
    list_xs.append(list_x4)
    list_xs.append(list_x5)




    list_ys=[]
    list_ys.append(list_y3)
    list_ys.append(list_y1)
    list_ys.append(list_y2)
    list_ys.append(list_y4)
    list_ys.append(list_y5)




    xTitle="days"
    yTitle="# of adopters"
    title="best fit training-testing"
    subtitle=""
    list_yLegends=["Actual evolution","training persuasion","testing persuasion","training infection","testing infection"]  # list of legends for the different series

    filename="../Results/training_testing.agr"
    libreria_plottools_pygrace.realmultilinegraph(list_xs,list_ys,xTitle,yTitle,list_yLegends,title,subtitle,filename)


    filename2="../Results/training_testing.png"
    libreria_plottools_pygrace.realmultilinegraph(list_xs,list_ys,xTitle,yTitle,list_yLegends,title,subtitle,filename2)



    print "\ncreated figures:",filename,"   ",filename2











    #####################
    # Best fit figure #
    #####################


    filename1="../Results/actual_time_evol_for_gnuplot.dat"
   
    list_x1, list_y1 = read_file_return_listXY(filename1, 0, 3,'\t') 

  



    filename2="../Results/save/Time_evolutions_Persuasion_alpha0.1_damping0.3_mutual_encourg0.3_threshold0.2_unif_distr_100iter_2012_seed31Oct_finalnetwork.dat"

    list_x2, list_y2 = read_file_return_listXY(filename2, 0,1,' ')


    filename3="../Results/save/Average_time_evolution_Infection_p0.9_Immune0.5_1000iter_2012.dat"

    list_x3, list_y3 = read_file_return_listXY(filename3, 0,1,' ')






    list_xs=[]
    list_xs.append(list_x1)
    list_xs.append(list_x2)
    list_xs.append(list_x3)

    list_ys=[]  
    list_ys.append(list_y1)
    list_ys.append(list_y2)
    list_ys.append(list_y3)
   



    xTitle="days"
    yTitle="# of adopters"
    title="best fit"
    subtitle=""
    list_yLegends=["Actual evolution","best fit Persuasion","best fit Infection"]  # list of legends for the different series
    filename="../Results/best_fit.agr"
    libreria_plottools_pygrace.realmultilinegraph(list_xs,list_ys,xTitle,yTitle,list_yLegends,title,subtitle,filename)


    filename2="../Results/best_fit.png"
    libreria_plottools_pygrace.realmultilinegraph(list_xs,list_ys,xTitle,yTitle,list_yLegends,title,subtitle,filename2)



    print "\ncreated figures:",filename,"   ",filename2



###################################################          

def read_file_return_listXY(filename,column1, column2, delimeter):

    list_x=[]
    list_y=[]
    result_actual_file= csv.reader(open(filename, 'rb'), delimiter=delimeter)  
    for row in result_actual_file:                 
        try:
            list_x.append(float(row[column1]))
            list_y.append(float(row[column2]))
        except IndexError:
            print row
            raw_input() 
#            pass

    return list_x, list_y
     





##################################################
######################################
if __name__ == '__main__':
  #  if len(sys.argv) > 1:
   #     graph_filename = sys.argv[1]
   
    main()
    #else:
     #   print "Usage: python script.py path/network.gml"

    
