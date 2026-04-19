'''一、元素周期表背诵小程序
    导入 元素周期表相关的字典信息
    用户规定练习xx-xx号元素
    用户选择根据名称回答原子序数还是根据原子序数回答名称 略
    判断机会有三次，三次都错误则显示正确答案        '''
'''待改进:1.添加难度分级：
                        简单模式:循环五次
                        中等模式：循环十次
                        困难模式：循环二十次
                        地狱模式: 循环三十次
        2.错题本功能：
                    记录答错的题目
                    提供针对性复习
        3.学习进度跟踪:
                    保存用户的学习记录
                    显示学习曲线和进步情况2
                    增设答题排行榜等
        4.待添加功能:根据名字 序号等说出周期或者主族
                    排列给定个数的原子半径/电负性等'''
import time
import random
import json
import re
def menu():
    print('===================================================================================================')
    print('------------------------------------元素周期表练习模式菜单------------------------------------------')
    print('--------------------------------1.根据原子序号说出中文元素名称---------------------------------------')
    print('--------------------------------2.根据中文元素名称说出原子序号---------------------------------------')
    print('--------------------------------3.根据原子序号说出元素缩写符号---------------------------------------')
    print('--------------------------------4.根据元素缩写符号说出原子序号---------------------------------------')
    print('--------------------------------5.根据元素缩写符号说出中文名称---------------------------------------')
    print('--------------------------------6.根据元素缩写符号说出所在位置---------------------------------------')
    print('--------------------------------7.根据元素符号来去比较原子半径---------------------------------------')
    print('--------------------------------8.根据元素的符号来去比较电负性---------------------------------------')
    print('--------------------------------0.退出元素周期表练习小程序项目---------------------------------------')
    print('===================================================================================================')
def main():
        with open('elements_info.json','r',encoding='UTF-8') as f:
            element_info=json.load(f)
        while True:
            #运行前数据提取
            menu()
            choice=get_user_choice()
            if choice==0:
               exit_judge=exit_confirm()
               if exit_judge==True:
                   print('感谢使用')
                   print('即将退出练习程序')
                   time.sleep(2)
                   break #要是确认退出就关闭小程序
               else:
                   print('即将返回功能菜单')
                   time.sleep(1)
                   continue #重回菜单
            num1,num2=get_practice_range() #用户选定的练习范围 将在此范围随机生成 这里规定了num1不为零
            element_chosen_list=element_info[num1-1:num2] #选定的指定元素
            #进入主程序
            if choice==1:
                generic_practice_quiz(element_chosen_list,'num2name','原子序号','中文名称','atomicNumber','nameCn',input_name_cn)
            elif choice==2:
                generic_practice_quiz(element_chosen_list,'name2num','中文名称','原子序号','nameCn','atomicNumber',input_atomicnum)
            elif choice==3:
                generic_practice_quiz(element_chosen_list,'num2symb','原子序号','英文缩写','atomicNumber','symbol',input_symbol)
            elif choice==4:
                generic_practice_quiz(element_chosen_list,'symb2num','英文缩写','原子序号','symbol','atomicNumber',input_atomicnum)
            elif choice==5:
                generic_practice_quiz(element_chosen_list,'symb2name','英文缩写','中文名称','symbol','nameCn',input_name_cn)
            elif choice==6:
                pass
            elif choice==7:
                generic_practice_compare(element_chosen_list,'symb2sortR','英文缩写','原子半径','symbol','atomicRadius',get_comparation_Radius)
            elif choice==8:
                pass
            elif choice==9:
                pass
