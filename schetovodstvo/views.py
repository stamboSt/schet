from django.shortcuts import render
from .models import vedomost, smetkoplan
from .forms import UploadFileForm,criterii_filtar, vedomost_form 
import csv
import io
from django.forms import modelformset_factory
from django.db.models import Q
# Create your views here.


class Sm:
    def __init__(self,smetka,s_ime, dt, kt,odt,okt):
        self.smetka=smetka
        self.s_ime=s_ime
        self.n_debit=float(dt)
        self.n_kredit=float(kt)
        self.debit=float(odt)
        self.kredit=float(okt)
#        self.s_debit=float(s_dt)
#        self.s_kredit=float(s_kt)
        if (self.n_debit+self.debit)-(self.n_kredit+self.kredit)>0:
            self.s_debit=float(self.n_debit+self.debit-self.n_kredit-self.kredit)
            self.s_kredit=0
        elif (self.n_kredit+self.kredit)-(self.n_debit+self.debit)>0:
            self.s_debit=0
            self.s_kredit=float(self.n_kredit+self.kredit-self.n_debit-self.debit)
        else:
            self.s_debit=0
            self.s_kredit=0

def smetkoplan_analiz(xxx, smetkoplan_obj):
    for row in xxx: # за всеки ред от таблицата, която съдържа осчетоводените операции
            for key in smetkoplan_obj: # за всеки ключ от речника smetkoplan_obj
                if row.debit==smetkoplan_obj[key].smetka: # ако стойността в колоната debit на таблицата е равна на стойността на ключа smetka 
                    smetkoplan_obj[key].debit+=float(row.suma)
                    if (smetkoplan_obj[key].n_debit+smetkoplan_obj[key].debit)-(smetkoplan_obj[key].n_kredit+smetkoplan_obj[key].kredit)>0:
                        smetkoplan_obj[key].s_debit=float(smetkoplan_obj[key].n_debit+smetkoplan_obj[key].debit-smetkoplan_obj[key].n_kredit-smetkoplan_obj[key].kredit)
                        smetkoplan_obj[key].s_kredit=0
                    elif (smetkoplan_obj[key].n_kredit+smetkoplan_obj[key].kredit)-(smetkoplan_obj[key].n_debit+smetkoplan_obj[key].debit)>0:
                        smetkoplan_obj[key].s_debit=0
                        smetkoplan_obj[key].s_kredit=float(smetkoplan_obj[key].n_kredit+smetkoplan_obj[key].kredit-smetkoplan_obj[key].n_debit-smetkoplan_obj[key].debit)

#                    smetkoplan_obj[key].s_debit+=float(row.suma)
                if row.credit==smetkoplan_obj[key].smetka: # ако стойността в колоната debit на таблицата е равна на стойността на ключа smetka 
                    smetkoplan_obj[key].kredit+=float(row.suma)
                    if (smetkoplan_obj[key].n_debit+smetkoplan_obj[key].debit)-(smetkoplan_obj[key].n_kredit+smetkoplan_obj[key].kredit)>0:
                        smetkoplan_obj[key].s_debit=float(smetkoplan_obj[key].n_debit+smetkoplan_obj[key].debit-smetkoplan_obj[key].n_kredit-smetkoplan_obj[key].kredit)
                        smetkoplan_obj[key].s_kredit=0
                    elif (smetkoplan_obj[key].n_kredit+smetkoplan_obj[key].kredit)-(smetkoplan_obj[key].n_debit+smetkoplan_obj[key].debit)>0:
                        smetkoplan_obj[key].s_debit=0
                        smetkoplan_obj[key].s_kredit=float(smetkoplan_obj[key].n_kredit+smetkoplan_obj[key].kredit-smetkoplan_obj[key].n_debit-smetkoplan_obj[key].debit)





#                    smetkoplan_obj[key].s_kredit+=float(row.suma)
#                if smetkoplan_obj[key].s_debit>smetkoplan_obj[key].s_kredit: #
#                    smetkoplan_obj[key].s_debit=smetkoplan_obj[key].s_debit-smetkoplan_obj[key].s_kredit
#                    smetkoplan_obj[key].s_kredit=0
#                elif smetkoplan_obj[key].s_debit<smetkoplan_obj[key].s_kredit: #
#                    smetkoplan_obj[key].s_debit=0
#                    smetkoplan_obj[key].s_kredit=smetkoplan_obj[key].s_kredit-smetkoplan_obj[key].s_debit
    

