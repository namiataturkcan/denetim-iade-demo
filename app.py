import streamlit as st


# =========================================================
# SAYFA AYARI
# =========================================================
st.set_page_config(
    page_title="İade Yazısı Gövdesi Üretici",
    layout="wide"
)


# =========================================================
# BASİT ŞİFRE KONTROLÜ
# =========================================================
def demo_sifresini_getir() -> str:
    """
    Streamlit Cloud'da DEMO_PASSWORD secret'ı tanımlanmışsa onu kullanır.
    Tanımlı değilse geçici varsayılan şifreyi kullanır.
    """
    try:
        return st.secrets.get("DEMO_PASSWORD", "denetim2026")
    except Exception:
        return "denetim2026"


def sifre_kontrolu():
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    if st.session_state.authenticated:
        return

    st.title("İade Yazısı Gövdesi Üretici")
    st.info("Demo uygulamasına erişmek için şifre giriniz.")

    girilen_sifre = st.text_input("Demo şifresi", type="password")

    if st.button("Giriş"):
        if girilen_sifre == demo_sifresini_getir():
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("Şifre hatalı.")

    st.stop()


sifre_kontrolu()


# =========================================================
# İADE METNİ ÜRETİCİ YARDIMCI FONKSİYONLAR
# =========================================================
MADDE_SECENEKLERI = [
    "TBMM İçtüzüğü’nün 67’nci maddesi",
    "TBMM İçtüzüğü’nün 96’ncı maddesi",
    "TBMM İçtüzüğü’nün 97’nci maddesi",
    "Anayasa’nın 138’inci maddesi",
]

MADDE_KISA_ADLARI = {
    "TBMM İçtüzüğü’nün 67’nci maddesi": "İçtüzük 67",
    "TBMM İçtüzüğü’nün 96’ncı maddesi": "İçtüzük 96",
    "TBMM İçtüzüğü’nün 97’nci maddesi": "İçtüzük 97",
    "Anayasa’nın 138’inci maddesi": "Anayasa 138",
}


def madde_kisa_adi(madde: str) -> str:
    return MADDE_KISA_ADLARI.get(madde, madde)


# Giriş kısmında 97 seçilemez.
GIRIS_MADDE_SECENEKLERI = [
    "TBMM İçtüzüğü’nün 67’nci maddesi",
    "TBMM İçtüzüğü’nün 96’ncı maddesi",
    "Anayasa’nın 138’inci maddesi",
]

# 97 yalnızca soru kısmında seçilebilir.
SORU_MADDE_SECENEKLERI = [
    "TBMM İçtüzüğü’nün 67’nci maddesi",
    "TBMM İçtüzüğü’nün 96’ncı maddesi",
    "TBMM İçtüzüğü’nün 97’nci maddesi",
    "Anayasa’nın 138’inci maddesi",
]

# Önergenin tamamı bakımından 97 seçeneği şimdilik kapalı.
TAMAMI_MADDE_SECENEKLERI = [
    "TBMM İçtüzüğü’nün 67’nci maddesi",
    "TBMM İçtüzüğü’nün 96’ncı maddesi",
    "Anayasa’nın 138’inci maddesi",
]


MADDE_BILGILERI = {
    "TBMM İçtüzüğü’nün 67’nci maddesi": {
        "tur": "İçtüzük",
        "duzenleme": "TBMM İçtüzüğü’nün",
        "madde": "67’nci",
        "sira": 1,
    },
    "TBMM İçtüzüğü’nün 96’ncı maddesi": {
        "tur": "İçtüzük",
        "duzenleme": "TBMM İçtüzüğü’nün",
        "madde": "96’ncı",
        "sira": 2,
    },
    "TBMM İçtüzüğü’nün 97’nci maddesi": {
        "tur": "İçtüzük",
        "duzenleme": "TBMM İçtüzüğü’nün",
        "madde": "97’nci",
        "sira": 3,
    },
    "Anayasa’nın 138’inci maddesi": {
        "tur": "Anayasa",
        "duzenleme": "Anayasa’nın",
        "madde": "138’inci",
        "sira": 4,
    },
}


