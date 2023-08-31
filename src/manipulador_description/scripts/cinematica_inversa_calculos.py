#! /usr/bin/env python
# Computing 
from math import acos,atan,sqrt,pi,cos,sin
from numpy import array

class calculos_cinematica_inversa():
      
     def cal_2GDL_arri(x,z,L1, L2):
        r=sqrt(x*x+z*z)
        a=atan(abs(z)/abs(x))
        b=acos((L1*L1+r*r-L2*L2)/(2*L1*r))
        c=acos((L1*L1-r*r+L2*L2)/(2*L1*L2))
     
        if x==0 and z==0:
                print("Sin coordenadas")
     
        ## condiciones para cada cuadrante del robot
        #Cuadrante 1
        elif x>0 and z>0:
                q1p=0
                q1=a+b
                q2=c-pi
        #Cuadrante 2
        elif x<0 and z>0 :
                q1p=b-a
                q1=pi+q1p
                q2=c-pi
        #Cuadrante 3
        elif x<0 and z<0 :
                q1p=a+b
                q1=pi+q1p
                q2=c-pi
        #Cuadrante 4
        elif x>0 and z<0 :
                q1p=-a-b
                q1=2*pi+q1p
                q2=pi-c
        
        q1g=q1*180/pi
        q2g=q2*180/pi
        #Desfase de q1:
        q1=pi/2-q1
        #Limites de las articulaciones
        if q1 < -1.57:
                q1=-1.57
        if q1 > 1.57:
                q1=1.57

        if q2 > 2.09:
                q2=2.09
        if q2 < -2.09:
                q2=-2.09

        #Retornamos el resultado
        result=array([q1,-q2])
        print(" ")
        print('Codo Arriba')
        print('Q1 vale en grados: ',q1g)
        print('Q2 vale en grados  ',q2g)
        print('El resultado en radianes es: ',-q1,q2)
        print("""
        
        
         """)
        return result
     
     def cal_2GDL_aba(x,z,L1,L2):
        r=sqrt(x**2+z**2)
        a=atan(abs(z)/abs(x))
        b=acos((L1**2+r**2-L2**2)/(2*L1*r))
        c=acos((L1**2-r**2+L2**2)/(2*L1*L2))
        if x==0 and z==0:
                print("Sin coordenadas")
        #Cuadrante1
        elif x>0 and z>0:
                q1p=0
                q1=a-b
                q2= pi-c
        #Cuadrante2
        elif x<0 and z>0 :
                q1p=-(a+b)
                q1=pi+q1p
                q2=pi-c
        #Cuadrante3
        elif x<0 and z<0 :
                q1p=a-b
                q1=pi+q1p
                q2= pi-c
        #Cuadrante4
        elif x>0 and z<0 :
                q1p= -(b+a)
                q1=2*pi+q1p
                q2=pi-c

        q1g=q1*180/pi
        q2g=q2*180/pi
        #Desfase de q1:
        q1=pi/2-q1
        #Limites de las articulaciones
        if q1 < -1.57:
                q1=-1.57
        if q1 > 1.57:
                q1=1.57

        if q2 > 2.09:
                q2=2.09
        if q2 < -2.09:
                q2=-2.09
                    
        #Retornamos el resultado
        result=array([q1,-q2])
        print(" ")
        print('Codo Abajo')
        print('Q1 vale en grados: ',q1g)
        print('Q2 vale en grados  ',q2g)
        print('El resultado en radianes es: ',-q1,q2)
        print("""
        
        
         """)
        return result
        


     def cal_3GDL_arri(x,z,qy,L1,L2,L3):
        print("Calculando para: x=",x,"z=",z)
        qy=abs(qy*pi/180)
        # Para el cuadrante 1
        if qy>=0 and qy<=pi/2:
                xp=x-L3*cos(qy)
                zp=z-L3*sin(qy)
        ## cuadrante 2
        elif qy>pi/2 and qy<= pi:
                xp=x+L3*cos(pi-qy)
                zp=z-L3*sin(pi-qy)
        ## cuadrante 3
        elif qy>pi and qy<=(3*pi)/2:
                xp=x+L3*cos(qy-pi)
                zp=z+L3*sin(qy-pi)
        ## cuadrante 4
        elif qy> (3*pi)/2 and qy<=2*pi:
                xp=x-L3*cos(2*pi-qy)
                zp=z+L3*sin(2*pi-qy)
        
        print("Valor de xp:",xp,"valor de zp:",zp)

        #Establecemos las ecuaciones para cada cuadrante
        #cuando no hay coordenadas
        if x==0 and z==0:
                print('Sin coordenadas')
        if z>0:
                #Cudrante 1
                if xp>0:
                        r=sqrt(xp*xp + zp*zp)
                        a=abs(atan(zp/xp))
                        b=acos((L1*L1+r*r-L2*L2)/(2*L1*r))
                        c=acos((L1*L1-r*r+L2*L2)/(2*L1*L2))
                        q1=a+b
                        q2=c-pi
                        q3=qy-q1-q2

                #Cuadrante 2
                elif xp<0:
                        r=sqrt(xp*xp + zp*zp)
                        a=abs(atan(zp/xp))
                        b=acos((L1*L1+r*r-L2*L2)/(2*L1*r))
                        c=acos((L1*L1-r*r+L2*L2)/(2*L1*L2))
                        q1p=b-a
                        q1=pi+q1p
                        q2=c-pi
                        q3=qy-q1-q2

        #cuadrante Negativo
        elif x>0 and z<0 :
                
                r=sqrt((xp*xp)+(zp*zp))
                a=abs(atan(zp/xp))
                b=acos((L1*L1+r*r-L2*L2)/(2*L1*r))
                c=acos((L1*L1-r*r+L2*L2)/(2*L1*L2))
                q1=(b-a)
                q2=-(pi-c)
                q3=qy-q1-q2

        q1g=q1*180/pi
        q2g=q2*180/pi
        q3g=q3*180/pi
        #Desfase de q1:
        q1=pi/2-q1
        #Limites de las articulaciones
        if q1 < -1.57:
                q1=-1.57
        if q1 > 1.57:
                q1=1.57

        if q2 > 2.09:
                q2=2.09
        if q2 < -2.09:
                q2=-2.09

        if q3 > 1.57 :
                q3=1.57
        if q3 < -2.1:
                q3=-2.1
        
        
        #Retornamos el resultado
        result=array([q1,-q2,-q3])
        print(" ")
        print('Codo Arriba')
        print('Q1 vale en grados: ',q1g)
        print('Q2 vale en grados  ',q2g)
        print('Q3 vale en grados: ',q3g)
        print('El resultado en radianes es: ',-q1,q2,q3)
        print("""
        
        
         """)
        return result  
      
     def cal_3GDL_aba (x,z,qy,L1,L2,L3):
        qy=abs(qy*pi/180)
        
        #Condiciones para cada cuadrante relativo del efector final
        #Primer Cuadrante
        if qy>=0 and qy<=pi/2:
                xp=x-L3*cos(qy)
                zp=z-L3*sin(qy)
        #Segundo cuadrante
        if qy>pi/2 and qy<=pi:
                xp=x+L3*cos(pi-qy)
                zp=z-L3*sin(pi-qy)
        #Tercer Cuadrante
        if qy>pi and qy<=(3*pi)/2:
                xp=x+L3*cos(qy-pi)
                zp=z+L3*sin(qy-pi)
        #Cuarto Cuadrante
        if qy>(3*pi)/2 and qy<=2*pi:
                xp=x-L3*cos(2*pi-qy)
                zp=z+L3*sin(2*pi-qy)
                
        print("Valor de xp:",xp,"valor de zp:",zp)
        #Ecuaciones para hallar R,a,b y c
        r=sqrt((xp*xp)+(zp*zp))
        a=abs(atan(zp/xp))
        b=acos((L1*L1+r*r-L2*L2)/(2*L1*r))
        c=acos((L1*L1-r*r+L2*L2)/(2*L1*L2))

        #Condiciones para el cuadrante del robot

        if x==0 and z==0:
                print('No coordenadas')
        if z>0:
                #Cudrante 1
                if xp>0:
                        r=sqrt(xp*xp + zp*zp)
                        a=abs(atan(zp/xp))
                        b=acos((L1*L1+r*r-L2*L2)/(2*L1*r))
                        c=acos((L1*L1-r*r+L2*L2)/(2*L1*L2))
                        q1=a-b
                        q2=pi-c
                        q3=qy-q1-q2

                #Cuadrante 2
                elif xp<0:
                        r=sqrt(xp*xp + zp*zp)
                        a=abs(atan(zp/xp))
                        b=acos((L1*L1+r*r-L2*L2)/(2*L1*r))
                        c=acos((L1*L1-r*r+L2*L2)/(2*L1*L2))
                        q1p=-(a+b)
                        q1=pi+q1p
                        q2=pi-c
                        q3=qy-q1-q2

        #cuadrante Negativo
        elif x<0 and z<0 :
                r=sqrt((xp*xp)+(zp*zp))
                a=abs(atan(zp/xp))
                b=acos((L1*L1+r*r-L2*L2)/(2*L1*r))
                c=acos((L1*L1-r*r+L2*L2)/(2*L1*L2))
                q1p=(b-a)
                q1=pi-q1p
                q2=pi-c
                q3=qy-q1-q2

        #Enviamos los resultados
        q1g=q1*180/pi
        q2g=q2*180/pi
        q3g=q3*180/pi

        #Desfase de q1:
        q1=pi/2-q1
        #Limites de las articulaciones
        if q1 < -1.57:
                q1=-1.57
        if q1 > 1.57:
                q1=1.57

        if q2 > 2.09:
                q2=2.09
        if q2 < -2.09:
                q2=-2.09

        if q3 > 1.57 :
                q3=1.57
        if q3 < -2.1:
                q3=-2.1
        
        
        #Retornamos el resultado
        result=array([q1,-q2,-q3])
        print(" ")
        print('Codo Abajo')
        print('Q1 vale en grados: ',q1g)
        print('Q2 vale en grados  ',q2g)
        print('Q3 vale en grados: ',q3g)
        print('El resultado en radianes es: ',-(pi/2-q1),q2,q3)
        return result  