def index(request):
       
    return render(request, 'base.html')

def oschetovodiavane_pokupki(opisanie,opisanie2):
    stoki_list=['храни','храна','консум','пиво','плод','зелен','сток','пром','цигари','хляб','хлебни','брашн','зърнен','тест. изд.','риба','разни','месо','месни','мляко','млечни','кашк','л-ца','подправ','бира','безалк','напитк','захарн','зах.','кафе','ст.дом','промишлен','препара','прах','тестен','закус','ядки','боза','сладолед','чай','пампер','детск','мин.','пюре']
    uslugi_list=['сервиз','услуг','охрана','обслужване','абонам','ремонт','ремнот']
    elektrichestvo=['електричество','ток','енергия']
    lizing=['лизинг','лизингова']
    materiali_remont=['дървев мат', 'стр.','строителни']
    ch_string=opisanie
    contr_string=opisanie2
    list_smetki=[]
 
    if any(ele in ch_string for ele in stoki_list):#oschetovodiavane na zakupuvane na stoki
        smetka1_dt=304
 #           list_smetki.append(smetka1_dt)
        smetka1_kt=501
 #           list_smetki.append(smetka2_kt)
        smetka2_dt=4531
 #           list_smetki.append(smetka2_dt)
        smetka2_kt=501
 #           list_smetki.append(smetka2_kt)
        list_smetki=[smetka1_dt,smetka1_kt,smetka2_dt,smetka2_kt]

    elif any(ele in ch_string for ele in uslugi_list):#oschetovodiavane na zakupuvane na uslugi
        smetka1_dt=602
        smetka1_kt=501
        smetka2_dt=4531
        smetka2_kt=501
        list_smetki=[smetka1_dt,smetka1_kt,smetka2_dt,smetka2_kt]

    elif any(ele in ch_string for ele in materiali_remont):#oschetovodiavane na zakupuvane na uslugi
        smetka1_dt=601
        smetka1_kt=501
        smetka2_dt=4531
        smetka2_kt=501
        list_smetki=[smetka1_dt,smetka1_kt,smetka2_dt,smetka2_kt]

    elif any(ele in ch_string for ele in elektrichestvo):#oschetovodiavane na zakupuvane na el.tok 6021
        smetka1_dt=6021
        smetka1_kt=501
        smetka2_dt=4531
        smetka2_kt=501
        smetka3_dt=0
        smetka3_kt=0
        smetka4_dt=0
        smetka4_kt=0
        list_smetki=[smetka1_dt,smetka1_kt,smetka2_dt,smetka2_kt]

    elif ch_string=='вода':#oschetovodiavane na zakupuvane na voda 6022
        smetka1_dt=6022
        smetka1_kt=501
        smetka2_dt=4531
        smetka2_kt=501
        smetka3_dt=0
        smetka3_kt=0
        smetka4_dt=0
        smetka4_kt=0
        list_smetki.append(smetka1_dt,smetka1_kt,smetka2_dt,smetka2_kt)


    elif ch_string=='наем' and contr_string=='BG000573078':#oschetovodiavane na naem RPK Balkan 6023
        smetka1_dt=6023
        smetka1_kt=501
        smetka2_dt=4531
        smetka2_kt=501
        smetka3_dt=0
        smetka3_kt=0
        smetka4_dt=0
        smetka4_kt=0
        list_smetki=[smetka1_dt,smetka1_kt,smetka2_dt,smetka2_kt]

    elif ch_string=='наем' and contr_string!='BG000573078':#oschetovodiavane na naem 6023
        smetka1_dt=6023
        smetka1_kt=4012
        smetka2_dt=4531
        smetka2_kt=4012
        smetka3_dt=0
        smetka3_kt=0
        smetka4_dt=0
        smetka4_kt=0
        list_smetki=[smetka1_dt,smetka1_kt,smetka2_dt,smetka2_kt]

    elif ch_string=='гориво':#oschetovodiavane na zakupuvane na gorivo 302
        smetka1_dt=302
        smetka1_kt=501
        smetka2_dt=4531
        smetka2_kt=501
        smetka3_dt=0
        smetka3_kt=0
        smetka4_dt=0
        smetka4_kt=0
        list_smetki=[smetka1_dt,smetka1_kt,smetka2_dt,smetka2_kt]

    elif any(ele in ch_string for ele in lizing):#oschetovodiavane na вноска лизинг
        smetka1_dt=159
        smetka1_kt=4011
        smetka2_dt=6212
        smetka2_kt=625
        smetka3_dt=4531
        smetka3_kt=4011
        smetka4_dt=159
        smetka4_kt=4011
        list_smetki=[smetka1_dt,smetka1_kt,smetka2_dt,smetka2_kt,smetka3_dt,smetka3_kt,smetka4_dt,smetka4_kt]
        
    else:
        smetka1_dt=0
        smetka1_kt=0
        smetka2_dt=0
        smetka2_kt=0
        smetka3_dt=0
        smetka3_kt=0
        smetka4_dt=0
        smetka4_kt=0
        list_smetki=[smetka1_dt,smetka1_kt,smetka2_dt,smetka2_kt]
    return list_smetki
            
