def cbin(dec:int) ->list:
    a=[]
    while dec>0:
        x=dec%2
        y=dec//2
        a.append(x)
        print(f"{dec}:2=    {y}R{x}")
        dec=y
    
    a.reverse()
    return a

#a)

def dreieck(num:int):
    for x in range(num):
        for y in range(x+1):
            print(y+1,end="")
        print()
#b)
def dreieckr(num:int,char:str="."):
    for x in range(num,0,-1):
        print(char*(num-x),end="")
        print(x)
#c)

def rlist(l:list)->list:
    x=len(l)
    for i in range(int(x/2)):
        b=x-i-1
        #print(i,b)
        w=l[i]
        r=l[b]
        l[i]=r
        l[b]=w
        
    return l

def c(input:str)->list:
    a=[]
    for x in input:
        if not x.isnumeric():
            #print(x)
            if x.lower()=="p":
                print("".join(a))
            elif x.lower()=="u":
                a=rlist(a)
        else:
            a.append(x)
    
if __name__== '__main__':
    #print(cbin(100))
    #dreieckr(5)
    
    c("12pup3p")
