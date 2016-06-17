import os
from multiprocessing import Process
print ('Process (%s) start...' %os.getpid())

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
if __name__ == '__main__':
  with open("test.py") as ls:
    c = test_gen()
    print (help(ls))
    test_gen2(c)

 