def oborotna_vedomost(request):
    smetki=smetkoplan.objects.all()
    ved=vedomost.objects.all()
    smetkoplan_obj={}
#за всяка сметка от таблицата сметкоплан се създава елемент от речника smetkoplan_obj    
    for smetka in smetki:
        smetkoplan_obj[smetka.smetka]=Sm(smetka.smetka,smetka.opisanie,smetka.n_saldo_dt,smetka.n_saldo_kt,0,0)

#тук функцията smetkoplan_analiz  
    smetkoplan_analiz(ved, smetkoplan_obj)

    
    return render(request, 'catalog.html',{'smetkoplan_obj':smetkoplan_obj})


def upload_file_prodajbi(request):
    file_content = None
    form = UploadFileForm()
    listi_file=[]
    lines=[]
    lines1=[]

            
        
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = request.FILES['file'] # When a user uploads a text-based file (like CSV), Django gives you a File object in request.FILES.
                                                  # Here uploaded_file is a binary file object - opened file.
                                                  # request.FILES will only contain data if the request method was POST, at least one file field was actually posted,
                                                  # and the <form> that posted the request has the attribute enctype="multipart/form-data". Otherwise, request.FILES
                                                  # will be empty
            file_content = uploaded_file.read().decode('windows-1251')#file_content is a string representation of the binary file object - uploaded_file
            lines = file_content.splitlines() # splitlines () method splits a string into a list. The splitting is done at line breaks.

            for row in lines:
                try:
                    buls=row[0:11].strip()
                    first_f=row[11:21].strip()
                    aparat=row[21:42].strip()
                    nomer=row[42:44].strip()
                    date=row[44:72].strip()
                    firma='Kalina'
                    opisanie=row[72:149].strip()
                    suma1=row[149:182].strip()
                    suma2=row[182:197].strip()
                    doc='отчет за продажбите'
                    debit1='501'
                    kredit1='702'
                    debit2='501'
                    kredit2='4532'
                    check=str(first_f+';'+doc+';'+date+';'+nomer+';'+firma+';'+buls+';'+opisanie+';'+suma1+';'+debit1+';'+kredit1)
                    lines1.append(check)

                    if vedomost.objects.filter(nomer=nomer, opisanie=opisanie).exists():
                        continue
                    
                    vedomost.objects.create(first_f=first_f, doc=doc, date=date, nomer=nomer, firma=firma, buls=buls, opisanie=opisanie, suma=suma1, debit=debit1, credit=kredit1) 
                    vedomost.objects.create(first_f=first_f, doc=doc, date=date, nomer=nomer, firma=firma, buls=buls, opisanie=opisanie, suma=suma2, debit=debit2, credit=kredit2) 

                except Exception as e:
                    print(f"Error")
 
    return render(request, 'upload.html', {'form': form, 'file_content': file_content, 'lines1':lines1})

