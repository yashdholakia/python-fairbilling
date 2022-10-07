import billing

for file_n in range(1,10):
    print("Processing ", "input{}.txt".format(file_n))
    billing.main_executor("input{}.txt".format(file_n))
