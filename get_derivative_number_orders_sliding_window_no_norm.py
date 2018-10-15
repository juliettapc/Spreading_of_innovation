 #!/usr/bin/env python

import scipy
import numpy

def main():
 
             


    time_window=40


    total_number_PCT=86.  #because i wanna plot the derivative of the cumulative number of orders, not of the fraction of orders
    total_number_cell=945.



    ############# input file
    filename_actual_evol="/home/staff/julia/at_Northwestern/idea_propagation_hospital/Idea-Spread-Hospital/Data/normalized_cumulative_num_culture_test_pct_vs_days.csv"    


    #filename_actual_evol="/home/staff/julia/at_Northwestern/idea_propagation_hospital/Idea-Spread-Hospital/Code/for_testing.dat"

    ############ output files
    output_file=filename_actual_evol.split(".")[0]+"_derivative_no_norm.dat"
    file = open(output_file,'wt')    
  

    output_file2=filename_actual_evol.split(".")[0]+"_derivative_sliding_window"+str(time_window)+"_no_norm.dat"
    file2 = open(output_file2,'wt')    
 


    
    file1=open(filename_actual_evol,'r')       
    list_lines_file=file1.readlines()
    

    dict_index_day={}
    dict_day_index={}

    list_cell_culture_orders=[]      
    list_PCT_orders=[]  
    cont=0
    for line in list_lines_file:      # [1:]:   # i exclude the first row            
        day=int(line.split(" ")[0])      
        
        cell_cult= float(line.split(" ")[1]) * total_number_cell      
        PCT= float(line.split(" ")[2]) *total_number_PCT      
        
        list_cell_culture_orders.append([day, cell_cult])  
        list_PCT_orders.append([day, PCT]) 

        dict_day_index[day]=cont     # because not every single day has a data entry
        dict_index_day[cont]=day

      #  print "dict:",dict_day_index[day],dict_index_day[cont]


        cont +=1

    
    list_derivative_cell_cult=[]
    list_derivative_PCT=[]


    for i in range(len(list_PCT_orders)-1):
       

        derivative_cell=(list_cell_culture_orders[i+1][1]-list_cell_culture_orders[i][1]) / (list_cell_culture_orders[i+1][0]-list_cell_culture_orders[i][0])

        derivative_PCT=(list_PCT_orders[i+1][1]-list_PCT_orders[i][1]) / (list_PCT_orders[i+1][0]-list_PCT_orders[i][0])



        list_derivative_cell_cult.append([list_cell_culture_orders[i][0]+(list_cell_culture_orders[i+1][0]-list_cell_culture_orders[i][0])/2., derivative_cell])
        list_derivative_PCT.append([list_PCT_orders[i][0]+(list_PCT_orders[i+1][0]-list_PCT_orders[i][0])/2., derivative_PCT])
        

        print >> file, list_PCT_orders[i][0]+(list_PCT_orders[i+1][0]-list_PCT_orders[i][0])/2., derivative_cell, derivative_PCT
        print i, "times:",list_PCT_orders[i][0],list_PCT_orders[i+1][0], list_PCT_orders[i][0]+(list_PCT_orders[i+1][0]-list_PCT_orders[i][0])/2., "   values:",list_cell_culture_orders[i][1],list_cell_culture_orders[i+1][1], "  ",list_PCT_orders[i][1],list_PCT_orders[i+1][1],"   deriv:",derivative_cell, derivative_PCT

       


    file.close()






   ######## i smooth out the derivatives by taking the average over a time window

   

    w_ini=list_PCT_orders[0][0]   #0
    last_day=list_PCT_orders[-1][0]   #244
    
   
 
    while w_ini  < last_day:             
        list_for_avg_derivative_cells=[]
        list_for_avg_derivative_PCT=[]

        for i in range(len(list_PCT_orders)-1):
            day=list_PCT_orders[i][0]

        
            if day >=  w_ini  and day <  w_ini+ time_window and day < last_day- time_window/2.:
                    index=dict_day_index[day]   
                    
                    
                    list_for_avg_derivative_cells.append(list_derivative_cell_cult[index][1])
                    list_for_avg_derivative_PCT.append(list_derivative_PCT[index][1])                

           


        if len(list_for_avg_derivative_cells) > 0 and w_ini +time_window/2. <= last_day-time_window/2.:
            print  w_ini +time_window/2., numpy.mean(list_for_avg_derivative_cells), numpy.mean(list_for_avg_derivative_PCT),numpy.mean(list_for_avg_derivative_PCT)/numpy.mean(list_for_avg_derivative_cells)
            print >> file2, w_ini +time_window/2., numpy.mean(list_for_avg_derivative_cells), numpy.mean(list_for_avg_derivative_PCT),numpy.mean(list_for_avg_derivative_PCT)/numpy.mean(list_for_avg_derivative_cells)

       

        w_ini += 1


    file2.close()



    print "original file:",filename_actual_evol
    print "derivative file:",output_file
    print "derivative sliding window file:",output_file2

 



##################################################
######################################
if __name__ == '__main__':
   # if len(sys.argv) > 1:
       
    main()
    
    
