def type_eval(string):
    """return the value of string (if it isn't in it's supported types it will raise exception) for example: type_eval('["aaa",10,10.0,(10,1)]')=["aaa",10,10.0,(10,1)]
    supported types: list,tuple,string,int,float,boolean"""
    return type_eval_recurtion(string.replace(" ",""))

def type_eval_recurtion(string):
    """return the value of string (if it isn't in it's supported types it will raise exception) for example: type_eval('["aaa",10,10.0,(10,1)]')=["aaa",10,10.0,(10,1)]
    supported types: list,tuple,string,int,float,boolean
    NOTE: assume that there is no space in the string"""
    if len(string)==0:
        raise Exception("type_eval: string can't be ''")
    elif (string[0]=="[" and string[-1]=="]") or (string[0]=="(" and string[-1]==")"):
        #list or tuple
        ans= split_no_bracket(string[1:-1])
        for i in range(len(ans)):
            ans[i]= type_eval_recurtion(ans[i])
            
        if string[0]=="(":
            ans= tuple(ans)
    elif len(string)>1 and ((string[0]=="'" and string[-1]=="'") or (string[0]=='"' and string[-1]=='"')):
        #string
        ans= string[1:-1]
    elif string in ["True","False"]:
        return string=="True"
    elif consist_of(string[1:],"1234567890.") and (string[0] in "1234567890-"):
        #float or int
        dot_num= string.count(".")
        if dot_num==0:
            ans= int(string)
        elif dot_num==1:
            ans= float(string)
        else:
            raise Exception("type_eval: consist of nums and dots but to much dots for tuple")
    elif string.count("e")==1:
        #it can be float from the from (a)e(b) for example 1.5e-10
        parts= string.split("e")
        try:
            parts= [type_eval_recurtion(parts[0]),type_eval_recurtion(parts[1])]
            if type(parts[1])!=int:
                raise Exception()
            ans= parts[0]*(10**parts[1])
        except:
            print("string:",string)
            raise Exception("type_eval: undefint type")
    else:
        print("string:",string)
        raise Exception("type_eval: undefint type")
    return ans
        

def consist_of(string1,string2):
    """check does string1 consist of characters in string2"""
    for c in string1:
        if not c in string2:
            return False
    return True

def split_no_bracket(string):
    """split the string according to "," when ignoryng the "," that in any type of brakets (including (),[],{})"""
    ans=[]
    slice_start=0
    open_brackets= "([{"
    close_brackets= ")]}"
    brackets_level= [0,0,0,0,0]
    #brackets_level[0]- () level
    #brackets_level[1]- [] level
    #brackets_level[2]- {} level
    #brackets_level[3]- "" level
    #brackets_level[4]- '' level
    for i in range(len(string)):
        if string[i]=="," and sum(brackets_level)==0:
            #print(i)
            ans.append(string[slice_start:i])
            slice_start= i+1
        elif open_brackets.find(string[i])!=-1:
            brackets_level[open_brackets.find(string[i])]+=1
        elif close_brackets.find(string[i])!=-1:
            brackets_level[close_brackets.find(string[i])]-=1
        elif "\"'".find(string[i])!=-1:
            brackets_level["\"'".find(string[i])+3]+=1
            brackets_level["\"'".find(string[i])+3]%=2
            

        if brackets_level[0]<0 or brackets_level[1]<0 or brackets_level[2]<0:
            raise Exception("split_no_bracket: to much closing brakets in: "+string)

    if sum(brackets_level)!=0:
            raise Exception("split_no_bracket: to much opening brakets in: "+string)

    ans.append(string[slice_start:])
    return ans
