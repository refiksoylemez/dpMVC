import backEnd
import uyariListesi as durum

class ModelBasic(object):

    def __init__(self, covidModel):
        self._item_type = 'covid19'
        self.covidListeOlustur(covidModel)

    @property
    def item_type(self):
        return self._item_type

    @item_type.setter
    def item_type(self, covidYeniTip):
        self._item_type = covidYeniTip

    def covidOlustur(self, ulke, vaka, gun):
        backEnd.covidOlustur(ulke, vaka, gun)

    def covidListeOlustur(self, items):
        backEnd.covidListeOlustur(items)

    def covidOku(self, ulke):
        return backEnd.covidOku(ulke)

    def covidListeOku(self):
        return backEnd.covidListeOku()

    def covidDegistir(self, ulke, vaka, gun):
        backEnd.covidDegistir(ulke, vaka, gun)

    def covidSil(self, ulke):
        backEnd.covidSil(ulke)
class View(object):

    @staticmethod
    def yildizliListeGoster(item_type, items):
        print('=' * 100)
        print('=== {} LİSTE ==='.format(item_type.upper()))
        for item in items:
            print('* {}'.format(item))
        print('=' * 100)

    @staticmethod
    def sayisalListeGoster(item_type, items):
        print('=' * 100)
        print('=== {} LİSTE ==='.format(item_type.upper()))
        for i, item in enumerate(items):
            print('{}. {}'.format(i+1, item))

        print('=' * 100)
    @staticmethod
    def covidGoster(item_type, item, item_info):
        print('='*100)
        print('Tebrikler!, {} Veri Tabanı ile Eşleşti. İşte Bilgiler!'.format(item.upper()))
        print('{} DETAY: {}'.format(item_type.upper(), item_info))
        print('=' * 100)

    @staticmethod
    def covidEksikHataGoster(item, err):
        print('='*100)
        print('Üzgünüm!, Veri Tabanında "{}" ile Eşleşen Herhangi Bir Kayıt Bulunamadı.'.format(item.upper()))
        print('{}'.format(err.args[0]))
        print('='*100)

    @staticmethod
    def covidFazlaHataGoster(item, item_type, err):
        print('='*100)
        print('Üzgünüm!, {} Veri Tabanı Listesinde "{}" ile Eşleşen Zaten Bir Kayıt Var.'
              .format(item_type,item.upper()))
        print('{}'.format(err.args[0]))
        print('='*100)

    @staticmethod
    def covidKayitYokHataGoster(item, item_type, err):
        print('=' * 100)
        print('Üzgünüm!, {} Veri Tabanı Listesinde "{}" ile Eşleşen Herhangi Bir Kayıt Bulunamadı.'
              .format(item_type,item.upper()))
        print('{}'.format(err.args[0]))
        print('=' * 100)

    @staticmethod
    def covidKayitBasariliGoster(item, item_type):
        print('=' * 100)
        print('Tebrikler! {} Veri Tabanı Listesinde "{}" Kaydı Başarı İle Eklendi.'
              .format(item.upper(), item_type))
        print('='*100)

    @staticmethod
    def covidTipGuncellemBasariliGoster(older, newer):
        print('='*100)
        print('Tebrikler!,  Veri Tabanı Listesinde "{}" ile "{}" Kaydı Başarı İle Değiştirildi.'.format(older, newer))
        print('='*100)

    @staticmethod
    def covidIcerikGuncellemBasariliGoster(item, o_vaka, o_gun, n_vaka, n_gun):
        print('='*100)
        print('Tebrikler!, Güncelleme Başarılı. {} Eski Vaka Sayısı: {} Yeni Vaka Sayısı: {}'
              .format(item, o_vaka, n_vaka))
        print('Tebrikler!, Güncelleme Başarılı. {} Eski Gün Sayısı: {} Yeni Gün Sayısı: {}'
              .format(item, o_gun, n_gun))
        print('='*100)

    @staticmethod
    def covidSilmeBasariliGoster(ulke):
        print('=' * 100)
        print('Tebrikler!, "{}" Silme İşlemi Başarılı.'.format(ulke))
        print('='*100)
class Controller(object):

    def __init__(self, model, view):
        self.model = model
        self.view = view

    def covidListeGoster(self, sayisalListe=False):
        items = self.model.covidListeOku()
        item_type = self.model.item_type
        if sayisalListe:
            self.view.yildizliListeGoster(item_type, items)
        else:
            self.view.sayisalListeGoster(item_type, items)

    def covidGoster(self, item_ulke):
        try:
            item = self.model.covidOku(item_ulke)
            item_type = self.model.item_type
            self.view.covidGoster(item_type, item_ulke, item)
        except durum.CovidKayitliDegilUyarisi as e:
            self.view.covidEksikHataGoster(item_ulke, e)

    def covidEkle(self, ulke, vaka, gun):
        assert vaka >= 0, 'VAKA SAYISI EN AZ 0 OLABİLİR'
        assert gun >= 1, 'VAKA SAYISI EN AZ 1 OLABİLİR'
        item_type = self.model.item_type
        try:
            self.model.covidOlustur(ulke, vaka, gun)
            self.view.covidKayitBasariliGoster(ulke, item_type)
        except durum.CovidKayitliUyarisi as e:
            self.view.covidFazlaHataGoster(ulke, item_type, e)

    def covidGuncelle(self, ulke, vaka, gun):
        assert vaka >= 0, 'VAKA SAYISI EN AZ 0 OLABİLİR'
        assert gun >= 1, 'VAKA SAYISI EN AZ 1 OLABİLİR'
        item_type = self.model.item_type

        try:
            self.model.covidDegistir(ulke, vaka, gun)
            older = self.model.covidOku(ulke)
            self.view.covidIcerikGuncellemBasariliGoster(
                ulke, older['vaka'], older['gun'], vaka, gun)
        except durum.CovidKayitliDegilUyarisi as e:
            self.view.covidKayitYokHataGoster(ulke, item_type, e)
            # burada eğer güncellenecek ülke yoksa yeniden ekletedebilrdik

    def covidGuncelle_type(self, covidYeniTip):
        old_item_type = self.model.item_type
        self.model.item_type = covidYeniTip
        self.view.covidTipGuncellemBasariliGoster(old_item_type, covidYeniTip)

    def covidSil(self, ulke):
        item_type = self.model.item_type
        try:
            self.model.covidSil(ulke)
            self.view.covidSilmeBasariliGoster(ulke)
        except durum.CovidKayitliDegilUyarisi as e:
            self.view.covidKayitYokHataGoster(ulke, item_type, e)


if __name__ == "__main__":
    covidDatabase = [
        {'ulke': 'tr', 'vaka': 1500, 'gun': 11},
        {'ulke': 'abd', 'vaka': 20000, 'gun': 55},
        {'ulke': 'de', 'vaka': 2345, 'gun': 22},
    ]

    c = Controller(ModelBasic(covidDatabase), View())
    c.covidListeGoster()
    c.covidListeGoster(sayisalListe=True)
    c.covidGoster('tr')
    c.covidEkle('kktc', vaka=23, gun=5)
    c.covidEkle('kktc', vaka=23, gun=5)
    c.covidGuncelle('tr', vaka=134, gun=22)
    c.covidGuncelle('tr1', vaka=134, gun=22)
    c.covidSil('kktc')
    c.covidSil('nl')


