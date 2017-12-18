#DEMO
import json
import  magic_box as mb 
#加载json数据
data_o=open("/home/ubuntu/Magic_Box/data_str.json",'r')
data_str=data_o.read()

#先将数据转化成mb可以进行处理的二维数组（必须是Array格式的）
data_obj=mb.Data(data_str)
#转化
#data_dic=data_obj.json2dic()
data_table,index_user,index_content=data_obj.json2table()
#实例化主对象
new_mb=mb.main(index_user,index_content,data_table)
#建立用户空间地图
new_mb.build_user_map()
#建立实例化池
new_mb.product_pool()
#预测，以小黑为例
json_str_sim='{"wujintao":[12,23,13,56,34,67,23,78]}'



sim_data_obj=mb.Data(json_str_sim)
sim_table,index_user,index_content=sim_data_obj.json2table()
sim_result=new_mb.sim(sim_table,index_content,flag=3,alphe=0.3,index_id="wujintao")
print("the result=:\n",sim_result)
