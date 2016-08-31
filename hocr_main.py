__author__ = 'Michael'

work='C:\\Users\\Michael\\Projects\\HOCR\\2016'
import os

results = os.path.join(work,'2014-raw-results.txt')
output_file = os.path.join(work,'2014-results-tabd.txt')

def main():
    rf = open(results,'r')
    of = open(output_file,'w')
    ct=0
    eventflag=False
    boatflag=False
    evtdesc=''
    evtid=''
    boatheaders = ('Event ID','Event Description','Event Day','Place','Lane','Club Name','Boat','Description','Status','Raw Time','Raw Delta','Raw Pct','Handicap','Penalty','Penalty Codes','Adj Time','Adj Delta','Adj Pct')
    numfields = 18
    line='\t'.join(['%s']*numfields) + '\n'

    of.write(line % boatheaders)

    for i in rf:
        if eventflag == True:
            a=i.strip().split('\t')
            print a
            evtid=a[0]
            evtdesc=a[1]
            evtday=a[4]
            # break
        if boatflag==True:
            a=i.strip().split('\t')
            # print a
            a.insert(0,evtday)
            a.insert(0,evtdesc)
            a.insert(0,evtid)
            # print len(line.strip().split('\t'))
            # print len(a[0:numfields])
            if len(a)<numfields:
                for j in range(numfields-len(a)):
                    a.append('')
            of.write(line % tuple(a[0:numfields]))
            # print tuple(a)
            ct+=1
            # if ct>5:
            #     break
        if i.strip()=='Hide':
            eventflag=True
            boatflag=False
        elif i.strip()=='Show':
            boatflag=True
            eventflag=False
        else:
            eventflag=False
            boatflag=False
        a=None

    of.close()
    rf.close()
    print ct

if __name__=='__main__':
    main()