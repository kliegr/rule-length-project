def generateText(column):
    return column.replace([" => {Label=","}$","{","}",",","=1.0"],["then the risk of traffic accidents is <b>","</b>" ,"if the country falls into all of the following group(s) (simultaneously) <ul><li>", "&nbsp;</li></ul>", "&nbsp;<b>and</b> </li><li>",""], regex=True)