MADDE_ACIKLAMA_PARAGRAFLARI = {
    "TBMM İçtüzüğü’nün 67’nci maddesi": (
        "TBMM İçtüzüğü’nün 67’nci maddesinin ikinci fıkrasında “Başkanlığa gelen yazı ve "
        "önergelerde kaba ve yaralayıcı sözler varsa, Başkan, gereken düzeltmelerin yapılması için, "
        "o yazı veya önergeyi sahibine geri verir.” kuralına yer verilmiştir. Bu çerçevede Türkiye Büyük "
        "Millet Meclisi Başkanlığı’na sunulan Meclis araştırması önergeleri ile yazılı soru önergelerinde "
        "toplumun bir kesimi veya tamamı yahut belirli kişi veya kişiler yönünden yaralayıcı olabilecek "
        "ifadelerin bulunması durumunda önergenin, söz konusu ifadelerin düzeltilmesi için TBMM Başkanı "
        "tarafından sahibine iadesi gerekmektedir."
    ),
    "TBMM İçtüzüğü’nün 96’ncı maddesi": (
        "TBMM İçtüzüğü’nün “Yazılı soru” başlıklı 96’ncı maddesinde “Yazılı soru, … kişisel "
        "görüş ileri sürülmeksizin; … bir önerge ile yazılı olarak cevaplanmak üzere milletvekillerinin, "
        "Cumhurbaşkanı yardımcıları ve bakanlara yazılı olarak soru sormalarından ibarettir.” "
        "kuralına yer verilmiş olup; bu madde uyarınca yazılı soru önergesi metninde önerge sahibi "
        "milletvekilinin kişisel görüşlerine yer verilmemesi gerekmektedir."
    ),
    "TBMM İçtüzüğü’nün 97’nci maddesi": (
        "TBMM İçtüzüğü’nün “Sorulamayacak konular” başlıklı 97’nci maddesi “Aşağıdaki "
        "sorular Başkanlıkça kabul edilmez: … b) Tek amacı istişare sağlamaktan ibaret konular” "
        "hükmünü içermektedir. Bu maddede yazılı soru önergelerinde sadece belli bir konu hakkında "
        "istişarî amaçla sorulan soruların Başkanlıkça kabul edilemeyeceği hükme bağlanmıştır."
    ),
    "Anayasa’nın 138’inci maddesi": (
        "Anayasa’nın 138’inci maddesinin üçüncü fıkrasında “Görülmekte olan bir dava hakkında "
        "Yasama Meclisinde yargı yetkisinin kullanılması ile ilgili soru sorulamaz, görüşme yapılamaz "
        "veya herhangi bir beyanda bulunulamaz.” hükmüne yer verilmiştir. Bu hüküm uyarınca "
        "görülmekte olan bir dava hakkında yargı yetkisinin kullanılmasına ilişkin nitelikteki soruların "
        "yazılı soru önergesine konu edilmemesi gerekmektedir."
    ),
}


STANDART_ACIKLAMA_PARAGRAFI = (
    "Türkiye Büyük Millet Meclisi (TBMM) İçtüzüğü’nün 67’nci ve 96’ncı maddeleri "
    "uyarınca TBMM Başkanlığı’na sunulan yazılı soru önergeleri Anayasa ve İçtüzük "
    "hükümlerine uygunluk noktasında TBMM Başkanlığı’nca incelenmekte ve yapılan "
    "değerlendirme sonucunda işleme alınarak gelen kâğıtlar listesinde yayımlanmakta veya "
    "sahibine iade edilmektedir."
)


