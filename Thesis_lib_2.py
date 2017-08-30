from __future__ import divisionimport sysfrom math import*import numpy as npfrom numpy import*def Theta_Find(num_pts):    XX=[]    for i in range(num_pts):                  #generate random x values for sine graph and scatter        x=np.random.rand()*np.pi              #same x values for both sine scatter allows for easier comparison because we can now just focus on the discrpancies in Y values        XX.append(x)    Xsine=XX                                  #sort random values so that when plotting sine it will be correct    Ysine=np.sin(Xsine)**3                    #generates y values for sin^3 graph    YY=[]    for t in range(len(Xsine)):               #generates random y value for random scatter, for every X value.         y=np.random.rand()                           YY.append(y)    Xscat=[]            Yscat=[]    for i in range(len(YY)):                  #compares y values of scatter to y values of sine at cooresponding x values        if YY[i]<= Ysine[i]:            Yscat.append(YY[i])            Xscat.append(Xsine[i])    Theta=Xscat[0]    #print "Theta: "+str(Theta)    return Thetadef Scatter_Vectors(Theta,Phi):        Kxx=sin(Theta)*cos(Phi)    Kyy=cos(Theta)    Kzz=sin(Theta)*sin(Phi)        Kdp=(Kxx,Kyy,Kzz)                                #Scatter Vector    return np.array(Kdp)def Scatter_EField(Kdp,Ep):        L=np.cross(Kdp,Ep)                                 #vector orthoganal to the plane formed by E and KK        Lx=L[0]    Ly=L[1]    Lz=L[2]    Kxx=Kdp[0]    Kyy=Kdp[1]    Kzz=Kdp[2]    Exx= (1/(1+((Ly*(Kxx-(Lx*Kzz/Lz)))/(Lz*(Kyy-(Ly*Kzz/Lz))))**2+(-(Kxx-(Lx*Kzz/Lz))/(Kyy-(Ly*Kzz/Lz)))**2))**(1/2)    Eyy= - Exx*(Kxx-(Lx*Kzz/Lz))/(Kyy-(Ly*Kzz/Lz))    Ezz= (Exx/Lz)*((Ly*(Kxx-(Lx*Kzz/Lz))/(Kyy-(Ly*Kzz/Lz)))-Lx)    Edp=np.array([Exx,Eyy,Ezz])    Edp=Edp/np.sqrt(np.sum(Edp**2))                                   #E field of propogation    return Edpdef Rotation(E,Sigma):    Rotate=np.matrix([[1,0,0],[0,np.cos(Sigma),-np.sin(Sigma)],[0,np.sin(Sigma),np.cos(Sigma)]])    Erotate=E*Rotate    Erotate2=np.empty(3)    Erotate2[0]=Erotate[0,0]    Erotate2[1]=Erotate[0,1]    Erotate2[2]=Erotate[0,2]    return Erotate2def EField_Comps(Detect,nph):    #Select Vectors in Direction of Detector     kx,ky,kz=loadtxt('Exit_Vectors.dat',unpack=True)    Ex,Ey,Ez=loadtxt('Exit_EFields.dat',unpack=True)    outfile_SV=open('Selected_Exit_Vectors.dat','w')    outfile_SE=open('Selected_Exit_EFields.dat','w')        #Detect=np.array([0.001,0.001,1])    #print "Detector: " +str(Detect)    DetLength=np.linalg.norm(Detect)    DFD=5                  #degrees off of detector vector that are accepted    i=0    while i < nph:              vect=np.array([kx[i],ky[i],kz[i]])          #takes vector        VectLength=np.linalg.norm(vect)             #norm of vector        a=(np.dot(vect,Detect))/(DetLength*VectLength)  #determines the angles between the scatter vector and the detector vector        omega=np.arccos(a)        if omega <= np.deg2rad(DFD):        #if this angle is within our degreees of freedom = keep            writestring_SV=str(kx[i])+'\t'+str(ky[i])+'\t'+str(kz[i])+'\n'            outfile_SV.write(writestring_SV)            writestring_SE=str(Ex[i])+'\t'+str(Ey[i])+'\t'+str(Ez[i])+'\n'            outfile_SE.write(writestring_SE)        i+=1    outfile_SV.close()    outfile_SE.close()    x,y,z=loadtxt('Selected_Exit_Vectors.dat',unpack=True)    Ex,Ey,Ez=loadtxt('Selected_Exit_EFields.dat',unpack=True)    #Find EField Compents in Detector Reference Frame    outfile_EC=open('Exit_EField_Comps.dat','w')    D=Detect    XD=np.array((1/(D[0]**2+D[1]**2+D[2]**2))**(1/2)*D)                                        #direction of detector=xaxis of detector reference frame=line through back of detector    ZD=np.array([ (-sign(XD[0])*XD[2]/(XD[0]**2+XD[2]**2)**(1/2)) , 0 , (1-(XD[2]**2/(XD[0]**2+XD[2]**2)))**(1/2) ])     #z axis of the detector    Zy= (1/((XD[0]**2/XD[2]**2)+((XD[0]**2+XD[2]**2)**2/(XD[1]**2*XD[2]**2))+1))**(1/2)    YD=np.array([(Zy*XD[0]/XD[2]), -((Zy/XD[1])*((XD[0]**2+XD[2]**2)/XD[2])), Zy])     #is the yaxis of the detector reference frame    #print "Number of Photons: " +str(len(Ex))    for i in range(Ex.size):        E=(Ex[i],Ey[i],Ez[i])        Ecx=np.dot(E,XD)/np.linalg.norm(XD)        Ecy=np.dot(E,YD)/np.linalg.norm(YD)        Ecz=np.dot(E,ZD)/np.linalg.norm(ZD)        writestring_EC=str(Ecx)+'\t'+str(Ecy)+'\t'+str(Ecz)+'\n'        outfile_EC.write(writestring_EC)                    Ep=(Ecx,Ecy,Ecz)    outfile_EC.close()    return  def Stokes(EFieldComps):    #Calculate componets of Efields on each axis    Ecx,Ecy,Ecz=loadtxt('Exit_EField_Comps.dat', unpack=True)    outfile_P=open('Polarization_NEW.dat','w')            a=array([sqrt(2),sqrt(2)])          #rotates axes    b=array([sqrt(2),-sqrt(2)])    EZ=np.zeros([Ecx.size])    EY=np.zeros([Ecx.size])    Ea=np.zeros([Ecx.size])    Eb=np.zeros([Ecx.size])            for i in range(Ecx.size):        Ec=array([Ecy[i], Ecz[i]])        EZ[i]=Ecz[i]        EY[i]=Ecy[i]        Ea[i]=np.dot(Ec,a)        Eb[i]=np.dot(Ec,b)    #Compute Stokes Parameters    EZ2=EZ**2    EY2=EY**2    Ea2=Ea**2    Eb2=Eb**2    I=sum(EZ2)/Ecx.size + sum(EY2)/Ecx.size    Q=sum(EZ2)/Ecx.size - sum(EY2)/Ecx.size    U=sum(Ea2)/Ecx.size - sum(Eb2)/Ecx.size    P=np.sqrt(Q**2+U**2)/I    outfile_P.write(str(P))    outfile_P.close()    return Pdef Rot3D(K,Theta,Phi):    RotateY=np.matrix([[np.cos(Phi),0,np.sin(Phi)],[0,1,0],[-np.sin(Phi),0,np.cos(Phi)]])    RotateZ=np.matrix([[np.cos(Theta),np.sin(Theta),0],[-np.sin(Theta),np.cos(Theta),0],[0,0,1]])        KRot=K*RotateZ          #K vector after rotation about y axis    KK=KRot*RotateY         #K vector after rotation about z axis        KR= np.empty(3)     KR[0]=KK[0,0]    KR[1]=KK[0,1]    KR[2]=KK[0,2]    return KRdef CoRot3D(K,Theta,Phi):    RotateY=np.matrix([[np.cos(Phi),0,-np.sin(Phi)],[0,1,0],[np.sin(Phi),0,np.cos(Phi)]])    RotateZ=np.matrix([[np.cos(Theta),-np.sin(Theta),0],[np.sin(Theta),np.cos(Theta),0],[0,0,1]])    KRot=K*RotateY          #K vector after rotation about y axis    KK=KRot*RotateZ         #K vector after rotation about z axis            KR= np.empty(3)     KR[0]=KK[0,0]    KR[1]=KK[0,1]    KR[2]=KK[0,2]        return KRdef EllipCloud(Theta,Phi,a,b,c):    #outer radii of ellipitcal cloud    X=a*np.outer(np.cos(Phi),np.sin(Theta))    Y=c*np.outer(np.ones(np.size(Phi)),np.cos(Theta))    Z=b*np.outer(np.sin(Phi),np.sin(Theta))    R=(X**2+Y**2+Z**2)**(1/2)        return Rdef Photon_Propagation(Lambda):    d=Lambda*(-np.log(np.random.rand()))       #distance traveled based on mean free path    k=np.array([d,0,0])    Theta = np.arccos((np.random.rand()*2)-1)  #randomly generate direction of photo    Phi = np.random.rand()*2*np.pi    #print("Theta: "+str(Theta))    ThetaPrime=np.pi/2-Theta        Sigma=np.random.rand()*(pi)                 #Random angle for Efield     e=array([0,np.cos(Sigma),np.sin(Sigma)])    ### 1st Rotation gives propagation vectors ###    K=Rot3D(k,ThetaPrime,Phi)                   #Propagation Vector    E=Rot3D(e,ThetaPrime,Phi)    return K,E,Theta,Phidef Compton_Scatter(K,E,Lambda):            ### Single Scattering Function ###    #### Find New Angles ####    # Find Theta #    Theta2 = np.arccos(K[1]/(K[0]**2+K[1]**2+K[2]**2)**(1/2))          ThetaPrime = np.pi/2 - Theta2    #print("Theta2: "+str(Theta2))    # Find Phi #    if np.sign(K[0]) == 1:        if np.sign(K[2]) == 1:            Phi = np.arctan(K[2]/K[0])        if np.sign(K[2]) == -1:            Phi =(3*np.pi/2)+np.abs(np.arctan(K[0]/K[2]))    if np.sign(K[0]) == -1:        if np.sign(K[2]) == 1:            Phi =(np.pi/2)+ np.abs(np.arctan(K[0]/K[2]))        if np.sign(K[2]) == -1:            Phi =(np.pi)+ np.arctan(K[2]/K[0])    if np.sign(K[0]) == 0:        Phi = np.pi/2    if np.sign(K[2]) == 0:        Phi = 0    # Find Sigma #    e = CoRot3D(E,ThetaPrime,Phi)        Sigma = np.arccos(e[1]/(e[0]**2+e[1]**2+e[2]**2)**(1/2))    ### Find Scatter Vectors ###    ThetaScat = Theta_Find(100)    PhiScat = np.random.rand()*2*pi    d=Lambda *(-np.log(np.random.rand()))    KS = d*(Scatter_Vectors(ThetaScat,PhiScat))    ES = Scatter_EField(KS,E)    ## Rotation #2 counter rotate #1 ###    KSp = CoRot3D(KS,ThetaPrime,Phi)    ESp = CoRot3D(ES,ThetaPrime,Phi)    ## Rotation #3 Counter Rotate for Sigma ###    KSP = Rotation(KSp,Sigma)    ESP = Rotation(ESp,Sigma)    #print(ESP)        return KSP,ESP,KSp,ESpdef Cloud_Scatter(nph,a,b,c):    outfile_V=open('Exit_Vectors.dat','w')    outfile_E=open('Exit_EFields.dat','w')    ####Define parameters####    C=3.0*10**8             #m/s    alpha = 0.8    Lambda = alpha*a       #R/T #Mean Free Path    TimeS=np.empty(nph)     #create empty array for time values     for p in range(nph):        K,E,Theta,Phi = Photon_Propagation(Lambda)          #Create Initial Propagation Vectors                R=EllipCloud(Theta,Phi,a,b,c)[0,0]                  #Radius of cloud at angle of propagation        #print(R)        X=K[0]        Y=K[1]        Z=K[2]        D=np.linalg.norm(K)                     #Distance from orgin        #print(D)        i=0        #TimeT=np.linalg.norm(K)/C               #initial time of travel        while D <= R:                            #Scatter Process            KSP,ESP,KSp,ESp = Compton_Scatter(K,E,Lambda)    #Scatters propagation vector            X=X+KSP[0]            Y=Y+KSP[1]            Z=Z+KSP[2]            D=(X**2+Y**2+Z**2)**(1/2)                      #find angle D is away from y axis now            ThetaR=np.arccos(Y/D)            #find angle D is away from x axis now            if np.sign(X) == 1:                if np.sign(Z) == 1:                    PhiR = np.arctan(Z/X)                if np.sign(Z) == -1:                    PhiR =(3*np.pi/2)+np.abs(np.arctan(X/Z))                                    if np.sign(X) == -1:                if np.sign(Z) == 1:                    PhiR =(np.pi/2)+ np.abs(np.arctan(X/Z))                if np.sign(Z) == -1:                    PhiR =(np.pi)+ np.arctan(Z/X)            if np.sign(Z)==0:                PhiR=0            if np.sign(X)==0:                PhiR=np.pi/2            R=EllipCloud(ThetaR,PhiR,a,b,c)[0,0]      #Radius at angle of scatte            ## Reset Vectors ##            K=KSP            E=ESP                        #Time=(np.linalg.norm(K)/C)                                  #Time per scatter displacement            #TimeT=TimeT+Time                            #Total Time of photon motion                        i+=1        #print ('Number of Scatters: '+str(i))                Rd=D-R                                          #Distance traveled after leaving the star         #if TimeT==0:        #    TimeS[p]=0        #else:        #    TimeS[p]=(TimeT-(Rd/C))                         #Total time of photon motion while in the star           if i == 0:            writestring_V=str(K[0])+'\t'+str(K[1])+'\t'+str(K[2])+'\n'            writestring_E=str(E[0])+'\t'+str(E[1])+'\t'+str(E[2])+'\n'        else:            writestring_V=str(KSp[0])+'\t'+str(KSp[1])+'\t'+str(KSp[2])+'\n'            writestring_E=str(ESp[0])+'\t'+str(ESp[1])+'\t'+str(ESp[2])+'\n'                    outfile_V.write(writestring_V)        outfile_E.write(writestring_E)           outfile_V.close()    outfile_E.close()        return