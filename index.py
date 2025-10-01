print("class usage")
class first:
    a=80
    def method(self): #self is mandatory when we use the fun in class
        print("hi")

o=first()
print(o.a)
o.a=78
print(o.a)
o.method()

class second(first):
    b=48
    def method1(self):
        print("hello")
        
s=second()
print(s.a)
print(s.b)
s.a=60
s.b=50
print(s.a)
print(s.b)
s.method1()
print()

print("modules usage")
import pass1
pass1.add(3,4)
import pass1 as p
p.sub(8,6)
from pass1 import *
mul(3,5)
div(8,4)
print()

print("numpy array detals")
import numpy as np
a=np.array([[1,9,3],[8,9,3]])
print("type",type(a))
print("dimension",a.ndim)
print("shape",a.shape)
print("size",a.size)
print("data",a.dtype)
print("elements",a)
print()
b=a.reshape(1,a.size)
print(b)
print()
c=np.arange(1,13)
print(c)
print(c.reshape(2,6))
print()
print(c.reshape(4,3))
print()
d=np.array([[1,2,3],[4,5,6]])
print(np.concatenate((a,d),axis=1))
print()
print(np.concatenate((a,d),axis=0))
print()
print(np.split(c,4))
print()
print(np.split(c,[3,8,10]))
print()

print("numpy basic operations")
e=np.array([1,2,3])
g=np.array([4,5,6])
print("e+g=",e+g)
print("e-g=",e-g)
print("e*g=",e*g)
print("e/g=",e/g)
print("e//g=",e//g)
print("e%g=",e%g)
print("e**g=",e**g)
print("sqrt(e)=",np.sqrt(e))
print("exp(e)=",np.exp(e))
print("log(e)=",np.log(e))
print("log10(e)=",np.log10(e))
print("sin(e)=",np.sin(e))
print()
print("a=\n",a)
print("sum(a)=",np.sum(a))
print("sum of (a) along axis 0 col=",np.sum(a,axis=0))
print("sum of (a) along axis 1 col=",np.sum(a,axis=1))
print("mean(a)=",np.mean(a))
print("min(a)=",np.min(a))
print("max(a)=",np.max(a))
print("standard deviation(a)=",np.std(a))
print("cummlative mean(a)=",np.cumsum(a))
print()
print("a=\n",a)
print("d=\n",d)
print("transpose of d=\n",d.T)
f=d.T
print("matrix multiplication=\n",a@f)
print("dot(a,f)=\n",np.dot(a,f))
h=np.array([[1,2],[3,4]])
print(h)
print("determinant(h)=\n",np.linalg.det(h))
print("squared(h)=\n",h**2)

i=np.array([[1,2,3],[4,5,6]],dtype='float')
print("array passed in list",i)
j=np.array((1,2,3))
print("tuple to list",j)
print("element from i ",i[1,2])
print("addition of i,j",i+j)
import pandas as pd
data=[1,2,3,4,5]
series=pd.Series(data)
print("series data in pandas\n",series)
data={
    'Name':["alice","boy","girl","nikki"],
    'Age':[22,25,23,25]
}
df=pd.DataFrame(data)
print("dataframe using pandas\n",df)
print("selecting multiple rows \n",df.iloc[[1,3]])
data={
    "A":[1,2,np.nan,5,6],
    "B":[8,9,3,4,np.nan],
    "C":[7,3,4,np.nan,6]
}
df=pd.DataFrame(data)
print("\noriginal data\n",df)
fill=df.fillna(0)
print("\nfilled with 0\n",fill)
fill=df.fillna(np.mean(df))
print("\nfilled with avg\n",fill)
df1=pd.DataFrame({
    "A":[1,2,3,4],
    "B":[5,6,7,8]
})
df2=pd.DataFrame({
    "A":[9,2,3,10],
    "D":[5,6,7,8]
})
print("\ninner merge\n",pd.merge(df1,df2,on="A",how="inner"))  #intersection
print("\nleft merge\n",pd.merge(df1,df2,on="A",how="left"))    #all rows from left
print("\nright merge\n",pd.merge(df1,df2,on="A",how="right"))  #all rows from right
print("\nouter merge\n",pd.merge(df1,df2,on="A",how="outer"))  #all rows

import matplotlib.pyplot as plt
df1.plot(kind="bar",x="A",y="B",legend=None)   #Valid plot kinds: ('line', 'bar', 'barh', 'kde', 'density', 'area', 'hist', 'box', 'pie', 'scatter', 'hexbin')
plt.xlabel('A')
plt.ylabel('B')
plt.title("basic graph")
plt.show()
print(df1)