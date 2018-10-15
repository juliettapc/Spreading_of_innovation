#! /usr/bin/env python


#for i in range(1):#
def integral(lista_tuplas, starting_point):   #x,y values
    #print lista_tuplas, starting_point
    #starting_point=0.
  
    
    x_old=lista_tuplas[0][0]
    y_old=lista_tuplas[0][1]
    
    area=0.
    if starting_point < lista_tuplas[0][0]:

        cont=0
        for item in lista_tuplas:      
            x= item[0]
            y=item[1]
            if cont==0:
                area+= (x-starting_point)*y  # the rectangle to the left of the first datapoint
         
            else:
                area+= (x-x_old)*( (y-y_old)/2.+y_old)
               # print x,x_old,"--",y,y_old,"area",area
            x_old=x
            y_old=y
            
            cont+=1
       

    else:
        cont=0
        for item in lista_tuplas:      
            x= item[0]
            y=item[1]
            
            if x >=starting_point:
                                   
                if cont>0:
                    area+= (x-x_old)*( (y-y_old)/2.+y_old)
                   # print x,x_old,"--",y,y_old,"area",area
                x_old=x
                y_old=y
            
                cont+=1
       
  
    print "area",area
   
    return area
