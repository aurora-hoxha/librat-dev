import operator

import pandas as pd
from background_task import background
from sklearn.metrics.pairwise import cosine_similarity

from app import globals
from app.models import Liber, Vlersim, Cache


# Auto procesim
@background(schedule=0)
def matrix_vlersim_per_perdorues(user_id):
    print(f'Para: {globals.VLERSIM_PER_PERDORUES}')
    globals.VLERSIM_PER_PERDORUES = False
    globals.VLERSIM_PER_PERDORUES_MATRIX = None

    ka_vleresim = Vlersim.objects.filter(perdorues=user_id).exists()
    if not ka_vleresim:
        quit()

    # Marrim Librat nga databaza si queryset edhe i konvertojme ne pandas DataFrame
    liber_queryset = Liber.objects.values_list('titulli', 'autori', 'cmimi', 'img_src', 'iid', 'vlersimi_avg').all()
    kolonat_e_librit = columns = ['titulli', 'autori', 'cmimi', 'img_src', 'iid', 'vlersimi_avg']
    librat_df = pd.DataFrame.from_records(liber_queryset, columns=kolonat_e_librit)

    # Marrim Vlersimit nga databaza si queryset edhe i konvertojme ne pandas DataFrame
    vlersim_queryset = Vlersim.objects.all().values_list('id', 'perdorues_id', 'liber_id', 'vlersimi')
    kolonat_e_vlersimit = ['id', 'perdorues_id', 'liber_id', 'vlersimi']
    vlersimi_df = pd.DataFrame.from_records(vlersim_queryset, columns=kolonat_e_vlersimit)

    # Filtrojme Vlersimi_df duke hequr entryt me vlersim 0
    vlersimi_df = vlersimi_df[vlersimi_df.vlersimi != 0]

    vlersim_per_perdorues_series = vlersimi_df.groupby('perdorues_id')['vlersimi'].count()

    vlersim_per_liber_series = vlersimi_df.groupby('liber_id')['vlersimi'].count()

    """Zvogelojme numrin e entrys duke hequr librat qe jane  vlersuar nga pak perdorues"""
    # numerimi i vlersimeve per liber
    vlersim_per_Liber_df = pd.DataFrame(vlersim_per_liber_series)
    # hiq if < 175 vlersime
    filtered_vlersime_per_liber_df = vlersim_per_Liber_df[vlersim_per_Liber_df.vlersimi >= 175]
    # lista e librave qe na nevojiten
    libra_popullor = filtered_vlersime_per_liber_df.index.tolist()

    """ Zvogelojme sipas perdoruesve qe nuk kan vlersuar shume libra"""
    # numerimi i vlersimeve per perdorues
    vlersime_per_perdorues_df = pd.DataFrame(vlersim_per_perdorues_series)
    # hiq if vlersimet < 200
    filtered_vlersime_per_perdorues_df = vlersime_per_perdorues_df[vlersime_per_perdorues_df.vlersimi >= 200]
    # lista ku mbajme perdorues_id qe na nevojiten
    prolific_users = filtered_vlersime_per_perdorues_df.index.tolist()

    """ Heqim nga vlersimet librat dhe perdoruest qe nuk jane ne listat me lart"""
    vlersimet_filtered = vlersimi_df[vlersimi_df.perdorues_id.isin(prolific_users)]

    """ Matrica e vlersimit mes perdorueseve dhe librave"""
    vlersim_matrix = vlersimet_filtered.pivot_table(index='perdorues_id', columns='liber_id', values='vlersimi')
    # replace NaN values with 0
    vlersim_matrix = vlersim_matrix.fillna(0)

    globals.VLERSIM_PER_PERDORUES = True
    globals.VLERSIM_PER_PERDORUES_MATRIX = vlersim_matrix
    # globals.LIBRAT_DF = librat_df

    # vlersim_matrix, librat_df = globals.VLERSIM_PER_PERDORUES_MATRIX
    perdoruesi_loguar = user_id
    perdoruesit_e_ngjashem = perdorues_te_ngjashem(perdoruesi_loguar, vlersim_matrix)
    libra_te_rekomaduar_ids = rekomando_liber(perdoruesi_loguar, perdoruesit_e_ngjashem, vlersim_matrix, librat_df)
    libra_te_rekomaduar = libra_te_rekomaduar_ids
    print(f'Pas: {globals.VLERSIM_PER_PERDORUES}')
    print('________________________________')
    print(libra_te_rekomaduar)
    print('________________________________')
    globals.LIBRA_TE_REKOMANDUAR = libra_te_rekomaduar

    cache = Cache.objects.create(librat_to_string=str(libra_te_rekomaduar))

    # quit()


