
##########################################

def histograma(lista, name_h, flag_normalize, maximo, minimo):
        
   # print "IMPUT:",name_h,lista, max(lista), min(lista)
    dict_value_prob={}
    dict_value_cumulat_prob={}


# 0,4 for infection, -2,6 for persuasion  (for 30 iter)
    if maximo ==None:
        maximo=int(max(lista) +2)

     

    if minimo==None:
        minimo=int(min(lista) )
   

    
    
  #  print "max:",maximo,"min:", minimo

   
    for i in range(minimo, maximo):  # min included, max not included
        #if i in lista:
            dict_value_prob[i]=0.
            dict_value_cumulat_prob[i]=0.


   
    norm=0.
    for item in lista:  #Calculate Prob(i)       
        dict_value_prob[item]+=1.        
        norm+=1.

   # print dict_value_prob


    for item in lista: #Calculate Cumulat Prob(i)
        for key in sorted(dict_value_prob.iterkeys()):
            if key <= item:
                dict_value_cumulat_prob[key]+=1.


   


    list_freq=[]
    file = open(name_h,'wt')
    for key in sorted(dict_value_prob.iterkeys()):
        print >> file,key, dict_value_prob[key]/norm ,dict_value_prob[key]  
        if flag_normalize==0:
            list_freq.append(int(dict_value_prob[key] ))
        elif flag_normalize==1:
            list_freq.append(dict_value_prob[key]/norm )
        else:
            print "wrong flag_normalize value!"
    file.close()
        



    file2 = open(name_h.split(".dat")[0]+"_cumulat.dat",'wt')
    for key in sorted(dict_value_cumulat_prob.iterkeys()):
        print >> file2,key, dict_value_cumulat_prob[key]/norm, dict_value_cumulat_prob[key]
    file2.close()
        

  #  print "OUTPUT:",list_freq
   # raw_input()
    return(list_freq,maximo,minimo)



