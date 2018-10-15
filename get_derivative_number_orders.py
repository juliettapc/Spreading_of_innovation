 #!/usr/bin/env python

import scipy

def main():
 
             
    ############# input file
    filename_actual_evol="/home/staff/julia/at_Northwestern/idea_propagation_hospital/Idea-Spread-Hospital/Data/normalized_cumulative_num_culture_test_pct_vs_days.csv"    


    ############ output file
    output_file=filename_actual_evol.split(".dat")[0]+"_derivative.dat"

    file = open(output_file,'wt')    
  



    
    file1=open(filename_actual_evol,'r')       
    list_lines_file=file1.readlines()
    
    list_cell_culture_orders=[]      
    list_PCT_orders=[]  
    for line in list_lines_file:      # [1:]:   # i exclude the first row            
        day=int(line.split(" ")[0])      
        
        cell_cult= float(line.split(" ")[1])              
        PCT= float(line.split(" ")[2]) 
        
        list_cell_culture_orders.append([day, cell_cult])  
        list_PCT_orders.append([day, PCT]) 


    for i in range(len(list_PCT_orders)-1):
       

        derivative_cell=(list_cell_culture_orders[i+1][1]-list_cell_culture_orders[i][1]) / (list_cell_culture_orders[i+1][0]-list_cell_culture_orders[i][0])

        derivative_PCT=(list_PCT_orders[i+1][1]-list_PCT_orders[i][1]) / (list_PCT_orders[i+1][0]-list_PCT_orders[i][0])

     
        
        print >> file, list_PCT_orders[i][0]+(list_PCT_orders[i+1][0]-list_PCT_orders[i][0])/2., derivative_cell, derivative_PCT
        print i, "times:",list_PCT_orders[i][0],list_PCT_orders[i+1][0], list_PCT_orders[i][0]+(list_PCT_orders[i+1][0]-list_PCT_orders[i][0])/2., "   values:",list_cell_culture_orders[i][1],list_cell_culture_orders[i+1][1], "  ",list_PCT_orders[i][1],list_PCT_orders[i+1][1],"   deriv:",derivative_cell, derivative_PCT

       


    file.close()

    print "original file:",filename_actual_evol
    print "derivative file:",output_file



##################################################
######################################
if __name__ == '__main__':
   # if len(sys.argv) > 1:
       
    main()
    
    