def generic_practice_quiz(element_chosen_list,test_type,question_name,answer_name,question_key,answer_key,input_fun):
    '''参数解释 test_type:测试的类型
                question_name:转化前的中文名
                answer_name:转化后的中文名
                question_key:问题的键值
                answer_key:答案的键值
                input_fun:输入答案所用函数
                '''
    print(f'==================欢迎来到{test_type}测试======================')
    print('-------------------每个问题你有三次机会-----------------------')
    print('--------------------希望你能挑战成功哦-----------------------')
    print('===========================================================')
    while True:
        answer_times=0
        answer_wrong=0
        wrong_element=[] #用于储存答错的元素,结束时展示
        loop_times=get_user_times_quiz() #获取参与者选择的模式对应的答题个数
        start=time.time()  #获取进入该程序的时间戳
        while answer_times<loop_times:
            answer_times+=1  #记录参与答题的循环次数 用于计算正确率
            random_element=random.choice(element_chosen_list) #从给定范围的元素里随机选取一个
            print(f'随机元素的{question_name}为{random_element.get(f'{question_key}')}')
            print(f'请根据该元素{question_name}写出对应的{answer_name}')
            for i in range(1,4):
                answer=input_fun()
                if answer==random_element.get(answer_key):
                    print('恭喜你回答正确')
                    break
                else:
                    print(f'很遗憾本次回答错误,你还有{3-i}次机会')
                if 3-i==0: 
                    answer_wrong+=1
                    wrong_element.append(random_element) #储存答错元素的信息便于结束后展示
                    print(f'正确答案为:{random_element.get(answer_key)}')
                    print('不要放弃啊,继续加油奥力给,勤能补拙')
        print('恭喜你完成本次练习')
        end=time.time() #获取退出该程序的时间戳1
        time_last=end-start
        avg_time=time_last/answer_times
        correct_rate=(answer_times-answer_wrong)*100/answer_times
        print(f'本次练习共参与{answer_times}次,正确回答{answer_times-answer_wrong}次,正确率为:{correct_rate:.2f}%')
        print(f'总用时为:{time_last:.2f}s,平均每次用时为:{avg_time:.2f}s')
        if correct_rate!=100.00:
            print('答错的元素如下:')
            print(f'\t\t{question_name}\t{answer_name}')
            for element in wrong_element:
                print(f'\t\t   {element.get(question_key)}\t\t   {element.get(answer_key)}')
        return_menu=loop_judge()
        if return_menu==True:
            print('即将返回菜单栏')
            time.sleep(2)
            return
        else:
            print('即将重新进行该功能,请做好准备')
            time.sleep(1)
            continue
def generic_practice_compare(element_chosen_list,test_type,question_name,answer_name,question_key,answer_key,input_fun): #从已选范围的元素选择生成的随机元素个数 然后输入判断的比较
    '''参数解释 test_type:测试的类型
                question_name:转化前的中文名
                answer_name:转化后的中文名
                question_key:问题的键值
                answer_key:答案的键值
                input_fun:输入答案所用函数
                '''
    print(f'==================欢迎来到{test_type}测试======================')
    print('-------------------每个问题你有三次机会-----------------------')
    print('--------------------希望你能挑战成功哦-----------------------')
    print('===========================================================')
    answer_times=0
    answer_wrong=0
    duration_total_list=[]  #记录答题总持续的时间
    while True:
        answer_times+=1 #记录答题次数
        num2compare=get_user_num2compare(element_chosen_list)  #这里传入是要判断所选的元素范围会不会超过比较数目
        random_element_list=random.sample(element_chosen_list,k=num2compare)  #随机选取k个不重复元素
        random.shuffle(random_element_list)   #打乱一下次序 防止选取时的偶然性
        correct_sorted_raw=sorted(random_element_list,key=lambda x : x.get(answer_key)) #这里列表里的还是字典格式需转换
        correct_sorted_done=[x.get(question_key) for x in correct_sorted_raw] #这里完成转换变为question_name(元素缩写等)排序
        print('随机选取的元素为:',*[x.get(question_key) for x in random_element_list]) 
        print(f'请根据所给随机元素的{question_name}写出其{answer_name}从小到大的正确排序')
        start_single=time.time()  #记录开始答题时的时间(每次答题时间)
        for i in range(1,4):
            answer_list=input_fun(num2compare)
            if answer_list==correct_sorted_done:
                end_single=time.time()  #获取答题完毕的时间(每次答题时间)
                duration_single=end_single-start_single
                duration_total_list.append(duration_single)
                print('恭喜你回答正确')
                print(f'本次答题用时:{duration_single:.2f}s')
                break
            else:
                print(f'很遗憾本次回答错误,你还有{3-i}次机会')
            if 3-i==0: 
                answer_wrong+=1
                end_single=time.time()  #获取答题完毕的时间(每次答题时间)
                duration_single=end_single-start_single
                duration_total_list.append(duration_single)
                print('正确答案为:','<'.join(correct_sorted_done))
                print('不要放弃啊,继续加油奥力给,勤能补拙')
        return_menu=loop_judge()
        if return_menu==True:
            correct_rate=(answer_times-answer_wrong)*100/answer_times
            duration_total=sum(duration_total_list)
            avg_duration=duration_total/answer_times
            print('即将返回菜单栏')
            print(f'本次练习共参与{answer_times}次,正确回答{answer_times-answer_wrong}次,正确率为:{correct_rate:.2f}%')
            print(f'本次练习答题总持续时间为:{duration_total:.2f}s 平均每次答题时间为:{avg_duration:.2f}')
            for i in range(3,-1,-1):
                print(f'返回倒计时:{i}s',end="\r",flush=True)
                time.sleep(1)
            return
        else:
            print('即将重新进行该功能,请做好准备')
            time.sleep(1)
            continue