SIRA_SOZLUGU = {
    1: "birinci",
    2: "ikinci",
    3: "üçüncü",
    4: "dördüncü",
    5: "beşinci",
    6: "altıncı",
    7: "yedinci",
    8: "sekizinci",
    9: "dokuzuncu",
    10: "onuncu",
    11: "on birinci",
    12: "on ikinci",
    13: "on üçüncü",
    14: "on dördüncü",
    15: "on beşinci",
    16: "on altıncı",
    17: "on yedinci",
    18: "on sekizinci",
    19: "on dokuzuncu",
    20: "yirminci",
    21: "yirmi birinci",
    22: "yirmi ikinci",
    23: "yirmi üçüncü",
    24: "yirmi dördüncü",
    25: "yirmi beşinci",
    26: "yirmi altıncı",
    27: "yirmi yedinci",
    28: "yirmi sekizinci",
    29: "yirmi dokuzuncu",
    30: "otuzuncu",
    31: "otuz birinci",
    32: "otuz ikinci",
    33: "otuz üçüncü",
    34: "otuz dördüncü",
    35: "otuz beşinci",
    36: "otuz altıncı",
    37: "otuz yedinci",
    38: "otuz sekizinci",
    39: "otuz dokuzuncu",
    40: "kırkıncı",
    41: "kırk birinci",
    42: "kırk ikinci",
    43: "kırk üçüncü",
    44: "kırk dördüncü",
    45: "kırk beşinci",
    46: "kırk altıncı",
    47: "kırk yedinci",
    48: "kırk sekizinci",
    49: "kırk dokuzuncu",
    50: "ellinci",
}


def sira_sozu(sayi: int) -> str:
    return SIRA_SOZLUGU.get(int(sayi), f"{sayi}.")


def turkce_liste(items, baglac="ve") -> str:
    items = [str(item) for item in items if str(item).strip()]

    if not items:
        return ""

    if len(items) == 1:
        return items[0]

    if len(items) == 2:
        return f"{items[0]} {baglac} {items[1]}"

    return f"{', '.join(items[:-1])} {baglac} {items[-1]}"


def maddeleri_sirala(maddeler: list) -> list:
    temiz = []
    for madde in maddeler:
        if madde in MADDE_BILGILERI and madde not in temiz:
            temiz.append(madde)

    return sorted(temiz, key=lambda m: MADDE_BILGILERI[m]["sira"])


def madde_yonelme_ifadesi(maddeler: list) -> str:
    """
    Örn:
    - TBMM İçtüzüğü’nün 96’ncı maddesi hükmüne
    - TBMM İçtüzüğü’nün 96’ncı ve 97’nci maddeleri hükümlerine
    """

    maddeler = maddeleri_sirala(maddeler)

    if not maddeler:
        return "ilgili mevzuat hükmüne"

    bilgiler = [MADDE_BILGILERI[m] for m in maddeler]
    turler = set(b["tur"] for b in bilgiler)

    if len(turler) == 1:
        duzenleme = bilgiler[0]["duzenleme"]
        madde_sirasi = [b["madde"] for b in bilgiler]

        if len(madde_sirasi) == 1:
            return f"{duzenleme} {madde_sirasi[0]} maddesi hükmüne"

        return f"{duzenleme} {turkce_liste(madde_sirasi)} maddeleri hükümlerine"

    tekil_ifadeler = []
    for b in bilgiler:
        tekil_ifadeler.append(f"{b['duzenleme']} {b['madde']} maddesi")

    return f"{turkce_liste(tekil_ifadeler)} hükümlerine"


def sonuc_hukum_ifadesi(maddeler: list) -> str:
    """
    Son cümledeki:
    - İçtüzük hükmüne
    - İçtüzük hükümlerine
    - Anayasa hükmüne
    - ilgili mevzuat hükümlerine
    kısmını üretir.
    """

    maddeler = maddeleri_sirala(maddeler)

    if not maddeler:
        return "ilgili mevzuat hükmüne"

    bilgiler = [MADDE_BILGILERI[m] for m in maddeler]
    turler = set(b["tur"] for b in bilgiler)

    if turler == {"İçtüzük"}:
        if len(set(maddeler)) == 1:
            return "İçtüzük hükmüne"
        return "İçtüzük hükümlerine"

    if turler == {"Anayasa"}:
        if len(set(maddeler)) == 1:
            return "Anayasa hükmüne"
        return "Anayasa hükümlerine"

    return "ilgili mevzuat hükümlerine"


