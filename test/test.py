#coding:gbk
import os
from multiprocessing import Process
#print ('Process (%s) start...' %os.getpid())

'''
pid = os.fork()
if pid == 0:
  print ("I am child process (%s) and my parent is %s" %(os.getpid(), os.getppid()))
else:
  print ("I (%s) just created a child process (%s)" %(os.getpid(), pid))
'''

def run_proc(name):
  print ("Run child process %s (%s)..." % (name, os.getpid()))
  #p = Process(target=run_proc, args=('test', ))
  #print ('Child process will start')
  #p.start()
  #p.join()
  #print ('process over')
def test_gen():
  n = 0 
  while True:
    r = yield n
    if (r != ''):
      n += 1
      print ('r is', r)
    else:
      return

def test_gen2(c):
  r = 1
  c.send(None)
  while r < 5:
    n = c.send(r)
    r += 1
    print ('n is', n)
  c.close()


'''
  print ("Run process %s"% os.getpid())
  p = Process(target=run_proc, args=('test', ))
  print ("Child process will start")
  p.start()
  p.join()
  print('Child process end.')
'''
def encode_file():
  with open ("jsformat.js", 'rb') as f:
    with open("jsformat2.js", "wb") as f2:
      print ("test______________")
      content = f.read().decode('gbk').encode('UTF8')
      print (content)
      f2.write(content)

class test_list():
  def __init__(self):
    self._children = []
  def add(self, l):
    self._children.append(l)    
  def __repr__(self):
    return self._children

def test_list2():
  t1 = test_list(1)
  t2 = test_list(2)
  t3 = test_list(3)
  print("t1:%s, t2:%s, t3:%s" %(str(t1), str(t2), str(t3))
  return (t1, t2, t3)

s2 = test_list2()
