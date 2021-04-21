import pandas as pd
import sqlalchemy
import pareto
from sqlalchemy import create_engine
engine = create_engine('mysql+pymysql://yourdblogname:yourdbpasswd@localhost:3306/yourdatabase')

# python和sql二选一均可完成帕累托，需要使用哪种方法将另一种注释掉即可。
# python做帕累托
sql = 'select * from orders_2020;' #读取数据，也可以pd.read_csv(),需要包含user_id和用户支付金额
df = pd.read_sql_query(sql,engine)
df_fillna = pareto.fillna(df)  #填充空值
df_pareto = pareto.pareto(df_fillna, 'pay_amount', 'user_id')[0] #0为头部用户组，1为头部用户订单金额，2为头部用户数量
# 将结果写入mysql中
print('头部用户清单导入中......')
df_pareto.to_sql('headusers_total',engine,index=False,if_exists='replace')
print('完整头部用户导入完毕。')


# sql做帕累托
sql ='''
select b.`user_id`,b.`sum_amt` as `pay_amount`, b.`accum_amt`
from
(select a.*,
sum(a.`sum_amt`) over(order by a.`row_num`) as `accum_amt`
from
(select `user_id`,
sum(`pay_amount`) as `sum_amt`,
row_number() over (order by sum(`pay_amount`)  desc) as `row_num`
from
`ey`.`orders_2020`
where `order_status` in (1,2,3,5,8)
and `user_id` != 0
and year(`order_time`) in (2020,2018,2019)
group by `user_id`) a ) b
where b.`accum_amt` <=
(select sum(`pay_amount`)*0.8 as thres
from `ey`.`orders_2020`
where `order_status` in (1,2,3,5,8)
and year(`order_time`) in (2018,2019,2020)
and `user_id` != 0);
'''
df_pareto = pd.read_sql_query(sql,engine)


# 写入mysql数据库
print('完整头部用户导入中......')
df_pareto.to_sql('headusers_total',engine,index=False,if_exists='replace')
print('完整头部用户导入完毕。')
