# weight=float(input("enter the weight:"))
# height=float(input("enter the height:"))
# BMI=weight/(height**2)
# if BMI <=18.5:
#     print("under weight")
# elif BMI<=25:
#     print("normal")
# elif BMI<=30:
#     print("overweight")
# else:
#     print("obse")

#     electricity bill
# units=int(input("enter the number of units used:"))
# if units<=100:
#     bill=units*1
# elif units<=200:
#     bill=100*1+(units-100)*2
# else:
#     bill=100*1+100*2+(units-200)*5
# print("Electricity bill:",bill)

# trinagles
# a=int(input("enter the first angle:"))
# b=int(input("enter the second angle:"))
# c=int(input("enter the third angle:"))
# if a == b and b == c and c == a:
#     print("equilateral triangle")
# elif a == b or b == c or c == a:
#     print("isosceles triangle")
# else:
#     print("scalen triangle")
age=int(input("enter the age:"))
if age>=18:
    print("allowed for match")
    if age>=18 and age<30:
        print("2$ ticket price")
    elif age>=30 and age<60:
        print("1$ ticket price")
    else:
        print("0$ ticket price")
else:
    print("not alloewd for match")
