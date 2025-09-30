a=int(input('enter the value:'))
k=1
for i in range(1,a+1): 
  for s in range(0,a-i):
      print('',end='')
  for j in range (1,i):
      print('{0}'.format(k),end=' ')
      k=k+1
  print('\n')
