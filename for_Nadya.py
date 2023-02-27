from bs4 import BeautifulSoup
import requests
import re
from astropy.table import Table


def write_tab(lst_data):
    # b_name, starttime, starttime_ut, duration, fluence, err_fl, pf_ti, peak_fl_res, peak_fl, err_pf, ep, err_ep,
    # mode, redshift
    lst_names = "GCN Name Time TimeHHMMSS Duration Fluence Err_Fluence(-) Err_Fluence(+) PFti PFscale PF Err_PF(-) " \
                "Err_PF(+) Ep Err_Ep(-) Err_Ep(+) Mode Z(Redshift)".split()

    tab = Table(rows=lst_data, names=lst_names)
    tab.write('Burst_info2.txt', format='ascii.fixed_width', delimiter='', overwrite=True)


def parce_line(string):
    string = string.replace('\n', ' ')
    string = string.replace('�', '±')

    m = re.search(r'(GRB\s*\d{6}\w |GRB\s*\d{6} |SGR\s*\d+.\d+ |SGR\d+.\d+ |\d+\s*\SGR)', string)
    if m is not None:
        b_name = m.group(1).replace(' ', '')
    else:
        b_name = '--'
    print(b_name)

    if re.search('SGR', b_name):
        print("SGR burst - skipping")
        return None

    m = re.search(r'in\s+the\s+waiting\s+mode', string)
    if m:
        print("Waiting mode - skipping")
        return None

    m = re.search(r'(T0\s*=\s*(\d+\.\d+) | starting at\s*(\d+)\s* | T0....\s*=\s*(\d+) | T0.....\s*=\s*(\d+)'
                  r'| T0\s*=\s*(\d+) | at\s*(\d+\.\d+)\s* | T0....\s*=\s*(\d+\.\d+)'
                  r'| T0\s*=\s*(\d+\.\d+) | \(T0....\s*=\s*(\d+\.\d+) | T0\s*=\s*(\d+\.\d+)\w)', string)

    if m is not None:
        starttime = m.group().replace('T0=', '').replace(' at ', '').replace(' ', '').replace('T0(KW)=', '').replace(
            '(', '').replace('s', '')
    else:
        starttime = '--'
    print(starttime)

    m = re.search(r'in\s+the\s+waiting\s+mode', string)
    if m:
        print("Waiting mode - skipping")
        return None

    m = re.search(r'(UT..(\d{2}:\d{2}:\d{2}.\d+)|T0.........(\d{2}:\d{2}:\d{2})|T0......(\d{2}:\d{2}:\d{2})'
                  r'|UT..(\d{2}:\d{2}:\d{2})|T0.......(\d{2}:\d{2}:\d{2}.\d+)'
                  r'|T0.......(\d{2}:\d{2}:\d{2})|(UT...(\d{2}:\d{2}:\d{2}.\d+))'
                  r'|(\d..(\d{2}:\d{2}:\d{2}.\d+))|at.(\d{2}:\d{2}:\d{2}.\d+))', string)

    if m is not None:
        starttime_ut = m.group().replace('T0=T0(BAT)=', '').replace('UT (', '').replace('T0(BAT)= ', '').replace(
            'T0(BAT)=', '').replace('T0(MAXI)=', '').replace('UT  (', '').replace('5 (', '').replace('at ', '')
    else:
        starttime_ut = '--'
    print(starttime_ut)

    m = re.search(
        r'((duration\s+(?:of|is)\s*~\s*(\d+(?:\.\d+)?)\s*(s|ms))|(duration of the burst is\s*.(\d+\.\d+)\s*(s|ms))'
        r'|(duration of the burst is\s*.(\d+)\s*(s|ms))|(duration of\s*(\d+\.\d+)\s*(s|ms))'
        r'|(duration of\s*.(\d+)\s*(s|ms))|(burst\s......\s\w\w\s*.(\d+)\s*(s|ms))|(duration\s*.(\d+)\s*(s|ms))'
        r'|(duration\s......\s\w{2}\s*.(\d+)\s*(s|ms))|(of\s\w{5}\s*.(\d+)\s*(s|ms))'
        r'|(\d{4}\s\w{3}.\s\w\w\s*.(\d+\.\d+)\s*(s|ms))|(duration\s\w{2}\s\w{5}\s(\d+\.\d+)\s*(s|ms))'
        r'|(duration\s\w{2}\s\w{5}\s.(\d+\.\d+)\s*(s|ms))|(duration\s\w{2}\s\w{3}\s\w{5}.\s\w{2}\s*.(\d+)\s*(s|ms))'
        r'|(duration\s\w{2}\s\w{5}\s(\d+)\s*(s|ms))|(\d{4}\s\w{3}.\s\w\w\s*.(\d+)\s*(s|ms))'
        r'|(duration\s\w{2}\s\w{3}\s\w{5}\s\w{2}\s\w{2}\s*.(\d+\.\d+)\s*(s|ms))|(about\s*.(\d+)\s*(s|ms))'
        r'|(duration\s\w{2}\s\w{3}\s\w{5}\s\w{2}\s*.(\d+)\s*.(s|ms))|(duration\s\w{2}\s\w{3}\s\w{5}\s*.(\d+)\s*.(s|ms))'
        r'|(\d{3}\s\w{3}.\s\w\w\s*.(\d+)\s*(s|ms))|(duration\s.(\d+\.\d+)\s*(s|ms)))', string)

    # https://gcn.gsfc.nasa.gov/gcn3/19604.gcn3 - two durations

    if m is not None:
        duration = m.group(1).replace('duration of ~', '').replace('duration of the burst is ~', '').replace(
            'duration of~', '').replace('duration is ~', '').replace('duration  of ~', '').replace(' ', '').replace(
            'burst(T100)is~', '').replace('duration(T100)of~', '').replace('durationof', '').replace('ofabout',
                                                                                                     '').replace('`',
                                                                                                                 '').replace(
            '1300keV)is~', '').replace('360keV)is~', '').replace('1400keV)of~', '').replace('theburstis~', '').replace(
            'durationisabout', '').replace('duration~', '').replace('about', '').replace('theburstinis~', '').replace(
            '~', '').replace('theburstof', '').replace('theburst', '')

    else:
        duration = '--'
    print(duration)

    m = re.search(r'(fluence\s+of\s+(.+?)\s*erg|\d{4}\s\w{3}\s\w{4}\s\w{2}\s+(..................)'
                  r'|fluence\s\w{2}\s+(.......)\s+erg/cm2'
                  r'|fluence\s(...................)\s+erg/cm2)', string)
    m2 = re.search(r'(interval\s\w{2}\s+(...................)|fluence\s+(.+?)\s*erg)', string)

    if m is not None:
        fluence = m.group().replace('1500 keV band is ', '').replace('fluence of ', '').replace(' erg', '').replace(
            'interval is ', '').replace(' e', '').replace('fluence ', '').replace('this part is ', '') \
            .replace('is ', '').replace('the most intense part of the burst ', '').replace(' ', '').replace('~', '') \
            .replace('theburstsapproximately', '').replace('/cm2', '').replace('of', '')
    elif m2 is not None:
        fluence = m2.group().replace('1500 keV band is ', '').replace('fluence of ', '').replace(' erg', '').replace(
            'interval is ', '').replace(' e', '').replace('fluence ', '').replace('this part is ', '') \
            .replace('is ', '').replace('the most intense part of the burst ', '').replace(' ', '').replace('~', '') \
            .replace('theburstsapproximately', '').replace('/cm2', '')
    else:
        fluence = '--'
    err_fl = '--'

    if ')' in fluence:

        skobka = fluence.find('(')
        if skobka != -1 and skobka != 0:
            # new_fluence = fluence[0:skobka]

            fluence2 = re.search(r'([\d\.]+)\(((\-[\d\.]+\,\+[\d\.]+)|(\+\/\-[\d\.]+))\)(x?[\d\-\^]*)', fluence)
            if fluence2 is None:
                fluence2 = re.search(r'([\d\.]+)\(((\+[\d\.]+\/\-[\d\.]+)|(\+\/\-[\d\.]+))\)(x?[\d\-\^]*)', fluence)

            new_fluence = fluence2.group(1) + 'E' + fluence2.group(5)[-2:]
            err_fl = fluence2.group(2) + 'E' + fluence2.group(5)[-2:]

            if '/' in err_fl and '+/-' not in err_fl:
                err_fl = err_fl.replace('/', ',')
            if ',' in err_fl:
                index = err_fl.find(',')
                err_fl = err_fl[:index] + 'E' + fluence2.group(5)[-2:] + err_fl[index:]

        if skobka == -1 or skobka == 0:
            fluence2 = re.search(r'([\d.]+)((\+\/\-[\d.]+)|(±[\d.]+))\)(x?[\d\-\^]*)', fluence)

            new_fluence = fluence2.group(1).replace('±', '+/-') + 'E' + fluence2.group(5)[-2:]
            err_fl = fluence2.group(2).replace('±', '+/-') + 'E' + fluence2.group(5)[-2:]
    else:
        new_fluence = fluence
        if 'x' in new_fluence:
            index = new_fluence.find('x')
            new_fluence = new_fluence[:index] + 'E' + new_fluence[-2:]
        err_fl = '--'

    if ',' in err_fl:
        index = err_fl.find(',')
        err_fl1 = '-' + err_fl[1:index]
        err_fl2 = '+' + err_fl[index + 2:]
    elif '+/-' in err_fl:

        err_fl1 = '-' + err_fl.replace('+/-', '')
        err_fl2 = '+' + err_fl.replace('+/-', '')

    elif '/' in err_fl:
        index = err_fl.find('/')
        err_fl1 = '-' + err_fl[1:index]
        err_fl2 = '+' + err_fl[index + 2:]

    if err_fl == '--':
        err_fl1 = '--'
        err_fl2 = '--'

    print(new_fluence)
    print(err_fl1, err_fl2)

    # https://gcn.gsfc.nasa.gov/gcn3/5748.gcn3 - 'fluence of this part is', two fluences
    # https://gcn.gsfc.nasa.gov/gcn3/5689.gcn3 - 'fluence of this part is', two fluences

    peak_fl_res = re.search(
        (r'\d{1}.\d{1,4}-s|\d{1,4}-ms|measured\s\w\w\s\w\s\d{1}.\d{1,3}|cm2\s\w{3}\s\w\s\d{1}.\d{1,3}'
         r'|followed\s\w{2}\s.\d{1,3}|and\s\w\s\d{1,3}-s|started\s\w{2}\s\d{1,3}|over\s\d{1}.\d{1,3}'
         r'|\d{1,3}\smsec'), string)

    if peak_fl_res is not None:
        peak_fl_res = peak_fl_res.group()
        if peak_fl_res.find('-ms') != -1:
            peak_fl_res = float(peak_fl_res.replace('-ms', '')) / 1000
            peak_fl_res = str(peak_fl_res)
        if peak_fl_res.find('msec') != -1:
            peak_fl_res = float(peak_fl_res.replace('msec', '')) / 1000
            peak_fl_res = str(peak_fl_res)
        peak_fl_res = peak_fl_res.replace('-ms', '').replace('-s', '').replace('measured on a ', '').replace(
            'cm2 and a ',
            '').replace(
            'followed in ~', '').replace('and a ', '').replace('started at ', '').replace('over ', '')
    else:
        peak_fl_res = '--'
        print(peak_fl_res)

    # PFti
    m = re.search(r'peak.+flux.+?\s?T0\s?=?((\+ )?[\d+.-]+)', string)
    if m is not None:
        pf_ti = m.group(1).replace(' ', '')
    else:
        pf_ti = '--'
    print(pf_ti)

    m = re.search(r' peak.+?\D\s([\d. ]*\([\d., Â±+)/^x-]+)\serg/cm\^?2', string)
    if m is None:
        # m = re.search(r'peak.+[ ^a-zA-Z]{3,}~?([\d.x,Â\s ±+^E/()-]+)\serg/cm2', string)
        m = re.search(r' peak.+?\s~?([\d.]+[\d.x,Â\s ±+^E/()-]+)\serg/cm2', string)

    err_pf = 0
    if m is None:
        new_peak_fl = '--'
        err_pf = '--'
    else:

        peak_fl = m.group(1)
        peak_fl = peak_fl.replace(' ', '').replace('Â', '')

        if ')' in peak_fl:
            skobka = peak_fl.find('(')

            if skobka != -1 and skobka != 0:
                peak2 = re.search(r'([\d\.]+)\(((\-[\d\.]+\,\+[\d\.]+)|(\+\/\-[\d\.]+))\)(x?[\d\-\^]*)', peak_fl)

                if peak2 is None:
                    peak2 = re.search(r'([\d\.]+)\(((\+[\d\.]+\/\-[\d\.]+)|(\+\/\-[\d\.]+))\)(x?[\d\-\^]*)', peak_fl)

                new_peak_fl = peak2.group(1) + 'E' + peak2.group(5)[-2:]
                err_pf = peak2.group(2) + 'E' + peak2.group(5)[-2:]

                if '/' in err_pf and '+/-' not in err_pf:
                    err_pf = err_pf.replace('/', ',')
                if ',' in err_pf:
                    index = err_pf.find(',')
                    err_pf = err_pf[:index] + 'E' + peak2.group(5)[-2:] + err_pf[index:]

            if skobka == 0 or skobka == -1:
                peak2 = re.search(r'([\d.]+)((\+/-[\d.]+)|(±[\d.]+))\)(x?[\d\-\^]*)', peak_fl)
                new_peak_fl = peak2.group(1).replace('±', '+/-') + 'E' + peak2.group(5)[-2:]
                err_pf = peak2.group(2).replace('±', '+/-') + 'E' + peak2.group(5)[-2:]
        else:
            new_peak_fl = peak_fl
            if 'x' in new_peak_fl:
                index = new_peak_fl.find('x')
                new_peak_fl = new_peak_fl[:index] + 'E' + new_peak_fl[-2:]
            err_pf = '--'

    if ',' in err_pf:
        index = err_pf.find(',')
        err_pf1 = '-' + err_pf[1:index]
        err_pf2 = '+' + err_pf[index + 2:]
    elif '+/-' in err_pf:
        err_pf1 = '-' + err_pf.replace('+/-', '')
        err_pf2 = '+' + err_pf.replace('+/-', '')
    elif '/' in err_pf:
        index = err_pf.find('/')
        err_pf1 = '-' + err_pf[1:index]
        err_pf2 = '+' + err_pf[index + 2:]

    if err_pf == '--':
        err_pf1 = '--'
        err_pf2 = '--'

    print(new_peak_fl)
    print(err_pf1, err_pf2)

    # Ep
    m = re.search(r'Ep ?= ?([\d\(\)\-\+,\/.±Â ]+?) ?keV', string)

    if m is None:
        m = re.search(r'Epeak [\S ]+?([\d\(\)\-\+,\/.±Â ]+?) ?keV', string)
    b = 0

    if m is None:
        m = re.search(r' peak energy ([\d\(\)\-\+,\/.±Â ]+?) ?keV', string)

    if m is None:
        m = re.search(r'Ep ?= ?([\d\(\)\-\+,\/.±Â ]+?) ?MeV', string)
        if m is not None:
            b = 1

    if m is not None:
        ep = m.group(1).replace(' ', '')

        if '(' in ep and ep.find('(') != 0:
            index = ep.find('(')
            err_ep = ep[index + 1:-1]
            ep = ep[:index]
        elif '+' in ep and ep.find('(') != 0:
            index = ep.find('+')
            err_ep = ep[index:]
            ep = ep[:index]
        elif '±' in ep:
            index = ep.find('±')
            err_ep = ep[index:]
            err_ep = err_ep.replace('±', '+/-')
            ep = ep[:index]
        elif '+/-' in ep and ep.find('(') == 0:
            index = ep.find('+')
            err_ep = ep[index:-1]
            ep = ep[1:index]

        else:
            err_ep = '--'
    else:
        ep = '--'
        err_ep = '--'

    if ',' in err_ep:

        index = err_ep.find(',')
        err_ep1 = '-' + err_ep[1:index]
        err_ep2 = '+' + err_ep[index + 2:]
    elif '+/-' in err_ep:
        err_ep1 = '-' + err_ep.replace('+/-', '')
        err_ep2 = '+' + err_ep.replace('+/-', '')
    elif '/' in err_ep:
        index = err_ep.find('/')
        err_ep1 = '-' + err_ep[1:index]
        err_ep2 = '+' + err_ep[index + 2:]

    if b == 1:
        ep = str(int(float(ep) * 1000))
        err_ep1 = '-' + str(int(abs(float(err_ep1) * 1000)))
        err_ep2 = '+' + str(int(float(err_ep2) * 1000))

    if ep == '--':
        m = re.search(r'Ep ?~ ?([\d\(\)\-\+,\/.±Â ]+?) ?MeV', string)
        if m is not None:
            ep = m.group(1).replace(' ', '')
            ep = str(int(ep)*1000)
            err_ep = '--'

    if err_ep == '--':
        err_ep1 = '--'
        err_ep2 = '--'

    print(ep)
    print(err_ep1, err_ep2)

    m = re.search(r'(triggered|waiting\s*mode)', string)
    if m is not None:
        mode = m.group(1).replace(' ', '')
    else:
        mode = '--'
    print(mode)

    # https://gcn.gsfc.nasa.gov/gcn3/8611.gcn3 - 'trigger record'?

    m = re.search(r'z\s?=\s?([\d.]+)', string)
    if m is None:
        redshift = '--'
    else:
        redshift = m.group(1)

    print(redshift)

    return [b_name, starttime, starttime_ut, duration, new_fluence, err_fl1, err_fl2, pf_ti, peak_fl_res, new_peak_fl,
            err_pf1, err_pf2, ep, err_ep1, err_ep2, mode, redshift]


def main():
    with open("links.txt") as f:
        lines = f.read().split('\n')

    lst_data = []
    for line in lines:
        line = line.strip()
        print(line)
        str_gcn = line[-10:-5]
        response = requests.get(line)

        # soup = BeautifulSoup(response.content, "lxml")
        # ptag = soup.find(lambda tag: tag.name == 'p')
        # string = str(ptag)
        string = response.text

        res = parce_line(string)
        if res is not None:
            lst_data.append([str_gcn, ] + res)

    write_tab(lst_data)


main()
