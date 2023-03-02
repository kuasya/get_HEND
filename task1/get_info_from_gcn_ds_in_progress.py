from bs4 import BeautifulSoup
import requests
import re
from astropy.table import Table


def write_tab(lst_data):
    # b_name, starttime, starttimeUT, duration, fluence, peak_fl_res, peak_fl, mode, redshift
    lst_names = "GCN Name Time TimeHHMMSS Duration Fluence PFscale PF Mode Z(Redshift)".split()
  
    tab = Table(rows=lst_data, names=lst_names)
    tab.write('Burst_info.txt', format='ascii.fixed_width', delimiter='', overwrite=True)

def parce_line(string):

    string = string.replace('\n', ' ')

    m = re.search('(GRB\s*\d{6}\w |GRB\s*\d{6} |SGR\s*\d+.\d+ |SGR\d+.\d+ |\d+\s*\SGR)', string)
    if not m is None:
        b_name = m.group(1).replace(' ', '')
    else:
        b_name = '--'
    print(b_name)

    if re.search('SGR', b_name):
        print("SGR burst - skipping")
        return None

    m = re.search('in\s+the\s+waiting\s+mode', string)
    if m:
        print("Waiting mode - skipping")
        return None

    m = re.search('(T0\s*=\s*(\d+\.\d+) | starting at\s*(\d+)\s* | T0....\s*=\s*(\d+) | T0.....\s*=\s*(\d+)'
                   '| T0\s*=\s*(\d+) | at\s*(\d+\.\d+)\s* | T0....\s*=\s*(\d+\.\d+)'
                   '| T0\s*=\s*(\d+\.\d+) | \(T0....\s*=\s*(\d+\.\d+) | T0\s*=\s*(\d+\.\d+)\w)', string)

    if not m is None:
        starttime = m.group().replace('T0=', '').replace(' at ', '').replace(' ', '').replace('T0(KW)=', '').replace('(', '').replace('s', '')
    else:
        starttime = '--'
    print(starttime)

    m = re.search('in\s+the\s+waiting\s+mode', string)
    if m:
        print("Waiting mode - skipping")
        return None

    m = re.search('(UT..(\d{2}:\d{2}:\d{2}.\d+)|T0.........(\d{2}:\d{2}:\d{2})|T0......(\d{2}:\d{2}:\d{2})'
                  '|UT..(\d{2}:\d{2}:\d{2})|T0.......(\d{2}:\d{2}:\d{2}.\d+)'
                  '|T0.......(\d{2}:\d{2}:\d{2})|(UT...(\d{2}:\d{2}:\d{2}.\d+))'
                  '|(\d..(\d{2}:\d{2}:\d{2}.\d+))|at.(\d{2}:\d{2}:\d{2}.\d+))', string)

    if not m is None:
        starttimeUT = m.group().replace('T0=T0(BAT)=','').replace('UT (','').replace('T0(BAT)= ','').replace('T0(BAT)=','').replace('T0(MAXI)=','').replace('UT  (','').replace('5 (','').replace('at ','')
    else:
        starttimeUT = '--'
    print(starttimeUT)

    m = re.search('((duration\s+(?:of|is)\s*~\s*(\d+(?:\.\d+)?)\s*(s|ms))|(duration of the burst is\s*.(\d+\.\d+)\s*(s|ms))'
                  '|(duration of the burst is\s*.(\d+)\s*(s|ms))|(duration of\s*(\d+\.\d+)\s*(s|ms))'
                  '|(duration of\s*.(\d+)\s*(s|ms))|(burst\s......\s\w\w\s*.(\d+)\s*(s|ms))|(duration\s*.(\d+)\s*(s|ms))'
                  '|(duration\s......\s\w{2}\s*.(\d+)\s*(s|ms))|(of\s\w{5}\s*.(\d+)\s*(s|ms))'
                  '|(\d{4}\s\w{3}.\s\w\w\s*.(\d+\.\d+)\s*(s|ms))|(duration\s\w{2}\s\w{5}\s(\d+\.\d+)\s*(s|ms))'
                  '|(duration\s\w{2}\s\w{5}\s.(\d+\.\d+)\s*(s|ms))|(duration\s\w{2}\s\w{3}\s\w{5}.\s\w{2}\s*.(\d+)\s*(s|ms))'
                  '|(duration\s\w{2}\s\w{5}\s(\d+)\s*(s|ms))|(\d{4}\s\w{3}.\s\w\w\s*.(\d+)\s*(s|ms))'
                  '|(duration\s\w{2}\s\w{3}\s\w{5}\s\w{2}\s\w{2}\s*.(\d+\.\d+)\s*(s|ms))|(about\s*.(\d+)\s*(s|ms))'
                  '|(duration\s\w{2}\s\w{3}\s\w{5}\s\w{2}\s*.(\d+)\s*.(s|ms))|(duration\s\w{2}\s\w{3}\s\w{5}\s*.(\d+)\s*.(s|ms))'
                  '|(\d{3}\s\w{3}.\s\w\w\s*.(\d+)\s*(s|ms))|(duration\s.(\d+\.\d+)\s*(s|ms)))', string)


    #https://gcn.gsfc.nasa.gov/gcn3/19604.gcn3 - two durations

    if not m is None:
        duration = m.group(1).replace('duration of ~', '').replace('duration of the burst is ~', '').replace('duration of~', '').replace('duration is ~', '').replace('duration  of ~', '').replace(' ', '').replace('burst(T100)is~', '').replace('duration(T100)of~', '').replace('durationof', '').replace('ofabout', '').replace('`', '').replace('1300keV)is~', '').replace('360keV)is~', '').replace('1400keV)of~', '').replace('theburstis~', '').replace('durationisabout', '').replace('duration~', '').replace('about', '').replace('theburstinis~', '').replace('~', '').replace('theburstof', '').replace('theburst', '')

    else:
        duration = '--'
    print(duration)

    m = re.search('(fluence\s+of\s+(.+?)\s*erg|\d{4}\s\w{3}\s\w{4}\s\w{2}\s+(..................)'
                  '|fluence\s\w{2}\s+(.......)\s+erg/cm2'
                  '|fluence\s(...................)\s+erg/cm2)', string)
    m2 = re.search('(interval\s\w{2}\s+(...................)|fluence\s+(.+?)\s*erg)', string)

    if not m is None:
        fluence = m.group().replace('1500 keV band is ', '').replace('fluence of ', '').replace(' erg', '').replace(
            'interval is ', '').replace(' e', '').replace('fluence ', '').replace('this part is ', '')\
            .replace('is ', '').replace('the most intense part of the burst ', '').replace(' ', '').replace('~', '')\
            .replace('theburstsapproximately', '').replace('/cm2', '').replace('of', '')
    elif not m2 is None:
        fluence = m2.group().replace('1500 keV band is ', '').replace('fluence of ', '').replace(' erg', '').replace(
            'interval is ', '').replace(' e', '').replace('fluence ', '').replace('this part is ', '')\
            .replace('is ', '').replace('the most intense part of the burst ', '').replace(' ', '').replace('~', '')\
            .replace('theburstsapproximately', '').replace('/cm2', '')
    else:
        fluence = '--'

    print(fluence.strip())

    #https://gcn.gsfc.nasa.gov/gcn3/5748.gcn3 - 'fluence of this part is', two fluences
    #https://gcn.gsfc.nasa.gov/gcn3/5689.gcn3 - 'fluence of this part is', two fluences

    peak_fl_res = re.search(('\d{1}.\d{1,4}-s|\d{1,4}-ms|measured\s\w\w\s\w\s\d{1}.\d{1,3}|cm2\s\w{3}\s\w\s\d{1}.\d{1,3}'
                         '|followed\s\w{2}\s.\d{1,3}|and\s\w\s\d{1,3}-s|started\s\w{2}\s\d{1,3}|over\s\d{1}.\d{1,3}'
                         '|\d{1,3}\smsec'), string)

    if peak_fl_res != None:
        peak_fl_res = peak_fl_res.group()
        if peak_fl_res.find('-ms') != -1:
            peak_fl_res = float(peak_fl_res.replace('-ms', '')) / 1000
            peak_fl_res = str(peak_fl_res)
        if peak_fl_res.find('msec') != -1:
            peak_fl_res = float(peak_fl_res.replace('msec', '')) / 1000
            peak_fl_res = str(peak_fl_res)
        peak_fl_res = peak_fl_res.replace('-ms', '').replace('-s', '').replace('measured on a ', '').replace('cm2 and a ',
                                                                                                     '').replace(
            'followed in ~', '').replace('and a ', '').replace('started at ', '').replace('over ', '')
    else:
        peak_fl_res = '--'
        print(peak_fl_res)

    #https://gcn.gsfc.nasa.gov/gcn3/4394.gcn3 - 15-ms or 4-ms?
    #https://gcn.gsfc.nasa.gov/gcn3/3179.gcn3 - don`t understand peak flux


    m = re.search(('\s*s,\s*of\s*(.+?)\s*erg|\s*,\s*of\s*(.+?)\s*erg'
                   '|\d{2}\.\d{3}\s\w\s\w{2}\s(.+?)\s*erg/cm2/s,'
                   '|\w{8}\s\w{4}\s...\d+\.\d+\s\w\s\w{2}\s(.+?)\s*erg/cm2'), string)

    if m is None:
        peak_fl = '--'
    else:
        peak_fl = m.group().replace(' s, of ','').replace(' erg','').replace(', of ','').replace('s','').replace('63.107  i','').replace('/cm2/,','').replace(' ','').replace('/cm2','').replace('meauredfromT0+18.752of','').replace('meauredfromT0+8.640of','').replace('meauredfromT0+2.048of','').replace('meauredfromT0+3.536of','').replace('meauredfromT0+4.304of','').replace('meauredfromT0+1.296of','').replace(' erg/cm2','').replace('meauredfromT0+18.128of','').replace('meauredfromT0-0.320of','').replace('meauredfromT0+211.6of','')

        print(peak_fl)

    m = re.search('triggered|waiting\s*mode', string)
    if not m is None:
        mode = m.group(0).replace(' ', '')
    else:
        mode = '--'
    print(mode)

    #https://gcn.gsfc.nasa.gov/gcn3/8611.gcn3 - 'trigger record'?

    m = re.search(r'z\s*=\s*(\d+(?:\.\d+)?)', string)
    if m is None:
        redshift = '--'
    else:
        redshift = m.group(1)
        
    print(redshift)
 
    return [b_name, starttime, starttimeUT, duration, fluence, peak_fl_res, peak_fl, mode, redshift]

def main():

    with open("links.txt") as f:
        lines = f.read().split('\n') 
    
    lst_data = []
    for line in lines:
        line = line.strip()
        print(line)
        str_gcn = line[-10:-5]
        response = requests.get(line)
        soup = BeautifulSoup(response.content, "lxml")
        ptag = soup.find(lambda tag: tag.name == 'p')
    
        string = str(ptag)

        res = parce_line(string)
        if not res is None:
            lst_data.append([str_gcn,] + res)
    
    write_tab(lst_data)

main()