def upload_file_pokupki(request):
    file_content = None
    form = UploadFileForm()
    listi_file=[]
    lines=[]
    lines1=[]

            
        
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = request.FILES['file'] # When a user uploads a text-based file (like CSV), Django gives you a File object in request.FILES.
                                                  # Here uploaded_file is a binary file object
            file_content = uploaded_file.read().decode('windows-1251')#file_content is a string representation of the binary file object - uploaded_file
            lines = file_content.splitlines()

            for row in lines:
                try:
                    buls=row[0:11].strip()
                    first_f=row[11:21].strip()
 #                   aparat=row[21:50].strip()
                    nomer=row[21:53].strip()
                    date=row[53:72].strip()
                    bulstat_part=row[72:83].strip()
                    partnior=row[83:135].strip()
                    opisanie=row[135:175].strip()
                    suma1=row[175:182].strip()#suma - obsto
                    suma2=row[182:199].strip()#suma - osnova
                    suma3=row[199:220].strip()#suma - DDS
                    doc='фактура'
 #                   debit1='501'
 #                   kredit1='702'
 #                   debit2='501'
 #                   kredit2='4532'
 #                   check=str(first_f+';'+doc+';'+date+';'+nomer+';'+partnior+','+bulstat_part+';'+opisanie+';'+suma2+';'+debit1+';'+kredit1)
 #                   lines1.append(check)
                    list_smetki=oschetovodiavane_pokupki(opisanie,bulstat_part)
                    lines1.append(list_smetki)

                    if vedomost.objects.filter(nomer=nomer, opisanie=opisanie).exists():
                       continue

                    debit1=list_smetki[0]
                    kredit1=list_smetki[1]
                    debit2=list_smetki[2]
                    kredit2=list_smetki[3]
 
                    vedomost.objects.create(first_f=first_f, doc=doc, date=date, nomer=nomer, firma=partnior, buls=bulstat_part, opisanie=opisanie, suma=suma3, debit=debit1, credit=kredit1) 
                    vedomost.objects.create(first_f=first_f, doc=doc, date=date, nomer=nomer, firma=partnior, buls=bulstat_part, opisanie=opisanie, suma=suma3, debit=debit2, credit=kredit2) 

                except Exception as e:
                    print(f"Error")
 
    return render(request, 'upload_pok.html', {'form': form, 'file_content': file_content, 'lines1':lines1})


