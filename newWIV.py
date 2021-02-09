import glob
import pprint

folderList = glob.glob('D:/data/*')
#pprint.pprint(test)

for test in folderList:
    splited = test.split('\\')[-1]
    #print(splited)
    tmp = test + '/*.dat'
    pprint.pprint(tmp)
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    print('Changed!!')                                   
