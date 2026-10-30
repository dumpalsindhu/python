# lst=[0]*10
# print(lst)
# lst1=[1,2,3]*5
# print(lst1)

# lst1=[10,20,30]
# lst2=[40,50,60]
# lst3=lst1+lst2
# print(lst1)
# print(lst2)
# print(lst3)

#slicing
# lst=[10,20,30,40,50,60,70]
# print(lst[0])
# print(lst[::])
# print(lst[1:5])
# print(lst[::2])

# lst=[10,20,30,40,50,60,70]
# print(lst[-2:-5:])
# print(lst[-2:-5:-1])
# print(lst[::-1])

#maximum
profits=[200,450,300]
max_profits=profits[0]
for p in profits:
    if p>max_profits:
        max_profits=p
print("highest profit:",max_profits)