def upload_file_zaplati(request):
    file_content = None
    form = UploadFileForm()
    reader=[]
    list=[]
    x=1
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = request.FILES['file'] # When a user uploads a text-based file (like CSV), Django gives you a File object in request.FILES.
                                                  # Here uploaded_file is a binary file object
            file_content = uploaded_file.read().decode('windows-1251')
            io_string = io.StringIO(file_content)

            reader = csv.reader(io_string, delimiter=',')
            for row in reader:
                month=row[0]
                year=row[1]
                first_f=year+month
                doc='ведомост за заплати' 
                if vedomost.objects.filter(first_f=first_f, doc=doc).exists():
                    lines1='This file has been already uploaded'
                    return render(request, 'upload_zaplati.html', {'form': form, 'lines1':lines1})

                else:
                    for row in reader:
                        try:
                            month=row[0]
                            year=row[1]
                            buls=row[2]
                            egn=row[3]
                            family=row[5]
                            init=row[6]
                            vid_osig=int(row[7])

                            dni_osig=int(row[18])
                            
                            boln=int(row[20])
                            maichinstvo=int(row[21])

                            dni_boln_rab=int(row[24])
                            chasove=int(row[25])

                            osig_dohod=float(row[33])
                            doo_firma=float(row[34])
                            doo_rabotnik=float(row[35])
                            zov_firma=float(row[36])
                            zov_rabotnik=float(row[37])
                            tzpb=float(row[38])

                            upf_firma=float(row[41])
                            upf_rabotnik=float(row[42])

                            bruto=float(row[45])
                            obl_dohod=float(row[47])
                            danak=float(row[48])
                            neto=float(row[49])

                            if int(month)<10:
                                first_f=year+'0'+month
                            else:
                                first_f=year+month
                            doc='ведомост за заплати'
                            



                            if vid_osig==1 and dni_osig>0 and boln+maichinstvo==0: #19-брой отработени дни; 20,21 -някакви болнични
                                list1=[first_f, doc, year, month, family, egn]
                                list.append(list1)


                                osnova=float(osig_dohod)

                                doo_rabotodatel=doo_firma
                                doo_rabotodatel_t="ДОО за сметка на работодател"
                                doo_rabotodatel_v=osnova*doo_rabotodatel/100
             
                                doo_rabotnik=doo_rabotnik
                                doo_rabotnik_t="ДОО за сметка на работника"
                                doo_rabotnik_v=osnova*doo_rabotnik/100
                                
                                zdr_rabotodatel=zov_firma
                                zdr_rabotodatel_t="ЗДРАВНИ за сметка на работодател"
                                zdr_rabotodatel_v=osnova*zdr_rabotodatel/100
                             
                            
                                zdr_rabotnik=zov_rabotnik
                                zdr_rabotnik_t="ЗДРАВНИ за сметка на работника"
                                zdr_rabotnik_v=osnova*zdr_rabotnik/100

                                
                                tzpb1=tzpb
                                tzpb_rabotodatel_t="ТЗПБ"
                                tzpb_rabotodatel_v=osnova*tzpb1/100
                                
                            
                                dzpo_rabotodatel=upf_firma
                                dzpo_rabotodatel_t="ДЗПО за сметка на работодател"
                                dzpo_rabotodatel_v=osnova*dzpo_rabotodatel/100
                                
                            
                                dzpo_rabotnik=upf_rabotnik
                                dzpo_rabotnik_t="ДЗПО за сметка на работника"
                                dzpo_rabotnik_v=osnova*dzpo_rabotnik/100
                               

                                nach_zaplata_v=bruto
                                nach_zaplata_t="начислена заплата"
                                
                                izpl_zaplata_v=neto
                                izpl_zaplata_t="изплатена заплата"

                                dod_v=danak
                                dod_t="начислен ДОД"

                                
                                
                                vedomost.objects.create(first_f=first_f, doc=doc, date=year, nomer=month, firma=family, buls=egn, opisanie=doo_rabotodatel_t, suma=round(doo_rabotodatel_v,2), debit='605',credit='461')
                                vedomost.objects.create(first_f=first_f, doc=doc, date=year, nomer=month, firma=family, buls=egn, opisanie=doo_rabotnik_t, suma=round(doo_rabotnik_v,2), debit='421',credit='461')
                                vedomost.objects.create(first_f=first_f, doc=doc, date=year, nomer=month, firma=family, buls=egn, opisanie=zdr_rabotodatel_t, suma=round(zdr_rabotodatel_v,2), debit='605',credit='463')
                                vedomost.objects.create(first_f=first_f, doc=doc, date=year, nomer=month, firma=family, buls=egn, opisanie=zdr_rabotnik_t, suma=round(zdr_rabotnik_v,2), debit='421',credit='463')
                                vedomost.objects.create(first_f=first_f, doc=doc, date=year, nomer=month, firma=family, buls=egn, opisanie=tzpb_rabotodatel_t, suma=round(tzpb_rabotodatel_v,2), debit='605',credit='461')
                                vedomost.objects.create(first_f=first_f, doc=doc, date=year, nomer=month, firma=family, buls=egn, opisanie=dzpo_rabotodatel_t, suma=round(dzpo_rabotodatel_v,2), debit='605',credit='461')
                                vedomost.objects.create(first_f=first_f, doc=doc, date=year, nomer=month, firma=family, buls=egn, opisanie=dzpo_rabotnik_t, suma=round(dzpo_rabotnik_v,2), debit='421',credit='461')
                                vedomost.objects.create(first_f=first_f, doc=doc, date=year, nomer=month, firma=family, buls=egn, opisanie=dod_t, suma=round(dod_v,2), debit='421',credit='454')
                                vedomost.objects.create(first_f=first_f, doc=doc, date=year, nomer=month, firma=family, buls=egn, opisanie=izpl_zaplata_t, suma=round(izpl_zaplata_v,2), debit='421',credit='501')
                                
                        except Exception as e:
                            print(f"Error")
 
    return render(request, 'upload_zaplati.html', {'form': form, 'lines1':list})

