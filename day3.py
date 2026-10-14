 # program 1
# Rama_height=1.3
# Raja_height=1.7
# if Rama_height>Raja_height:
#     print("Rama is taller")
# else:
#     print("Raja is taller")

#program 2
total=float(input("enetr total purchase amount:"))
if total>=1000:
    discount=total*0.10
    final_amount=total-discount
    print("discount applied:",discount)
    print("finala_amount to pay:",final_amount)
else:
    print("no discount applied")
    print("total amount:",total)