def get_practice_range():
    while True:
        try:
            num1=int(input('请输入所要练习的原子序数起始点(1-118):'))
            num2=int(input('请输入所要练习的原子序数终止点(1-118):'))
            if num1 > num2:
                print('第一次输入的数字要比第二次输入的小')
                print('即将重新输入')
                time.sleep(0.5)
                continue
            if num1<1:
                print('第一次输入的数字不能小于1哦')
                print('即将重新输入')
                time.sleep(0.5)
                continue
            if num2>118:
                print('原子序数不要大于118呀呀呀')
                print('即将重新输入')
                time.sleep(0.5)
                continue
            else: break #输入了满足条件的数字退出循环返回num1和num2
        except:
            print('请输入整数')
            print('即将重新输入')
            time.sleep(0.5)
            continue
    return num1,num2
def get_user_choice():
    while True:
        try:
            choice=int(input('请选择所要的训练模式:'))
            if choice not in range(0,9):
                print('请输入正确的数字范围')
                print('即将重新输入')
                time.sleep(1)
                continue
            else:
                break #退出确认数字输入的循环
        except:
            print('请输入整数')
            print('即将重新输入')
            time.sleep(1)
            continue
    return choice #返回用户输入的choice
def get_user_times_quiz():
    print('===============================================')
    print('-----------------模式选择菜单-------------------')
    print('---------------1.普通(5个问题)------------------')
    print('---------------2.中等(10个问题)-----------------')
    print('---------------3.困难(20个问题)-----------------')
    print('---------------4.地狱(30个问题)-----------------')
    print('---------------5.自定义个数[1,30]---------------')
    print('===============================================')
    while True:
        try:
            option=int(input('请输入你选择难度对应的序号:'))
            if option not in range(1,6):
                print('请输入正确范围的整数')
                print('即将重新输入')
                time.sleep(0.5)
                continue
            elif option==1:
                loop_times=5
                break
            elif option==2:
                loop_times=10
                break
            elif option==3:
                loop_times=20
                break
            elif option==4:
                loop_times=30
                break
            elif option==5:
                loop_times=num_times()
                break
        except:
            print('请输入整数')
            print('即将重新输入')
            time.sleep(0.5)
            continue
    return loop_times
def get_user_num2compare(element_chosen_list):
    print('===============================================')
    print('-----------------模式选择菜单-------------------')
    print('---------------1.普通(两个元素比较)--------------')
    print('---------------2.中等(三个元素比较)--------------')
    print('---------------3.困难(五个元素比较)--------------')
    print('===============================================')
    while True:
        try:
            option=int(input('请输入所要选择的模式对应的序号:'))
            if option not in range(1,4):
                print('请输入正确的整数')
                print('即将重新输入')
                time.sleep(0.5)
                continue
            elif option==1:
                num2compare=2  
                break
            elif option==2:
                if len(element_chosen_list)<3:
                    print('您选取的元素范围小于三个数目')
                    print('无法选择该模式,请重新选择')
                    time.sleep(1)
                    continue
                else:
                    num2compare=3
                break
            elif option==3:
                if len(element_chosen_list)<5:
                    print('您选取的元素范围小于五个数目')
                    print('无法选择该模式,请重新选择')
                    time.sleep(1)
                    continue
                num2compare=5
                break
        except:
            print('请输入正确的整数')
            print('即将重新输入')
            time.sleep(0.5)
            continue
    return num2compare
def num_times():
    while True:
        try:
            num=int(input('请输入自定义的问题个数:'))
            if num not in range(0,31):
                print('请输入正确范围内的数字')
                print('即将重新输入')
                time.sleep(0.5)
                continue
            else:
                break
        except:
            print('请输入整数')
            print('即将重新输入')
            time.sleep(0.5)
            continue
    return num