def giris_grubu_ifadesi(entries: list) -> str:
    """
    Giriş kısmı için daha doğal ifade üretir.

    Örn:
    - giriş kısmının üçüncü paragrafının
    - giriş kısmının üçüncü paragrafının birinci ve ikinci cümlelerinin
    - giriş kısmının üçüncü paragrafı ile yedinci paragrafının üçüncü cümlesinin
    """

    if not entries:
        return ""

    # Paragrafa göre grupla, giriş sırasını koru.
    paragraf_gruplari = []
    for entry in entries:
        bulundu = False
        for grup in paragraf_gruplari:
            if grup["paragraf"] == entry["paragraf"]:
                grup["entries"].append(entry)
                bulundu = True
                break

        if not bulundu:
            paragraf_gruplari.append({
                "paragraf": entry["paragraf"],
                "entries": [entry],
            })

    ifadeler = []

    for index, grup in enumerate(paragraf_gruplari):
        paragraf = sira_sozu(grup["paragraf"])
        prefix = "giriş kısmının " if index == 0 else ""
        terminal = index == len(paragraf_gruplari) - 1

        if any(e.get("cumle") is None for e in grup["entries"]):
            if terminal:
                ifade = f"{prefix}{paragraf} paragrafının"
            else:
                ifade = f"{prefix}{paragraf} paragrafı"

            ifadeler.append(ifade)
            continue

        cumleler = sorted(set(int(e["cumle"]) for e in grup["entries"]))
        cumle_sozleri = [sira_sozu(c) for c in cumleler]

        if len(cumleler) == 1:
            if terminal:
                ifade = f"{prefix}{paragraf} paragrafının {cumle_sozleri[0]} cümlesinin"
            else:
                ifade = f"{prefix}{paragraf} paragrafının {cumle_sozleri[0]} cümlesi"
        else:
            if terminal:
                ifade = f"{prefix}{paragraf} paragrafının {turkce_liste(cumle_sozleri)} cümlelerinin"
            else:
                ifade = f"{prefix}{paragraf} paragrafının {turkce_liste(cumle_sozleri)} cümleleri"

        ifadeler.append(ifade)

    return turkce_liste(ifadeler, baglac="ile")


def soru_grubu_ifadesi(entries: list) -> str:
    soru_numaralari = sorted(set(int(e["soru_no"]) for e in entries))

    if len(soru_numaralari) == 1:
        return f"{soru_numaralari[0]} numaralı sorusunun"

    return f"{turkce_liste(soru_numaralari)} numaralı sorularının"


def entries_maddelerine_gore_grupla(entries: list) -> list:
    """
    Sorunlu yerleri tip ve madde kombinasyonuna göre gruplar.
    Örn:
    - Giriş kısmı / 96
    - Soru kısmı / 96+97
    """

    gruplar = []

    for entry in entries:
        sirali_maddeler = tuple(maddeleri_sirala(entry["maddeler"]))
        anahtar = (entry["tip"], sirali_maddeler)

        bulundu = False
        for grup in gruplar:
            if grup["anahtar"] == anahtar:
                grup["entries"].append(entry)
                bulundu = True
                break

        if not bulundu:
            gruplar.append({
                "anahtar": anahtar,
                "tip": entry["tip"],
                "maddeler": list(sirali_maddeler),
                "entries": [entry],
            })

    return gruplar


def sorunlu_kisimler_cumlesi_uret(entries: list) -> str:
    """
    Ana değerlendirme cümlesindeki sorunlu kısım + hüküm bölümünü üretir.
    """

    gruplar = entries_maddelerine_gore_grupla(entries)

    cumle_parcalari = []

    for index, grup in enumerate(gruplar):
        tip = grup["tip"]
        maddeler = grup["maddeler"]

        if tip == "giris":
            ifade = giris_grubu_ifadesi(grup["entries"])
        else:
            ifade = soru_grubu_ifadesi(grup["entries"])

        hukum_ifadesi = madde_yonelme_ifadesi(maddeler)

        if index == 0:
            parca = f"{ifade} yukarıda aktarılan {hukum_ifadesi} aykırılık taşıdığı"
        else:
            parca = f"{ifade} ise yukarıda aktarılan {hukum_ifadesi} aykırılık taşıdığı"

        cumle_parcalari.append(parca)

    return "; ".join(cumle_parcalari)


