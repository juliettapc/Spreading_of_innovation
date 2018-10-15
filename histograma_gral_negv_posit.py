
##########################################

def histograma(lista, name_h,zeros=False):
        
  #  print lista

    dict_value_prob={}
    dict_value_cumulat_prob={}

    maximo=int(max(lista) +2)
    minimo=int(min(lista) -1  )
   # print name_h,maximo, minimo

   
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


   


   
    file = open(name_h,'wt')
    for key in sorted(dict_value_prob.iterkeys()):
        if zeros==False:    # i dont print out the null values of the distribution
            if dict_value_prob[key]!=0.:
                print >> file,key, dict_value_prob[key]/norm ,dict_value_prob[key]     
        if zeros==True:
            print >> file,key, dict_value_prob[key]/norm ,dict_value_prob[key]     

    file.close()
        



    file2 = open(name_h.split(".dat")[0]+"_cumulat.dat",'wt')
    for key in sorted(dict_value_cumulat_prob.iterkeys()):
        print >> file2,key, dict_value_cumulat_prob[key]/norm, dict_value_cumulat_prob[key]
    file2.close()
        
    print "written histogram:", name_h
