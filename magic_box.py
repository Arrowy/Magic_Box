import numpy as np 
from numpy import linalg as lg 
import json
#set up the uers Class
#part 1
np.set_printoptions(suppress=True)



class group(object):
	"""data==2dlist;index_c=session;index_r=users"""
	def __init__(self, data,index_c,index_r):
		self.index_c=index_c
		self.index_r=index_r
		self.matrix_A=np.matrix(data)
	def set_up_users_map(self):
		matrix_A=self.matrix_A
		U,sigma,V_transpose=lg.svd(matrix_A)
		#print(V_transpose)
		#print(self.matrix_A)
		V=np.matrix(V_transpose).T
		U=np.matrix(U) 
		#print(sigma)

		sum_sigma=0
		count=0
		#to cal the sum of the sigma,I create a [d_im_of_sigma,1] and muti it with the matrix_A
		
		total=np.sum(sigma)
		ratio_of_sum_sigma=0

		while ratio_of_sum_sigma<0.8:
			
			sum_sigma=sum_sigma+sigma[count]
			ratio_of_sum_sigma=sum_sigma/total
			count=count+1
		shape_of_users_map=[V.shape[0],count]#reduced V matrix
		reduced_U_matrix=U[:,:count]
		reduced_sigma_matrix=sigma[:count]
		matrix_user_map=V[:,:count]
		#print(V)
		#print(U)
		reduced_sigma_diag=np.matrix(np.diag(reduced_sigma_matrix))
		#print(reduced_sigma_diag)
		'''print("the count=",count)
		print("the u  ",reduced_U_matrix)
		print("the sigma  ",reduced_sigma_matrix)
		print("the sigma original=",sigma)
		print("the v  ",self.matrix_user_map)'''
		
		#print(self.matrix_user_map)
		return matrix_user_map,reduced_U_matrix,reduced_sigma_diag
	


class user(group):
	"""content_vector must be """
	def __init__(self,index_r,content_vector,index_id):
		
		self.vector =np.matrix(np.atleast_2d(content_vector))
		self.index_base=[]
		self.index_users=index_r
		self.index_id=index_id
		
	def pearson(self,matrix_user_map,reduced_U_matrix,reduced_sigma_matrix):
		location=self.vector*reduced_U_matrix*reduced_sigma_matrix.I
		#print(location)
		'''print(self.vector.T)
		print(reduced_U_matrix)
		print(reduced_sigma_matrix)'''

		pool=np.r_[location,matrix_user_map]
		#print(matrix_user_map)
		#print(pool)
		#print(pool.shape)
		#print(np.corrcoef(np.matrix(pool)))
		#print(np.corrcoef(pool))
		pearson_value=np.corrcoef(pool)[0,:]
		print("pearson=",np.corrcoef(pool))#a 2d matrix and the first line is the value we need
		#seek the index of the familiar users
		#print(pearson_value)
		
		for i in range(len(pearson_value)):
			if i !=0 and pearson_value[i]>=0.7:
				self.index_base.append(self.index_users[i-1])
		return self.index_base
	def tag_balance(self,flag):#将用于冷启动匹配的非内容相关的指标去掉，只留下和
		#stasistic the amount of every tag
		vector=self.vector
		
		#print(vector)

		
		vector[0,:flag]=np.zeros(flag)#这里矩阵的规模是没有发生变化的，只是内容不相关的部分变成了
		#print(vector)
		return vector#这里输出的是一个矩阵

#main API
class Data(object):
	"""process data into differet term dic2json/json2dic/dic2np.atleast2d"""
	def __init__(self, data):
		self.data = data
		self.index_r=[]
		self.index_c=[]
	def json2dic(self):
		data=json.loads(self.data)
		return data
	def json2table(self):
		data_dic=json.loads(self.data)
		print(self.data)
		#print(data_dic)
		for key,value in data_dic.items():
			self.index_r.append(key)
		#print(self.index_r)
		
		for i in range(len(data_dic[self.index_r[0]])):
			self.index_c.append(i)
		data_table=np.zeros((len(self.index_c),len(self.index_r)))
		for i in range(len(self.index_r)):
			data_table[:,i]=data_dic[self.index_r[i]]
		return data_table,self.index_r,self.index_c
	def table2json(self):
		result_dic={}
		for vec in range(self.data_table.shape[1]):
			result_dic[self.index_r[vec]]=list(self.data_table[:,vec])
		result_json=json.dumps(result_dic)
		return result_json
						


class main(object):
	
	def __init__(self, index_r,index_c,data,dtype="json"):
		
		self.index_r = index_r
		self.index_c=index_c
		self.data=data
		self.pool=[]
		self.uers_map=[]
		self.reduced_U_matrix=0
		self.reduced_sigma_matrix=0
	def build_user_map(self):
		user_group=group(self.data,self.index_c,self.index_r)
		self.uers_map,self.reduced_U_matrix,self.reduced_sigma_matrix=user_group.set_up_users_map()
	def product_pool(self):
		#put the all product into the pool
		data=self.data
		index_r=self.index_r
		new_pool=[]
		#read out the all user's name 
		for index_i in range(data.shape[1]):
			every_vector=data[:,index_i].T
			new_pool.append(user(index_r,every_vector,index_id=self.index_r[index_i]))#所有的用户都被实例化为user对象，拥有Pearson和index方法
		self.pool=new_pool
	def sim(self,new_user,index_c,flag,alphe,index_id):
		#先将这个进来的用户给实例化,flag代表前多少个内容指标是内容不相关的
		new_user=user(self.index_r,new_user.T,index_id)
		index_of_familiar=new_user.pearson(self.uers_map,self.reduced_U_matrix,self.reduced_sigma_matrix)
		result_of_familiar=np.matrix(np.zeros((1,len(index_c))))
		
		for count in self.pool:
			'''print(count.index_id)
			print(index_of_familiar)
			break'''
			if count.index_id in index_of_familiar:
				result_of_familiar+=count.tag_balance(flag)
		#print("pool=",self.pool)
		#print("index_of_familiar=",index_of_familiar)
		result=(alphe*new_user.tag_balance(flag))+((1-alphe)*result_of_familiar)
		return result







		