def upload_file_bank(request):
    file_content = None
    form = UploadFileForm()
    reader=[]
    list=[]
    list1=[]
    l1=['ТАКСА']
    l2=['ДЕПОЗИТ']
    l3=['НАЕМ']
    l4=['ДДС']
    x=0
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = request.FILES['file'] # When a user uploads a text-based file (like CSV), Django gives you a File object in request.FILES.
                                                  # Here uploaded_file is a binary file object
            file_content = uploaded_file.read().decode('windows-1251')
            io_string = io.StringIO(file_content)

            reader = csv.reader(io_string, delimiter=';')
            for row in reader:
                try:
                    data=row[1]
                    data1=data[6:10]
                    data2=data[3:5]
                    first_f=data1+data2
                    doc='банково извлечение'
                    nomer=row[2]
                    suma=row[4]
                    operacia=row[7]
                    opisanie2=row[8]
                    opisanie1=opisanie2.partition(',')#opisanie1 is a tuple, where the different members are the parts of the text in opisanie, separated by ,
                    opisanie=opisanie1[0]
                    


                    if any(ele in opisanie for ele in ['ТАКСА']):
                        vedomost.objects.create(first_f=first_f, doc=doc, date=data, nomer=nomer, firma="", buls="", opisanie=opisanie, suma=suma, debit=int('629'), credit=int('503'))
                        list1=[first_f, doc, data, nomer, '', '', opisanie, suma, int('629'), int('503')]
                        list.append(list1)
                    elif any(ele in opisanie for ele in ['ДЕПОЗИТ', 'ЗАХРАНВАНЕ']):
                        vedomost.objects.create(first_f=first_f, doc=doc, date=data, nomer=nomer, firma="", buls="", opisanie=opisanie, suma=suma, debit=int('503'), credit=int('501'))
                        list2=[first_f, doc, data, nomer, '', '', opisanie, suma, int('503'), int('501')]
                        list.append(list2)
                    elif any(ele in opisanie for ele in ['НАЕМ']):
                        vedomost.objects.create(first_f=first_f, doc=doc, date=data, nomer=nomer, firma="", buls="", opisanie=opisanie, suma=suma, debit=int('4012'), credit=int('503'))
                        list2=[first_f, doc, data, nomer, '', '', opisanie, suma, int('4012'), int('503')]
                        list.append(list2)
                    elif any(ele in opisanie for ele in ['ДДС']):
                        vedomost.objects.create(first_f=first_f, doc=doc, date=data, nomer=nomer, firma="", buls="", opisanie=opisanie, suma=suma, debit=int('4539'), credit=int('503'))
                        list2=[first_f, doc, data, nomer, '', '', opisanie, suma, int('4539'), int('503')]
                        list.append(list2)
                    elif any(ele in opisanie for ele in ['ЗОВ', 'ЗДР.']):
                        vedomost.objects.create(first_f=first_f, doc=doc, date=data, nomer=nomer, firma="", buls="", opisanie=opisanie, suma=suma, debit=int('463'), credit=int('503'))
                        list2=[first_f, doc, data, nomer, '', '', opisanie, suma, int('463'), int('503')]
                        list.append(list2)
                    elif any(ele in opisanie for ele in ['ДОО', 'ДЗПО', 'ТЗПБ']):
                        vedomost.objects.create(first_f=first_f, doc=doc, date=data, nomer=nomer, firma="", buls="", opisanie=opisanie, suma=suma, debit=int('461'), credit=int('503'))            #            vedomost.objects.create(first_f=first_f, doc=doc, date=date, nomer=nomer, firma=partnior, buls=bulstat_part, opisanie=opisanie, suma=suma, debit=debit1, credit=kredit1)
                        list2=[first_f, doc, data, nomer, '', '', opisanie, suma, int('461'), int('503')]
                        list.append(list2)
                    elif any(ele in opisanie for ele in ['ДАН.', 'ДАНЪЧНИ']):
                        vedomost.objects.create(first_f=first_f, doc=doc, date=data, nomer=nomer, firma="", buls="", opisanie=opisanie, suma=suma, debit=int('454'), credit=int('503'))            #            vedomost.objects.create(first_f=first_f, doc=doc, date=date, nomer=nomer, firma=partnior, buls=bulstat_part, opisanie=opisanie, suma=suma, debit=debit1, credit=kredit1)
                        list2=[first_f, doc, data, nomer, '', '', opisanie, suma, int('454'), int('503')]
                        list.append(list2)
                    elif any(ele in opisanie1[0] for ele in ['ПОГАСЯВАНЕ НА КРЕДИТ']) and any(ele in opisanie1[2] for ele in ['ПОГАСЯВАНЕ ГЛАВНИЦА']) :
                        vedomost.objects.create(first_f=first_f, doc=doc, date=data, nomer=nomer, firma="", buls="", opisanie=opisanie, suma=suma, debit=int('152'), credit=int('503'))            #           vedomost.objects.create(first_f=first_f, doc=doc, date=date, nomer=nomer, firma=partnior, buls=bulstat_part, opisanie=opisanie, suma=suma, debit=debit1, credit=kredit1)
                        list2=[first_f, doc, data, nomer, '', '', opisanie, suma, int('152'), int('503')]
                        list.append(list2)
                    elif any(ele in opisanie1[0] for ele in ['ПОГАСЯВАНЕ НА КРЕДИТ']) and any(ele in opisanie1[2] for ele in ['ПОГАСЯВАНЕ ЛИХВА']) :
                        vedomost.objects.create(first_f=first_f, doc=doc, date=data, nomer=nomer, firma="", buls="", opisanie=opisanie, suma=suma, debit=int('621'), credit=int('503'))            #           vedomost.objects.create(first_f=first_f, doc=doc, date=date, nomer=nomer, firma=partnior, buls=bulstat_part, opisanie=opisanie, suma=suma, debit=debit1, credit=kredit1)
                        list2=[first_f, doc, data, nomer, '', '', opisanie, suma, int('621'), int('503')]
                        list.append(list2)
                    elif any(ele in opisanie1[0] for ele in ['Транзакции с Карти']) :
                        vedomost.objects.create(first_f=first_f, doc=doc, date=data, nomer=nomer, firma="", buls="", opisanie=opisanie, suma=suma, debit=int('501'), credit=int('503'))            #           vedomost.objects.create(first_f=first_f, doc=doc, date=date, nomer=nomer, firma=partnior, buls=bulstat_part, opisanie=opisanie, suma=suma, debit=debit1, credit=kredit1)
                        list2=[first_f, doc, data, nomer, '', '', opisanie, suma, int('501'), int('503')]
                        list.append(list2)

                    else:
                        vedomost.objects.create(first_f=first_f, doc=doc, date=data, nomer=nomer, firma="", buls="", opisanie=opisanie, suma=suma, debit=int('0'), credit=int('0'))
                        list3=[first_f, doc, data, nomer, '', '', opisanie, suma, int('0'), int('0')]
                        list.append(list3)



                    
                except Exception as e:
                    print(f"Error")
    return render(request, 'upload_bank.html', {'form': form, 'lines1':list})      

