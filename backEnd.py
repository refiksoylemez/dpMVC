import uyariListesi as durum
covidGlobalListe = list()
def covidOlustur(ulke, vaka, gun):
    global covidGlobalListe
    results = list(filter(lambda x: x['ulke'] == ulke, covidGlobalListe))
    if results:
        raise durum.CovidKayitliUyarisi('Ekleme Hatası! Veri Tabanında "{}" ile Eşleşen En Az Bir Kayıt Bulundu.'.format(ulke))
    else:
        covidGlobalListe.append({'ulke': ulke, 'vaka': vaka, 'gun': gun})
def covidListeOlustur(app_items):
    global covidGlobalListe
    covidGlobalListe = app_items
def covidOku(ulke):
    global covidGlobalListe
    myitems = list(filter(lambda x: x['ulke'] == ulke, covidGlobalListe))
    if myitems:
        return myitems[0]
    else:
        raise durum.CovidKayitliDegilUyarisi(
            'Listeleme Hatası! Veri Tabanında "{}" ile Eşleşen Herhangi Bir Kayıt Bulunamadı.'.format(ulke))
def covidListeOku():
    global covidGlobalListe
    return [item for item in covidGlobalListe]
def covidDegistir(ulke, vaka, gun):
    global covidGlobalListe
    idxs_items = list(
        filter(lambda i_x: i_x[1]['ulke'] == ulke, enumerate(covidGlobalListe)))
    if idxs_items:
        i, item_to_update = idxs_items[0][0], idxs_items[0][1]
        covidGlobalListe[i] = {'ulke': ulke, 'vaka': vaka, 'gun': gun}
    else:
        raise durum.CovidKayitliDegilUyarisi(
            'Güncelleme Hatası! Veri Tabanında "{}" ile Eşleşen Herhangi Bir Kayıt Bulunamadı.'.format(ulke))
def covidSil(ulke):
    global covidGlobalListe
    idxs_items = list(
        filter(lambda i_x: i_x[1]['ulke'] == ulke, enumerate(covidGlobalListe)))
    if idxs_items:
        i, item_to_delete = idxs_items[0][0], idxs_items[0][1]
        del covidGlobalListe[i]
    else:
        raise durum.CovidKayitliDegilUyarisi(
            'Silme Hatası! Veri Tabanında "{}" ile Eşleşen Herhangi Bir Kayıt Bulunamadı.'.format(ulke))
