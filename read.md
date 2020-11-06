
**Ne kete dorezim kam punuar tek filet:**
1. scripts/auto_rater.py
2. scripts/sinkronizo.py && sinkronizo_mesataret()
3. View:  'app/rekomandime.py'  dhe  'app/views.py => vlerso_liber' (form vlersimi per librat (liber.html))

______________________________________________________________

**1. Bej migrimet** (skip)

**2. Instalo requirements.txt** 

` pip install -r requirements.txt`

**3. Databaza**

Databaze aktuale eshte e mbushur me perdorues te cilet kane vlersuar libra.
Ky proces eshte gjeneruar automatikisht nga scripti 'auto_rater'. Por keto libra te vlersuar
perdoruesit nuk i shtohen tek modeli Profil. Qe keto libra te shtohen
tek Profil gjenerojme skriptin 'sinkronizo_librat_e_mi'. 

Pra, nese kemi databazen e vjeter bejme keto hapa (ne kemi DB e re):
1. ekzekutojme skriptin ne filen 'auto_rater'
2. ekzekutojme skriptin 'sinkronizo_librat_e_mi(user_ud)' ne file-n 'sinkronizo'
3. ekzekutojme skriptin 'sinkronizo_mesataret()'   ne file-n 'sinkronizo' (per te afshiuar mesataret e vlersimeve qe ka gjeneruar ''auto_rater')

@/ Kujdes mos ekzekuto scriptet nqs ke Db e re, sepse ka kohe perocesimi te larte

username: Demo
password: demo2020