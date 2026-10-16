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
units=int(input("enter the number of units used:"))
if units<=100:
    bill=units*1
elif units<=200:
    bill=100*1+(units-100)*2
else:
    bill=100*1+100*2+(units-200)*5
print("Electricity bill:",bill)