def perdorues_te_ngjashem(perdorues_id, matrix, x=4):
    # Krijojme nje DF me perdoruesin e loguar
    perdorues_aktual = matrix[matrix.index == perdorues_id]

    # dhe nje DF me perdoruesit e tjere
    perdorues_te_tjere = matrix[matrix.index != perdorues_id]

    # logarisim cosine similarity mes perdoruesit te loguar  dhe te tjereve
    ngjashmerite = cosine_similarity(perdorues_aktual, perdorues_te_tjere)[0].tolist()

    # lista me id e perdorueseve te tjere
    indekset = perdorues_te_tjere.index.tolist()

    # krijojme cifte key/values  te indexit te perdoruesit dhe  te ngjashmeve te tije
    ngjashmeri_indeks = dict(zip(indekset, ngjashmerite))

    # sort by ngjashmeri
    index_similarity_sorted = sorted(ngjashmeri_indeks.items(), key=operator.itemgetter(1))
    index_similarity_sorted.reverse()

    # marrim var x per te nxjerre sa perdorues te ngjashem duam
    perdoruesit_me_te_ngjashem = index_similarity_sorted[:x]
    perdorues_list = [u[0] for u in perdoruesit_me_te_ngjashem]

    return perdorues_list


def rekomando_liber(perdoruesi_loguar, perdoruesit_e_ngjashem, vlersim_matrix, liberat_df, nr_libra_te_sygjeruar=10):
    # load vectors per perdoruesit e ngjashem
    perdorues_te_ngjashem_ = vlersim_matrix[vlersim_matrix.index.isin(perdoruesit_e_ngjashem)]
    # llogarisim avg e vlersimit mes perdoruesve te ngjashem
    perdorues_te_ngjashem_ = perdorues_te_ngjashem_.mean(axis=0)
    # convert to dataframe so its easy to sort and filter
    # konvertojme ne dataFrame sepse eshte me e lehte te filtrohet dhe renditet
    perdorues_te_ngjashem__df = pd.DataFrame(perdorues_te_ngjashem_, columns=['mean'])

    # load vector per perdoruesin e loguar
    perdorues_loguar_df = vlersim_matrix[vlersim_matrix.index == perdoruesi_loguar]
    # Transpozojme serine, sepse eshte me e lehte per te filtruar
    perdorues_loguar_df_transpose = perdorues_loguar_df.transpose()

    # riemerojme kolonen si 'vlersime'
    perdorues_loguar_df_transpose.columns = ['vlersime']

    # Fheqim rreshta pa nje vlere 0. Libra te pa lecuar akoma
    perdorues_loguar_df_transpose = perdorues_loguar_df_transpose[perdorues_loguar_df_transpose['vlersime'] == 0]

    # Gjenerojme nje list me libra te pa lexuar nga perdoruesi
    libra_te_palexuar = perdorues_loguar_df_transpose.index.tolist()

    # rendisim DataFramen
    perdorues_ngjashem_df_renditur = perdorues_te_ngjashem__df.sort_values(by=['mean'], ascending=False)
    # Marrim 'nr_libra_te_sygjeruar' nga koka
    top_libra = perdorues_ngjashem_df_renditur.head(nr_libra_te_sygjeruar)
    ids_libra_top = top_libra.index.tolist()
    # # lookup these anime in the other dataframe to find names
    # anime_information = liberat_df[liberat_df['iid'].isin(ids_libra_top)]

    return ids_libra_top  # items

# Auto procesim
@background(schedule=1000)
def clean_cache():
    Cache.objects.all().delete()
