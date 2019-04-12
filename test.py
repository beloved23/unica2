# import threading

# def worker(num):
#     """thread worker function"""
#     print 'Worker: %s' % num
#     return

# threads = []
# for i in range(5):
#     t = threading.Thread(target=worker, args=(i,))
#     threads.append(t)
#     t.start()
#     print 'ayanfe'

# def count(S, m, n ): 
  
#     # If n is 0 then there is 1 
#     # solution (do not include any coin) 
#     if (n == 0): 
#         return 1
  
#     # If n is less than 0 then no 
#     # solution exists 
#     if (n < 0): 
#         return 0; 
  
#     # If there are no coins and n 
#     # is greater than 0, then no 
#     # solution exist 
#     if (m <=0 and n >= 1): 
#         return 0
  
#     # count is sum of solutions (i)  
#     # including S[m-1] (ii) excluding S[m-1] 
#     return count( S, m - 1, n ) + count( S, m, n-S[m-1] ); 



# count([1,3,4], 4, 4)

def count(money,coins): 
    m = len(coins)
    res = [0 for k in range(money+1)]  
    res[0] = 1
    for i in range(0,m): 
        for j in range(coins[i],money+1): 
            res[j] += res[j-coins[i]] 
    return res[money]
x = count(4, [1,2]) 
print (x) 