def sonuc_nesnesi_uret(entries: list) -> str:
    """
    Sonuç cümlesindeki:
    - söz konusu kısım
    - söz konusu kısımlar
    - söz konusu soru
    - söz konusu sorular
    - söz konusu kısımlar ve soru
    gibi ifadeleri üretir.
    """

    giris_entries = [e for e in entries if e["tip"] == "giris"]
    soru_entries = [e for e in entries if e["tip"] == "soru"]

    giris_sayisi = len(giris_entries)
    soru_sayisi = len(set(int(e["soru_no"]) for e in soru_entries))

    if giris_sayisi > 0 and soru_sayisi > 0:
        kisim_ifadesi = "kısım" if giris_sayisi == 1 else "kısımlar"
        soru_ifadesi = "soru" if soru_sayisi == 1 else "sorular"
        return f"söz konusu {kisim_ifadesi} ve {soru_ifadesi}"

    if giris_sayisi > 0:
        return "söz konusu kısım" if giris_sayisi == 1 else "söz konusu kısımlar"

    if soru_sayisi > 0:
        return "söz konusu soru" if soru_sayisi == 1 else "söz konusu sorular"

    return "söz konusu kısım"


def tum_maddeleri_topla(entries: list) -> list:
    maddeler = []

    for entry in entries:
        for madde in entry["maddeler"]:
            if madde not in maddeler:
                maddeler.append(madde)

    return maddeleri_sirala(maddeler)


def esas_iade_paragrafi_uret(
    oner_sayisi: str,
    tamami_iade: bool,
    entries: list,
    tamami_maddeler: list,
    ek_aciklama: str = ""
) -> str:
    """
    Sadece esas iade değerlendirme paragrafını üretir.
    """

    if oner_sayisi == "Tek önerge":
        incelenen = "önergeniz incelenmiş"
        sahiplik = "önergenizin"
        sonuc_ozne = "önergeniz"
    else:
        incelenen = "önergeleriniz incelenmiş"
        sahiplik = "önergelerinizin"
        sonuc_ozne = "önergeleriniz"

    ek_aciklama = ek_aciklama.strip()

    if tamami_iade:
        hukum_ifadesi = madde_yonelme_ifadesi(tamami_maddeler)
        sonuc_hukum = sonuc_hukum_ifadesi(tamami_maddeler)

        metin = (
            f"Bu çerçevede ilgide kayıtlı {incelenen} ve {sahiplik} tamamının "
            f"yukarıda aktarılan {hukum_ifadesi} aykırılık taşıdığı değerlendirilmiştir. "
        )

        if ek_aciklama:
            metin += f"{ek_aciklama} "

        metin += (
            f"Dolayısıyla {sonuc_ozne}, yukarıda belirtilen {sonuc_hukum} uygun olarak "
            f"yeniden düzenlendiği takdirde işleme alınabilecektir."
        )

        return metin

    if not entries:
        return (
            "Henüz sorunlu kısım eklenmedi. Giriş kısmı veya soru kısmı seçilerek en az bir sorunlu yer eklenmelidir."
        )

    sorunlu_kisim_cumlesi = sorunlu_kisimler_cumlesi_uret(entries)
    sonuc_nesnesi = sonuc_nesnesi_uret(entries)
    maddeler = tum_maddeleri_topla(entries)
    sonuc_hukum = sonuc_hukum_ifadesi(maddeler)

    metin = (
        f"Bu çerçevede ilgide kayıtlı {incelenen} ve {sahiplik} "
        f"{sorunlu_kisim_cumlesi} değerlendirilmiştir. "
    )

    if ek_aciklama:
        metin += f"{ek_aciklama} "

    metin += (
        f"Dolayısıyla {sonuc_ozne}, {sonuc_nesnesi} çıkarıldığı veya yukarıda belirtilen "
        f"{sonuc_hukum} uygun olarak yeniden düzenlendiği takdirde işleme alınabilecektir."
    )

    return metin


