from __future__ import divisionimport sysfrom math import *from numpy import *import numpyfrom matplotlib import pyplot as pltfrom Thesis_lib import *# first we create the incoming propagation vector K and electric field EK=array([1,0,0])print "Propagation Vector: "+str(K)Sigma=numpy.random.rand()*(pi)                   #generating random angle of E prop. E=array([0,cos(Sigma),sin(Sigma)])print "Propagation E Field: " +str(E)# we then rotate the frames so that the electric field is in the y directionEp=Rotation(E,-Sigma)Kp=Kprint "Rotated Propagation E Field: " +str(Ep)# we now generate the scattering angles Theta and Phi(is in the Theta_Find FunctionTheta=Theta_Find(5)                    print "Angle of Scatter: " +str(Theta)#Find Scattered vectorKdp = Scatter_Vectors(K,Theta)print "Scatter Vector: "+str(Kdp)#Find Scattered EFieldEdp=Scatter_EField(K,Kdp, E)print "Scatter E Field: " +str(Edp)#Counter rotate scattered EFieldEtp=Rotation(numpy.array([0,cos(Sigma),sin(Sigma)]),Sigma)print 'Scatter Counter-Rotated E Field: ' +str(Etp)