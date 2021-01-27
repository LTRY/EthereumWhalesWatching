import numpy as np
import matplotlib.pyplot as plt
import pymysql
import time

t = time.time()
conn = pymysql.connect("127.0.0.1", "root", "*******", "ETH")
cur = conn.cursor()
cur.execute('select `transactionCount` from `block_info`;')
results = cur.fetchall()
results_as_list = [i[0] for i in results]
array = np.fromiter(results_as_list, dtype=np.int32)

x = np.array(range(0, len(array)))
y = np.array(array)
plt.plot(x, y)
plt.title('transactionCount By Block')
plt.savefig('txByBlock.png', bbox_inches='tight')
print(time.time() - t)
plt.show()
