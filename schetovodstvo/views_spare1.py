from django.shortcuts import render
from .models import vedomost, smetkoplan
from .forms import UploadFileForm,criterii_filtar 
import csv
import io
from django.forms import modelformset_factory
# Create your views here.


class Sm:
    def __init__(self,smetka,s_ime, dt, kt,odt,okt,s_dt,s_kt):
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
    for row in xxx:
            for key in smetkoplan_obj:
                if row.debit==smetkoplan_obj[key].smetka:
                    smetkoplan_obj[key].debit+=float(row.suma)
                    smetkoplan_obj[key].s_debit+=float(row.suma)
                if row.credit==smetkoplan_obj[key].smetka:
                    smetkoplan_obj[key].kredit+=float(row.suma)
                    smetkoplan_obj[key].s_kredit+=float(row.suma)
                if smetkoplan_obj[key].s_debit>smetkoplan_obj[key].s_kredit:
                    smetkoplan_obj[key].s_debit=smetkoplan_obj[key].s_debit-smetkoplan_obj[key].s_kredit
                    smetkoplan_obj[key].s_kredit=0
                elif smetkoplan_obj[key].s_debit<smetkoplan_obj[key].s_kredit:
                    smetkoplan_obj[key].s_debit=0
                    smetkoplan_obj[key].s_kredit=smetkoplan_obj[key].s_kredit-smetkoplan_obj[key].s_debit
    

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
    
    for smetka in smetki:
        smetkoplan_obj[smetka.smetka]=Sm(smetka.smetka,smetka.opisanie,smetka.n_saldo_dt,smetka.n_saldo_kt,0,0,0,0)

#    for row in ved:
#            for key in smetkoplan_obj:
#                if row.debit==smetkoplan_obj[key].smetka:
#                    smetkoplan_obj[key].debit+=float(row.suma)
#                    smetkoplan_obj[key].s_debit+=float(row.suma)
#                if row.credit==smetkoplan_obj[key].smetka:
#                    smetkoplan_obj[key].kredit+=float(row.suma)
#                    smetkoplan_obj[key].s_kredit+=float(row.suma)
#                if smetkoplan_obj[key].s_debit>smetkoplan_obj[key].s_kredit:
#                    smetkoplan_obj[key].s_debit=smetkoplan_obj[key].s_debit-smetkoplan_obj[key].s_kredit
#                    smetkoplan_obj[key].s_kredit=0
#                elif smetkoplan_obj[key].s_debit<smetkoplan_obj[key].s_kredit:
#                    smetkoplan_obj[key].s_debit=0
#                    smetkoplan_obj[key].s_kredit=smetkoplan_obj[key].s_kredit-smetkoplan_obj[key].s_debit
    smetkoplan_analiz(ved, smetkoplan_obj)

#    for key in smetkoplan_obj:
#        if smetkoplan_obj[key].n_debit+smetkoplan_obj[key].debit>smetkoplan_obj[key].n_kredit+smetkoplan_obj[key].kredit:
#            smetkoplan_obj[key].s_debit=(smetkoplan_obj[key].n_debit+smetkoplan_obj[key].debit)-(smetkoplan_obj[key].n_kredit+smetkoplan_obj[key].kredit)
#        if smetkoplan_obj[key].n_debit+smetkoplan_obj[key].debit<smetkoplan_obj[key].n_kredit+smetkoplan_obj[key].kredit:
#           smetkoplan_obj[key].s_kredit=(smetkoplan_obj[key].n_kredit+smetkoplan_obj[key].kredit)-(smetkoplan_obj[key].n_debit+smetkoplan_obj[key].debit) 
    
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
                                                  # Here uploaded_file is a binary file object
            file_content = uploaded_file.read().decode('windows-1251')#file_content is a string representation of the binary file object - uploaded_file
            lines = file_content.splitlines()

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
                    suma1=row[175:182].strip()
                    suma2=row[182:199].strip()
                    suma3=row[199:220].strip()
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
 
                    vedomost.objects.create(first_f=first_f, doc=doc, date=date, nomer=nomer, firma=partnior, buls=bulstat_part, opisanie=opisanie, suma=suma2, debit=debit1, credit=kredit1) 
                    vedomost.objects.create(first_f=first_f, doc=doc, date=date, nomer=nomer, firma=partnior, buls=bulstat_part, opisanie=opisanie, suma=suma3, debit=debit2, credit=kredit2) 

                except Exception as e:
                    print(f"Error")
 
    return render(request, 'upload_pok.html', {'form': form, 'file_content': file_content, 'lines1':lines1})

def function_display(request):
    form_criterii=criterii_filtar()


    context = {
        'form_criterii': form_criterii,
  
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

            
            
    

    
