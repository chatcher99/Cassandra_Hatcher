from __future__ import divisionimport sysfrom math import *from numpy import *import numpy as npfrom matplotlib import pyplot as pltfrom Thesis_lib import *outfile_E=open('Final_E_Fields.dat','w')outfile_K=open('Final_Scatter_Vectors.dat','w')nph= 10**4for p in range(nph):    # first we create the incoming propagation vector K and electric field E    K=array([1,0,0])    #print "Propagation Vector: "+str(K)    Sigma=np.random.rand()*(pi)                   #generating random angle of E prop.     E=array([0,cos(Sigma),sin(Sigma)])    #print "Propagation E Field: " +str(E)    # we then rotate the frames so that the electric field is in the y direction    Ep=Rotation(E,-Sigma)    Kp=K    #print "Rotated Propagation E Field: " +str(Ep)    # we now generate the scattering angles      Theta=Theta_Find(100)                       #Theta is off of y axis in xy plane (probability proportional to Theta^3)    Phi=np.random.rand()*2*pi                #Phi is off of x axis in xz plane (Randomly generated)    #Find Scattered vector    Kdp = Scatter_Vectors(Kp,Theta,Phi)    #print "Scatter Vector: "+str(Kdp)    #Find Scattered EField    Edp=Scatter_EField(K,Kdp, Ep)    #print "Scatter E Field: " +str(Edp)    #Counter rotate scattered EField and vector    Etp=Rotation(Edp,Sigma)    #print 'Scatter Counter-Rotated E Field: ' +str(Etp)    Ktp=Kdp    #create files to store vector data    writestring_E=str(Etp[0])+'\t'+str(Etp[1])+'\t'+str(Etp[2])+'\n'    outfile_E.write(writestring_E)    writestring_K=str(Ktp[0])+'\t'+str(Ktp[1])+'\t'+str(Ktp[2])+'\n'        outfile_K.write(writestring_K)    outfile_E.close()outfile_K.close()