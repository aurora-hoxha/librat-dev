Branch: **master** rekomandimet kryhen synchronous dhe vonon pak sa te ngarkohet '/rekomandime'

Branch: **rekomandime_optimizim** rekomandimet kryhen paralelisht dhe nuk bllokojne perdorimin e aplikacionit (asynchronous).

______________________________________________________________

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

______________________________________________________________

##Update, branch i ri##

Ne prezantimin e meparshem, url /rekomandime kerkonte kohe ekzekutimi pasi procesoheshin shume te dhena (120k+). Mendova te perfshij nje auto schedular si CronTab por duke qene se OS im eshte Windows dhe CronTab kerkon Linux, nuk munda ta perdor. Kete librari e zevendesova me 'background_task'.

Ceshtja kyce e optimizimit eshte kur perdoruesi logohet per here te pare, ne background ne proces paralel gjenerohet lista e librave te rekomandushem. Eshte i nevojshem nje proces paralel pasi kodi ne django ekzekutohet ne menryre iterative dhe serish do kishim humbje kohe. Pra ne momentin qe perdoruesi logohet, ngreme funksionin e rekomandimit. Nese perdoruesi menjehere klikon 'rekomandime' kjo view do te presi sa te ekzekutohet procesi paralel, edhe te marre te dhenat prej ati procesi. Kjo lloj zgjidhje e rrit performancen me gati 90%, por do pak me shume kohe qe te testohet per ndonje anomali. (Django async views mund te ishte nje zgjidhje tjeter e mire, por mendoj qe del jasht scop-it te kesaj detyre)

** Hapat e ekzekutimit **

py manage.py runserver
py manage.py process_tasks