def get_comparation_Radius(num2compare):  #加个是否确定答案 不确定就改
    answer_list=[]
    print('请按原子半径从小到大依次输入对应的元素符号')
    for index in range(1,num2compare+1):  #这里是为了输入给定的元素数量
        while True:
            answer=input(f'请输入第{index}个元素缩写符号(从小到大):')
            if is_valid_symbol(answer):   #输入的为确定格式则结束循环
                answer_list.append(answer) #加上输入的元素
                break
            else:
                print('请输入正确的元素缩写格式(如He、Na)开头首字母大写其余小写')
                print('即将重新输入,不消耗答题次数')
                time.sleep(0.5)
                continue
    while True:
        print('你输入的答案为:',"<".join(answer_list))
        answer=input('请问是否还需要更改?(y/n):')
        if answer not in ("y",'Y','N','n'):
            print('请输入正确的指令')
            print('即将重新输入')
            time.sleep(0.5)
        elif answer.lower()=='y':
            answer_list=answer_change(num2compare,answer_list)
        else:
            break #退出循环
    return answer_list
def input_name_cn():
    while True:
        answer=input('请输入你的答案:')
        if is_valid_name_Cn(answer):
            break
        else:
            print('请输入正确的汉字格式')
            print('即将重新输入,不消耗答题次数')
            time.sleep(0.5)
            continue
    return answer
def input_atomicnum():
    while True:
        try:
            answer=int(input('请输入你的答案:'))
            break
        except:
            print('请输入整数')
            print('即将重新输入,不消耗答题次数')
            time.sleep(0.5)
            continue
    return answer
def input_symbol():
    while True:
        symbol=input('请输入你的答案:')
        if is_valid_symbol(symbol):
            break
        else:
            print('请输入正确的元素缩写格式(如He、Na)开头首字母大写其余小写')
            print('即将重新输入,不消耗答题次数')
            time.sleep(0.5)
            continue
    return symbol
def answer_change(num2compare:int,answer_list:list):
    while True:
        try:
            change_index=int(input('请输入您目前所要更改的元素对应的位次(如1,2,3):'))
            if change_index not in range(1,num2compare+1):
                print(f'输入的位次不在指定范围{[1,num2compare+1]}内,请重新输入')
                print('即将重新输入')
                time.sleep(0.5)
                continue
            else:
                break #得到所要的索引 退出循环
        except:
            print('请输入整数')
            print('即将重新输入')
            time.sleep(0.5)
            continue
    print(f'你所要更改的是第{change_index}位所对应的元素其元素符号为{answer_list[change_index-1]}')
    while True:
        answer_change=input('请输入您要更改的答案(元素符号):')
        if is_valid_symbol(answer_change):
            answer_list[change_index-1]=answer_change
            print('更改完成')
            break
        else:
            print('请输入正确的缩写符号格式')
            print('即将重新输入')
            time.sleep(0.5)
            continue
    return answer_list
def is_valid_name_Cn(name):
    # 只允许：纯中文（元素中文名，比如 氢、氦、锂、铀...）
    pattern = re.compile(r'^[\u4e00-\u9fa5]{1,2}$')
    return bool(pattern.fullmatch(name))
def is_valid_symbol(symbol):
    # ^[A-Z] 首字母大写
    # [a-z]* 后面全部小写字母
    # $ 从头到尾严格匹配
    pattern= re.compile(r'^[A-Z][a-z]*$')
    return bool(pattern.fullmatch(symbol))
def loop_judge():
    return_menu=False
    while True:
        option=input('请问还需要进行该功能的练习吗?(y/n):')
        if option not in ('y','Y','N','n'):
            print('请输入正确的指令')
            print('即将重新输入')
            time.sleep(1)
            continue
        if option.lower()=='y':
            return_menu=False
            break
        else:
            return_menu=True
            break
    return return_menu
def exit_confirm():
    exit_judge=False
    while True:
        answer=input('请问真的要退出练习程序吗?(y/n):')
        if answer not in ('y','Y','N','n'):
            print('请输入正确的指令')
            print('即将重新输入')
            time.sleep(1)
            continue
        elif answer.lower()=='y':
            exit_judge=True
            break
        else:
            exit_judge=False
            break
    return exit_judge
if __name__=="__main__":
    main()