def madde_aciklama_paragraflarini_uret(maddeler: list) -> list:
    """
    Seçilen maddelere göre 67/96/97/138 açıklama paragraflarını üretir.
    """

    maddeler = maddeleri_sirala(maddeler)
    paragraflar = []

    for madde in maddeler:
        paragraf = MADDE_ACIKLAMA_PARAGRAFLARI.get(madde)
        if paragraf:
            paragraflar.append(paragraf)

    return paragraflar


def yazi_govdesi_uret(esas_paragraf: str, maddeler: list) -> str:
    """
    EBYS antet/sayı/ilgi/imza kısımları hariç yazı gövdesini üretir.
    """

    paragraflar = []

    paragraflar.append(STANDART_ACIKLAMA_PARAGRAFI)

    madde_paragraflari = madde_aciklama_paragraflarini_uret(maddeler)
    paragraflar.extend(madde_paragraflari)

    paragraflar.append(esas_paragraf)

    paragraflar.append("Bilgilerinizi rica ederim.")

    return "\n\n".join(paragraflar)


# =========================================================
# ARAYÜZ
# =========================================================
st.title("İade Yazısı Gövdesi Üretici")

st.info(
    "Bu demo uygulama yalnızca iade yazısı gövdesini üretir. "
    "Gerçek önerge PDF'i yüklenmez; EBYS antet, sayı, konu, ilgi, imza ve ek kısımları üretilmez."
)

if "giris_sayisi" not in st.session_state:
    st.session_state.giris_sayisi = 1

if "soru_sayisi" not in st.session_state:
    st.session_state.soru_sayisi = 1

st.subheader("1. Genel seçimler")

col1, col2 = st.columns(2)

with col1:
    oner_sayisi = st.radio(
        "Önerge sayısı",
        ["Tek önerge", "Birden fazla önerge"],
        horizontal=True
    )

with col2:
    tamami_iade = st.checkbox(
        "Önergenin tamamı iade edilecek",
        value=False,
        help="Bu seçenek işaretlenirse giriş ve soru kısmı seçimleri kapatılır."
    )

entries = []
tamami_maddeler = []

if tamami_iade:
    st.warning(
        "Önergenin tamamı seçildiği için giriş kısmı ve soru kısmı alanları devre dışı bırakıldı."
    )

    tamami_maddeler = st.multiselect(
        "Önergenin tamamı için ilgili hüküm/hükümler",
        TAMAMI_MADDE_SECENEKLERI,
        default=["TBMM İçtüzüğü’nün 96’ncı maddesi"],
        format_func=madde_kisa_adi
    )

