mylist = ["English", "Arabic", "Computer","Web","Erp","Apps"]
print(mylist)
sub=input("Enter subjects you don’t like.")
sub=sub.capitalize()
if sub in mylist:mylist.remove(sub)
else:print("Not in list")
print(mylist)