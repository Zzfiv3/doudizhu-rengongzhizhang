'''
发牌-斗地主

Author: dong
'''
import random

class doudizhu:
    #定义54张牌
    def __init__(self):
        self.a=[]
        for i in range(54):
            self.a.append(i)
    #洗牌
    def xipai(self):
        random.shuffle(self.a) #洗牌
        n = random.randint(1, 54)
        b = self.a[:n]  # 从n的位置切牌
        c = self.a[n:]
        self.a = b + c

        #发牌
    def fapai(self):
        self.user1=self.a[0:-3:3] #玩家1，获得牌的顺序为 0，3，6，9...
        self.user2=self.a[1:-3:3] #玩家2，获得牌的顺序为 1，4，7，10...
        self.user3=self.a[2:-3:3] #玩家3，获得牌的顺序为 2，5，8，11...
        self.dipai= self.a[-3:]    #底牌 ，顺序为51，52，53
    #抢地主
    def qiangdizhu(self):
        i=random.randint(1,3)#随机选择一个人当地主
        self.dizhu=i    #定义一个地主的实例
        if i == 1:
            self.user1+=self.dipai
        if i == 2:
            self.user2+=self.dipai
        if i == 3:
            self.user3+=self.dipai
    #码牌
    def mapai(self):
        self.user1.sort(reverse=True)   ##从小到大码牌
        self.user2.sort(reverse=True)
        self.user3.sort(reverse=True)
    #牌序和花色一一对应
    def yingshe(self):
        huase = [(0, '♦️3'), (1, '♣️3'), (2, '♥️3'), (3, '♠️3'),
                 (4, '♦️4'), (5, '♣️4'), (6, '♥️4'), (7, '♠️4'),
                 (8, '♦️5'), (9, '♣️5'), (10, '♥️5'), (11, '♠️5'),
                 (12, '♦️6'), (13, '♣️6'), (14, '♥️6'), (15, '♠️6'),
                 (16, '♦️7'), (17, '♣️7'), (18, '♥️7'), (19, '♠️7'),
                 (20, '♦️8'), (21, '♣️8'), (22, '♥️8'), (23, '♠️8'),
                 (24, '♦️9'), (25, '♣️9'), (26, '♥️9'), (27, '♠️9'),
                 (28, '♦️10'), (29, '♣️10'), (30, '♥️10'), (31, '♠️10'),
                 (32, '♦️J'), (33, '♣️J'), (34, '♥️J'), (35, '♠️J'),
                 (36, '♦️Q'), (37, '♣️Q'), (38, '♥️Q'), (39, '♠️Q'),
                 (40, '♦️K'), (41, '♣️K'), (42, '♥️K'), (43, '♠️K'),
                 (44, '♦️A'), (45, '♣️A'), (46, '♥️A'), (47, '♠️A'),
                 (48, '♦️2'), (49, '♣️2'), (50, '♥️2'), (51, '♠️2'),
                 (52, 'BlackJoker'), (53, 'RedJoker')]

        # huase = [(0, '️3'), (1, '️3'), (2, '3'), (3, '️3'),
        #          (4, '️4'), (5, '️4'), (6, '️4'), (7, '️4'),
        #          (8, '️5'), (9, '️5'), (10, '️5'), (11, '5'),
        #          (12, '️6'), (13, '️6'), (14, '️6'), (15, '️6'),
        #          (16, '️7'), (17, '️7'), (18, '️7'), (19, '️7'),
        #          (20, '️8'), (21, '️8'), (22, '️8'), (23, '️8'),
        #          (24, '️9'), (25, '️9'), (26, '️9'), (27, '9'),
        #          (28, '️10'), (29, '️10'), (30, '️10'), (31, '️10'),
        #          (32, '️J'), (33, 'J'), (34, 'J'), (35, '️J'),
        #          (36, '️Q'), (37, '️Q'), (38, '️Q'), (39, '️Q'),
        #          (40, '️K'), (41, '️K'), (42, '️K'), (43, '️K'),
        #          (44, '️A'), (45, '️A'), (46, '️A'), (47, '️A'),
        #          (48, '️2'), (49, '️2'), (50, '️2'), (51, '️2'),
        #          (52, 'BlackJoker'), (53, 'RedJoker')]   #没有花色版
        zdpai = dict(huase)
        user1Card=''
        for i in range(len(self.user1)):
            user1Card+=zdpai[self.user1[i]]+' ' #以字符串的形式将牌储存起来
        user2Card = ''
        for i in range(len(self.user2)):
            user2Card += zdpai[self.user2[i]] + ' '
        user3Card = ''
        for i in range(len(self.user3)):
            user3Card += zdpai[self.user3[i]] + ' '
        diPai = ''
        for i in range(len(self.dipai)):
            diPai += zdpai[self.dipai[i]] + ' '

        self.user1 = user1Card  #把花色对应好的牌的序列重新赋给三个玩家的实例属性
        self.user2 = user2Card
        self.user3 = user3Card
        self.dipai = diPai


if __name__ == '__main__':
    Player=doudizhu() #将类辅助给playes,方便调用
    Player.xipai()
    Player.fapai()
    Player.qiangdizhu()
    Player.mapai()
    Player.yingshe()

print('本局地主是：玩家{}'.format(Player.dizhu))
print('底牌：', Player.dipai)
print('玩家一：',Player.user1)
print('玩家二：',Player.user2)
print('玩家三：',Player.user3)