else:
    sorunlu_bolumler = st.multiselect(
        "Sorunlu bölüm/bölümler",
        ["Giriş kısmı", "Soru kısmı"],
        default=["Giriş kısmı"]
    )

    if "Giriş kısmı" in sorunlu_bolumler:
        st.subheader("2. Giriş kısmındaki sorunlu yerler")

        c1, c2 = st.columns([1, 1])

        with c1:
            if st.button("➕ Giriş kısmı için yeni sorunlu yer ekle"):
                st.session_state.giris_sayisi += 1

        with c2:
            if st.button("Giriş kısmı satırlarını sıfırla"):
                st.session_state.giris_sayisi = 1

        for i in range(st.session_state.giris_sayisi):
            with st.expander(f"Giriş kısmı - {i + 1}. sorunlu yer", expanded=True):
                col_a, col_b, col_c = st.columns(3)

                with col_a:
                    paragraf = st.number_input(
                        "Paragraf numarası",
                        min_value=1,
                        max_value=50,
                        value=1,
                        step=1,
                        key=f"giris_paragraf_{i}"
                    )

                with col_b:
                    cumle_turu = st.radio(
                        "Kapsam",
                        ["Paragrafın tamamı", "Belirli cümle"],
                        horizontal=False,
                        key=f"giris_cumle_turu_{i}"
                    )

                with col_c:
                    if cumle_turu == "Belirli cümle":
                        cumle = st.number_input(
                            "Cümle numarası",
                            min_value=1,
                            max_value=30,
                            value=1,
                            step=1,
                            key=f"giris_cumle_{i}"
                        )
                    else:
                        cumle = None

                maddeler = st.multiselect(
                    "Bu sorunlu yer için ilgili hüküm/hükümler",
                    GIRIS_MADDE_SECENEKLERI,
                    default=["TBMM İçtüzüğü’nün 96’ncı maddesi"],
                    key=f"giris_maddeler_{i}",
                    format_func=madde_kisa_adi
                )

                if maddeler:
                    entries.append({
                        "tip": "giris",
                        "paragraf": int(paragraf),
                        "cumle": int(cumle) if cumle is not None else None,
                        "maddeler": maddeler,
                    })

    if "Soru kısmı" in sorunlu_bolumler:
        st.subheader("3. Soru kısmındaki sorunlu yerler")

        c1, c2 = st.columns([1, 1])

        with c1:
            if st.button("➕ Soru kısmı için yeni sorunlu soru ekle"):
                st.session_state.soru_sayisi += 1

        with c2:
            if st.button("Soru kısmı satırlarını sıfırla"):
                st.session_state.soru_sayisi = 1

        for i in range(st.session_state.soru_sayisi):
            with st.expander(f"Soru kısmı - {i + 1}. sorunlu soru", expanded=True):
                col_a, col_b = st.columns(2)

                with col_a:
                    soru_no = st.number_input(
                        "Soru numarası",
                        min_value=1,
                        max_value=100,
                        value=1,
                        step=1,
                        key=f"soru_no_{i}"
                    )

                with col_b:
                    maddeler = st.multiselect(
                        "Bu soru için ilgili hüküm/hükümler",
                        SORU_MADDE_SECENEKLERI,
                        default=[
                            "TBMM İçtüzüğü’nün 96’ncı maddesi",
                            "TBMM İçtüzüğü’nün 97’nci maddesi"
                        ],
                        key=f"soru_maddeler_{i}",
                        format_func=madde_kisa_adi
                    )

                if maddeler:
                    entries.append({
                        "tip": "soru",
                        "soru_no": int(soru_no),
                        "maddeler": maddeler,
                    })

st.subheader("4. Ek açıklama")

ek_aciklama = st.text_area(
    "Ek açıklama cümlesi, isteğe bağlı",
    height=80,
    placeholder="Gerekirse esas iade değerlendirme paragrafına ilave edilecek açıklamayı yazabilirsiniz. Boş bırakılabilir."
)

if tamami_iade:
    kullanilan_maddeler = maddeleri_sirala(tamami_maddeler)
else:
    kullanilan_maddeler = tum_maddeleri_topla(entries)

esas_paragraf = esas_iade_paragrafi_uret(
    oner_sayisi=oner_sayisi,
    tamami_iade=tamami_iade,
    entries=entries,
    tamami_maddeler=tamami_maddeler,
    ek_aciklama=ek_aciklama
)

yazi_govdesi = yazi_govdesi_uret(
    esas_paragraf=esas_paragraf,
    maddeler=kullanilan_maddeler
)

st.subheader("5. Üretilen Yazı Gövdesi")

st.text_area("Yazı gövdesi", yazi_govdesi, height=500)

st.download_button(
    label="Yazı gövdesini TXT olarak indir",
    data=yazi_govdesi,
    file_name="iade_yazisi_govdesi.txt",
    mime="text/plain"
)

with st.expander("Sadece esas iade değerlendirme paragrafını göster"):
    st.text_area("Esas iade değerlendirme paragrafı", esas_paragraf, height=180)

st.warning(
    "Not: Bu metin taslaktır. EBYS’ye aktarılmadan önce ilgili önerge, madde gerekçesi "
    "ve Başkanlık uygulaması bakımından uzman/yönetici tarafından kontrol edilmelidir."
)
