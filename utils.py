
def findprepost(lst,obj):

    for i in range(len(lst)):
        if lst[i] == obj:
            return i-1, i+1