#This function call the display template and serves as a filter with options to search in the opisanie of the transactions and by account - usefull to filter 'neoschetovodeni' operations
def function_display(request):
    
#  modelformset_factory creates a formset class (a collection of model forms) tied to a specific model (vedomost)
#can_delete=True - adds a checkbox in the formset (beside each row). If the box is checked, after the submit button is hit, the relative row is deleted
    VedomostFormSet = modelformset_factory(vedomost, form=vedomost_form, extra=0, can_delete=True)

# An instance of the form to enter the criteria is created. or None is very important because when loading the page for the first time it helps to crate an unbound form
    form=criterii_filtar(request.GET or None)

# initialize a default empty queryset
#    query_smetki=None
    query_smetki=vedomost.objects.all()
# initialize a default empty formset
    formset=None
   
#here the values from the form with criterias are accepted and querysets according are created    
    if form.is_valid():
#        query_smetki=vedomost.objects.all()
        cd = form.cleaned_data
        field1=cd['crit1']
       
        field2=cd['crit2']
        
        field3=cd['crit3']
        field4=cd['crit4']


        if field1:
            query_smetki = query_smetki.filter(opisanie__icontains=field1)
        if field2:
            query_smetki = query_smetki.filter(Q(debit=int(field2)) | Q(credit=int(field2)))
        if field3:
            query_smetki = query_smetki.filter(doc=field3)
        if field4:
            query_smetki = query_smetki.filter(first_f=field4)
              
#        if field1 and field2:
#            query_smetki = vedomost.objects.filter(Q(debit=int(field2)) | Q(credit=int(field2)),  Q(opisanie__icontains=field1))

#values from the formset are accepted here and saved in the database
        if request.method == 'POST':
            formset=VedomostFormSet(request.POST, queryset=query_smetki)
            if formset.is_valid():
                formset.save()
            else:
                print(formset.errors)
#creation of the formset
        else:
            formset = VedomostFormSet(queryset=query_smetki)
    

    context = {
        'form_criterii': form,
        'zaiavka':query_smetki,
        'formset':formset,
  
    }
    return render(request, 'display.html', context)
    







'''
#This part is for csv files
            io_string = io.StringIO(file_content)#io.StringIO is a class from Python’s io module that allows you to create an in-memory file-like object
                                                 #— like a virtual text file that exists in RAM, not on disk. csv.reader expects a file-like object
                                                 #so in order to read the string in file_content csv.reader should receive it in a form of file-like object - wraped with StringIO
            reader = csv.reader(io_string, delimiter=';') #Reads rows from a CSV-formatted file (or file-like object) and returns them as lists of strings.
                                                          # Each line of the file is represented as a list of strings - separated by the separator
            for row in reader:
                listi_file.append(row)
 #               buls, first_f, aparat, date, opisanie, suma1, suma2
'''

            
            
    

    
