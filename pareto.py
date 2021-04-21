import numpy as np
## 填充空值

def fillna(filename):
    filename1 = filename.fillna(0)
    return filename1

## 帕累托主程序

def pareto(table,amt,key_cols):
    amt_threshold = table[amt].sum() * 0.8
    table_1 = table.groupby(by = key_cols).agg({amt:np.sum})
    table_2 = table_1.sort_values(by = amt, ascending=False)
    accum_amt = [0 for a in range(int(table_2.count()))]
    for df_keys,df_values in table_2.iteritems():
        for i in range(int(table_2.count())):
            if i == 0:
                accum_amt[i] = df_values[i]
            else:
                accum_amt[i] = accum_amt[i-1] + df_values[i]
            i += 1
    table_2['accum_amt'] = accum_amt
    pareto = table_2[table_2['accum_amt']<amt_threshold]
    pareto_cnt = pareto[amt].count()
    pareto_amt = pareto[amt].sum()
    return pareto,pareto_amt,pareto_cnt