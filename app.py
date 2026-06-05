import streamlit as st


# =========================================================
# SAYFA AYARI
# =========================================================
st.set_page_config(
    page_title="Yazılı Soru Önergeleri İade Yazısı Hazırlama Aracı",
    layout="wide"
)


# =========================================================
# BASİT ŞİFRE KONTROLÜ
# =========================================================
def demo_sifresini_getir() -> str:
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

    girilen_sifre = st.text_input("Demo Şifresi", type="password")

    if st.button("Giriş"):
        if girilen_sifre == demo_sifresini_getir():
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("Şifre hatalı.")

    st.stop()


sifre_kontrolu()


# =========================================================
# GÖRSEL DÜZENLEME
# =========================================================
st.markdown(
    """
    <style>
    .main {
        background-color: #f7f1fa;
    }

    h1 {
        color: #1f2937;
        font-weight: 700;
        letter-spacing: -0.5px;
    }

    h2, h3 {
        color: #111827;
        font-weight: 650;
    }

    .stAlert {
        border-radius: 12px;
    }

    div[data-testid="stExpander"] {
        border: 1px solid #d1d5db;
        border-radius: 12px;
        background-color: #ffffff;
        margin-bottom: 12px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.06);
    }

    div[data-testid="stExpander"] summary {
        font-weight: 650;
        color: #1f2937;
    }

    .stButton > button {
        border-radius: 10px;
        border: 1px solid #cbd5e1;
        background-color: #ffffff;
        color: #1f2937;
        font-weight: 600;
        padding: 0.45rem 0.8rem;
    }

    .stButton > button:hover {
        border-color: #64748b;
        background-color: #f1f5f9;
        color: #0f172a;
    }

    textarea {
        border-radius: 10px !important;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1200px;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# SABİT VERİLER
# =========================================================
MADDE_SECENEKLERI = [
    "Anayasa’nın 138’inci maddesi",
    "TBMM İçtüzüğü’nün 67’nci maddesi",
    "TBMM İçtüzüğü’nün 96’ncı maddesi",
    "TBMM İçtüzüğü’nün 97’nci maddesi",
]

MADDE_KISA_ADLARI = {
    "Anayasa’nın 138’inci maddesi": "Anayasa 138",
    "TBMM İçtüzüğü’nün 67’nci maddesi": "İçtüzük 67",
    "TBMM İçtüzüğü’nün 96’ncı maddesi": "İçtüzük 96",
    "TBMM İçtüzüğü’nün 97’nci maddesi": "İçtüzük 97",
}


def madde_kisa_adi(madde: str) -> str:
    return MADDE_KISA_ADLARI.get(madde, madde)


GIRIS_MADDE_SECENEKLERI = [
    "Anayasa’nın 138’inci maddesi",
    "TBMM İçtüzüğü’nün 67’nci maddesi",
    "TBMM İçtüzüğü’nün 96’ncı maddesi",
]

SORU_MADDE_SECENEKLERI = [
    "Anayasa’nın 138’inci maddesi",
    "TBMM İçtüzüğü’nün 67’nci maddesi",
    "TBMM İçtüzüğü’nün 96’ncı maddesi",
    "TBMM İçtüzüğü’nün 97’nci maddesi",
]

TAMAMI_MADDE_SECENEKLERI = [
    "Anayasa’nın 138’inci maddesi",
    "TBMM İçtüzüğü’nün 67’nci maddesi",
    "TBMM İçtüzüğü’nün 96’ncı maddesi",
]

MADDE_BILGILERI = {
    "Anayasa’nın 138’inci maddesi": {
        "tur": "Anayasa",
        "duzenleme": "Anayasa’nın",
        "madde": "138’inci",
        "sira": 1,
    },
    "TBMM İçtüzüğü’nün 67’nci maddesi": {
        "tur": "İçtüzük",
        "duzenleme": "TBMM İçtüzüğü’nün",
        "madde": "67’nci",
        "sira": 2,
    },
    "TBMM İçtüzüğü’nün 96’ncı maddesi": {
        "tur": "İçtüzük",
        "duzenleme": "TBMM İçtüzüğü’nün",
        "madde": "96’ncı",
        "sira": 3,
    },
    "TBMM İçtüzüğü’nün 97’nci maddesi": {
        "tur": "İçtüzük",
        "duzenleme": "TBMM İçtüzüğü’nün",
        "madde": "97’nci",
        "sira": 4,
    },
}

IC67_GEREKCE_SECENEKLERI = [
    "Toplumun bir kesimi / belirli kişi veya kişiler yönünden yaralayıcı ifade",
    "Kaba ve yaralayıcı ifade",
    "Kaba ifadeler veya toplumun bir kesimi yönünden yaralayıcı ifade",
]

IC96_GEREKCE_SECENEKLERI = [
    "Kişisel görüş",
    "Kısa ve gerekçesiz olma",
    "Kişilik ve özel yaşama ilişkin konu",
    "Ek belge yasağı",
    "96 tam metin",
]


# =========================================================
# AÇIKLAMA PARAGRAFLARI
# =========================================================
STANDART_ACIKLAMA_PARAGRAFI = (
    "Türkiye Büyük Millet Meclisi (TBMM) İçtüzüğü’nün 67’nci ve 96’ncı maddeleri "
    "uyarınca TBMM Başkanlığı’na sunulan yazılı soru önergeleri Anayasa ve İçtüzük "
    "hükümlerine uygunluk noktasında TBMM Başkanlığı’nca incelenmekte ve yapılan "
    "değerlendirme sonucunda işleme alınarak gelen kâğıtlar listesinde yayımlanmakta veya "
    "sahibine iade edilmektedir."
)

ANAYASA_138_PARAGRAFI = (
    "Anayasa’nın 138’inci maddesinin üçüncü fıkrasında “Görülmekte olan bir dava hakkında "
    "Yasama Meclisinde yargı yetkisinin kullanılması ile ilgili soru sorulamaz, görüşme yapılamaz "
    "veya herhangi bir beyanda bulunulamaz.” hükmüne yer verilmiştir. Bu hüküm uyarınca "
    "görülmekte olan bir dava hakkında yargı yetkisinin kullanılmasına ilişkin nitelikteki soruların "
    "yazılı soru önergesine konu edilmemesi gerekmektedir."
)

IC67_PARAGRAFLARI = {
    "Toplumun bir kesimi / belirli kişi veya kişiler yönünden yaralayıcı ifade": (
        "TBMM İçtüzüğü’nün 67’nci maddesinin ikinci fıkrasında “Başkanlığa gelen yazı ve "
        "önergelerde kaba ve yaralayıcı sözler varsa, Başkan, gereken düzeltmelerin yapılması için, "
        "o yazı veya önergeyi sahibine geri verir.” kuralına yer verilmiştir. Bu çerçevede Türkiye Büyük "
        "Millet Meclisi Başkanlığı’na sunulan Meclis araştırması önergeleri ile yazılı soru önergelerinde "
        "toplumun bir kesimi veya tamamı yahut belirli kişi veya kişiler yönünden yaralayıcı olabilecek "
        "ifadelerin bulunması durumunda önergenin, söz konusu ifadelerin düzeltilmesi için TBMM Başkanı "
        "tarafından sahibine iadesi gerekmektedir."
    ),
    "Kaba ve yaralayıcı ifade": (
        "TBMM İçtüzüğü’nün 67’nci maddesinin ikinci fıkrasında “Başkanlığa gelen yazı ve "
        "önergelerde kaba ve yaralayıcı sözler varsa, Başkan, gereken düzeltmelerin yapılması için, "
        "o yazı veya önergeyi sahibine geri verir.” kuralına yer verilmiştir. Bu çerçevede Türkiye Büyük "
        "Millet Meclisi Başkanlığı’na sunulan Meclis araştırması önergeleri ile yazılı soru önergelerinde "
        "kaba ve yaralayıcı ifadelerin bulunması durumunda önergenin, söz konusu ifadelerin düzeltilmesi "
        "için TBMM Başkanı tarafından sahibine iadesi gerekmektedir."
    ),
    "Kaba ifadeler veya toplumun bir kesimi yönünden yaralayıcı ifade": (
        "TBMM İçtüzüğü’nün 67’nci maddesinin ikinci fıkrasında “Başkanlığa gelen yazı ve "
        "önergelerde kaba ve yaralayıcı sözler varsa, Başkan, gereken düzeltmelerin yapılması için, "
        "o yazı veya önergeyi sahibine geri verir.” kuralına yer verilmiştir. Bu çerçevede Türkiye Büyük "
        "Millet Meclisi Başkanlığı’na sunulan Meclis araştırması önergeleri ile yazılı soru önergelerinde "
        "kaba ifadelerin ya da toplumun bir kesimi veya tamamı yahut belirli kişi veya kişiler yönünden "
        "yaralayıcı olabilecek ifadelerin bulunması durumunda önergenin, söz konusu ifadelerin düzeltilmesi "
        "için TBMM Başkanı tarafından sahibine iadesi gerekmektedir."
    ),
}

IC96_PARAGRAFLARI = {
    "Kişisel görüş": (
        "TBMM İçtüzüğü’nün “Yazılı soru” başlıklı 96’ncı maddesinde “Yazılı soru, … kişisel "
        "görüş ileri sürülmeksizin; … bir önerge ile yazılı olarak cevaplanmak üzere milletvekillerinin, "
        "Cumhurbaşkanı yardımcıları ve bakanlara yazılı olarak soru sormalarından ibarettir.” "
        "kuralına yer verilmiş olup; bu madde uyarınca yazılı soru önergesi metninde önerge sahibi "
        "milletvekilinin kişisel görüşlerine yer verilmemesi gerekmektedir."
    ),
    "Kısa ve gerekçesiz olma": (
        "TBMM İçtüzüğü’nün “Yazılı soru” başlıklı 96’ncı maddesinde “Yazılı soru, kısa, "
        "gerekçesiz … bir önerge ile yazılı olarak cevaplanmak üzere milletvekillerinin, "
        "Cumhurbaşkanı yardımcıları ve bakanlara yazılı olarak soru sormalarından ibarettir.” "
        "kuralına yer verilmiş olup; bu madde uyarınca yazılı soru önergesi metninin kısa ve "
        "gerekçesiz olması gerekmektedir."
    ),
    "Kişilik ve özel yaşama ilişkin konu": (
        "TBMM İçtüzüğü’nün “Yazılı soru” başlıklı 96’ncı maddesinde “Yazılı soru, kısa, "
        "gerekçesiz ve kişisel görüş ileri sürülmeksizin; kişilik ve özel yaşama ilişkin konuları "
        "içermeyen bir önerge ile yazılı olarak cevaplanmak üzere milletvekillerinin, Cumhurbaşkanı "
        "yardımcıları ve bakanlara yazılı olarak soru sormalarından ibarettir.” kuralına yer verilmiş "
        "olup; bu madde uyarınca yazılı soru önergesi metninin kişilik ve özel yaşama ilişkin konuları "
        "içermemesi ve metinde önerge sahibi milletvekilinin kişisel görüşlerine yer verilmemesi "
        "gerekmektedir."
    ),
    "Ek belge yasağı": (
        "TBMM İçtüzüğü’nün “Yazılı soru” başlıklı 96’ncı maddesinde “Yazılı soru, … kişisel "
        "görüş ileri sürülmeksizin; … bir önerge ile yazılı olarak cevaplanmak üzere milletvekillerinin, "
        "Cumhurbaşkanı yardımcıları ve bakanlara yazılı olarak soru sormalarından ibarettir. ... "
        "Yazılı soru önergelerine belge eklenemez.” kuralına yer verilmiş olup; bu madde uyarınca "
        "yazılı soru önergesi metninde önerge sahibi milletvekilinin kişisel görüşlerine yer verilmemesi "
        "ve yazılı soru önergelerine belge eklenmemesi gerekmektedir."
    ),
    "96 tam metin": (
        "TBMM İçtüzüğü’nün “Yazılı soru” başlıklı 96’ncı maddesinde “Yazılı soru, kısa, "
        "gerekçesiz ve kişisel görüş ileri sürülmeksizin; kişilik ve özel yaşama ilişkin konuları "
        "içermeyen bir önerge ile yazılı olarak cevaplanmak üzere milletvekillerinin, Cumhurbaşkanı "
        "yardımcıları ve bakanlara yazılı olarak soru sormalarından ibarettir.” kuralına yer verilmiş "
        "olup; bu madde uyarınca yazılı soru önergesi metninin kısa, gerekçesiz, kişisel görüş "
        "içermeyen ve kişilik ve özel yaşama ilişkin konuları içermeyen nitelikte olması gerekmektedir."
    ),
}

IC97_PARAGRAFI = (
    "TBMM İçtüzüğü’nün “Sorulamayacak konular” başlıklı 97’nci maddesi “Aşağıdaki "
    "sorular Başkanlıkça kabul edilmez: … b) Tek amacı istişare sağlamaktan ibaret konular” "
    "hükmünü içermektedir. Bu maddede yazılı soru önergelerinde sadece belli bir konu hakkında "
    "istişarî amaçla sorulan soruların Başkanlıkça kabul edilemeyeceği hükme bağlanmıştır."
)

SECIM_CEVRESI_GOVDESI = (
    "Türkiye Büyük Millet Meclisi (TBMM) İçtüzüğü’nün 67’nci ve 96’ncı maddeleri "
    "uyarınca TBMM Başkanlığı’na sunulan yazılı soru önergeleri Anayasa ve İçtüzük "
    "hükümlerine uygunluk noktasında TBMM Başkanlığı’nca incelenmekte ve yapılan "
    "değerlendirme sonucunda işleme alınarak gelen kâğıtlar listesinde yayımlanmakta veya "
    "sahibine iade edilmektedir.\n\n"
    "TBMM İçtüzüğü’nün “Yazılı soru” başlıklı 96’ncı maddesinde “Yazılı soru, … kişisel "
    "görüş ileri sürülmeksizin; … bir önerge ile yazılı olarak cevaplanmak üzere milletvekillerinin, "
    "Cumhurbaşkanı yardımcıları ve bakanlara yazılı olarak soru sormalarından ibarettir.” "
    "kuralına yer verilmiştir.\n\n"
    "Milletvekilleri tarafından Anayasa’nın 98’inci maddesi ile TBMM İçtüzüğü’nün "
    "96’ncı maddesi uyarınca Cumhurbaşkanı yardımcıları ve bakanlara yöneltilen yazılı soru "
    "önergelerinde önerge sahibi milletvekilinin seçim çevresini yazması gibi bir zorunluluk "
    "bulunmamaktadır. Bununla birlikte önerge sahibi milletvekilinin önergeye seçim çevresini "
    "yazmayı tercih etmesi durumunda, seçim çevresinin doğru ve mevzuat hükümlerine uygun "
    "şekilde yazılması gerekmektedir.\n\n"
    "Bu çerçevede mevzuatta yeri olmayan bir seçim çevresinin yazılı olduğu ilgi önerge "
    "yukarıda yer verilen mevzuat hükümleri kapsamında görülmüş olup; önergede yer alan seçim "
    "çevresi düzeltildiği takdirde önerge işleme alınabilecektir.\n\n"
    "Bilgilerinizi rica ederim."
)


# =========================================================
# SAYIYI SIRA SÖZÜNE ÇEVİRME
# =========================================================
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


# =========================================================
# YARDIMCI FONKSİYONLAR
# =========================================================
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
    if not entries:
        return ""

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
    if not entries:
        return ""

    if all(e.get("cumle") is None for e in entries):
        soru_numaralari = sorted(set(int(e["soru_no"]) for e in entries))

        if len(soru_numaralari) == 1:
            return f"{soru_numaralari[0]} numaralı sorusunun"

        return f"{turkce_liste(soru_numaralari)} numaralı sorularının"

    soru_gruplari = []

    for entry in entries:
        bulundu = False

        for grup in soru_gruplari:
            if grup["soru_no"] == entry["soru_no"]:
                grup["entries"].append(entry)
                bulundu = True
                break

        if not bulundu:
            soru_gruplari.append({
                "soru_no": entry["soru_no"],
                "entries": [entry],
            })

    ifadeler = []

    for index, grup in enumerate(soru_gruplari):
        soru_no = int(grup["soru_no"])
        terminal = index == len(soru_gruplari) - 1

        if any(e.get("cumle") is None for e in grup["entries"]):
            if terminal:
                ifade = f"{soru_no} numaralı sorusunun"
            else:
                ifade = f"{soru_no} numaralı sorusu"

            ifadeler.append(ifade)
            continue

        cumleler = sorted(set(int(e["cumle"]) for e in grup["entries"]))
        cumle_sozleri = [sira_sozu(c) for c in cumleler]

        if len(cumleler) == 1:
            if terminal:
                ifade = f"{soru_no} numaralı sorusunun {cumle_sozleri[0]} cümlesinin"
            else:
                ifade = f"{soru_no} numaralı sorusunun {cumle_sozleri[0]} cümlesi"
        else:
            if terminal:
                ifade = f"{soru_no} numaralı sorusunun {turkce_liste(cumle_sozleri)} cümlelerinin"
            else:
                ifade = f"{soru_no} numaralı sorusunun {turkce_liste(cumle_sozleri)} cümleleri"

        ifadeler.append(ifade)

    return turkce_liste(ifadeler, baglac="ile")


def ek_belge_grubu_ifadesi(entries: list) -> str:
    soru_numaralari = sorted(set(int(e["soru_no"]) for e in entries))

    if len(soru_numaralari) == 1:
        return f"{soru_numaralari[0]} numaralı sorusuna ek belgenin"

    return f"{turkce_liste(soru_numaralari)} numaralı sorularına ek belgelerin"


def entries_maddelerine_gore_grupla(entries: list) -> list:
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
    gruplar = entries_maddelerine_gore_grupla(entries)
    cumle_parcalari = []

    for index, grup in enumerate(gruplar):
        tip = grup["tip"]
        maddeler = grup["maddeler"]

        if tip == "giris":
            ifade = giris_grubu_ifadesi(grup["entries"])
        elif tip == "soru":
            ifade = soru_grubu_ifadesi(grup["entries"])
        elif tip == "ek_belge":
            ifade = ek_belge_grubu_ifadesi(grup["entries"])
        else:
            ifade = ""

        hukum_ifadesi = madde_yonelme_ifadesi(maddeler)

        if index == 0:
            parca = f"{ifade} yukarıda aktarılan {hukum_ifadesi} aykırılık taşıdığı"
        else:
            parca = f"{ifade} ise yukarıda aktarılan {hukum_ifadesi} aykırılık taşıdığı"

        cumle_parcalari.append(parca)

    return "; ".join(cumle_parcalari)


def sonuc_nesnesi_uret(entries: list) -> str:
    giris_entries = [e for e in entries if e["tip"] == "giris"]
    soru_entries = [e for e in entries if e["tip"] == "soru"]
    ek_belge_entries = [e for e in entries if e["tip"] == "ek_belge"]

    giris_sayisi = len(giris_entries)
    soru_sayisi = len(set(int(e["soru_no"]) for e in soru_entries))
    ek_belge_sayisi = len(set(int(e["soru_no"]) for e in ek_belge_entries))

    etkili_soru_sayisi = soru_sayisi if soru_sayisi > 0 else 0

    if soru_sayisi == 0 and ek_belge_sayisi > 0:
        if giris_sayisi > 0:
            kisim_ifadesi = "kısım" if giris_sayisi == 1 else "kısımlar"
            ek_ifadesi = "ek belge" if ek_belge_sayisi == 1 else "ek belgeler"
            return f"söz konusu {kisim_ifadesi} ve {ek_ifadesi}"

        return "söz konusu ek belge" if ek_belge_sayisi == 1 else "söz konusu ek belgeler"

    if giris_sayisi > 0 and etkili_soru_sayisi > 0:
        kisim_ifadesi = "kısım" if giris_sayisi == 1 else "kısımlar"
        soru_ifadesi = "soru" if etkili_soru_sayisi == 1 else "sorular"
        return f"söz konusu {kisim_ifadesi} ve {soru_ifadesi}"

    if giris_sayisi > 0:
        return "söz konusu kısım" if giris_sayisi == 1 else "söz konusu kısımlar"

    if etkili_soru_sayisi > 0:
        return "söz konusu soru" if etkili_soru_sayisi == 1 else "söz konusu sorular"

    return "söz konusu kısım"


def tum_maddeleri_topla(entries: list) -> list:
    maddeler = []

    for entry in entries:
        for madde in entry["maddeler"]:
            if madde not in maddeler:
                maddeler.append(madde)

    return maddeleri_sirala(maddeler)


def tum_gerekceleri_topla(entries: list) -> dict:
    ic67_gerekceleri = []
    ic96_gerekceleri = []

    for entry in entries:
        g67 = entry.get("gerekce_67")
        g96 = entry.get("gerekce_96")

        if g67 and g67 not in ic67_gerekceleri:
            ic67_gerekceleri.append(g67)

        if g96 and g96 not in ic96_gerekceleri:
            ic96_gerekceleri.append(g96)

    return {
        "67": ic67_gerekceleri,
        "96": ic96_gerekceleri,
    }


def ic67_paragrafi_sec(gerekceler: list) -> str:
    if not gerekceler:
        return IC67_PARAGRAFLARI["Toplumun bir kesimi / belirli kişi veya kişiler yönünden yaralayıcı ifade"]

    if "Kaba ifadeler veya toplumun bir kesimi yönünden yaralayıcı ifade" in gerekceler:
        return IC67_PARAGRAFLARI["Kaba ifadeler veya toplumun bir kesimi yönünden yaralayıcı ifade"]

    if (
        "Kaba ve yaralayıcı ifade" in gerekceler
        and "Toplumun bir kesimi / belirli kişi veya kişiler yönünden yaralayıcı ifade" in gerekceler
    ):
        return IC67_PARAGRAFLARI["Kaba ifadeler veya toplumun bir kesimi yönünden yaralayıcı ifade"]

    if "Kaba ve yaralayıcı ifade" in gerekceler:
        return IC67_PARAGRAFLARI["Kaba ve yaralayıcı ifade"]

    return IC67_PARAGRAFLARI["Toplumun bir kesimi / belirli kişi veya kişiler yönünden yaralayıcı ifade"]


def ic96_paragrafi_sec(gerekceler: list) -> str:
    if not gerekceler:
        return IC96_PARAGRAFLARI["Kişisel görüş"]

    if "Ek belge yasağı" in gerekceler:
        return IC96_PARAGRAFLARI["Ek belge yasağı"]

    if "Kısa ve gerekçesiz olma" in gerekceler and len(gerekceler) == 1:
        return IC96_PARAGRAFLARI["Kısa ve gerekçesiz olma"]

    if "Kişilik ve özel yaşama ilişkin konu" in gerekceler:
        return IC96_PARAGRAFLARI["Kişilik ve özel yaşama ilişkin konu"]

    if "96 tam metin" in gerekceler:
        return IC96_PARAGRAFLARI["96 tam metin"]

    if "Kısa ve gerekçesiz olma" in gerekceler:
        return IC96_PARAGRAFLARI["96 tam metin"]

    return IC96_PARAGRAFLARI["Kişisel görüş"]


def madde_aciklama_paragraflarini_uret(maddeler: list, gerekceler: dict) -> list:
    maddeler = maddeleri_sirala(maddeler)
    paragraflar = []

    for madde in maddeler:
        if madde == "Anayasa’nın 138’inci maddesi":
            paragraflar.append(ANAYASA_138_PARAGRAFI)

        elif madde == "TBMM İçtüzüğü’nün 67’nci maddesi":
            paragraflar.append(ic67_paragrafi_sec(gerekceler.get("67", [])))

        elif madde == "TBMM İçtüzüğü’nün 96’ncı maddesi":
            paragraflar.append(ic96_paragrafi_sec(gerekceler.get("96", [])))

        elif madde == "TBMM İçtüzüğü’nün 97’nci maddesi":
            paragraflar.append(IC97_PARAGRAFI)

    return paragraflar


def yeniden_iade_paragrafi_uret(yeniden_iade_turu: str) -> str:
    if yeniden_iade_turu == "Hayır":
        return ""

    if yeniden_iade_turu == "Bir önceki iade sonrası yeniden verilmiş":
        return (
            "Daha önce tarafınızca verilen ilgi (a) önergenin İçtüzük hükümlerine uygun olarak "
            "yeniden düzenlendiği takdirde işleme alınabileceği hususunun ilgi (b) Başkanlık yazısı ile "
            "tarafınıza bildirildiği; ancak anılan Başkanlık yazısına konu oluşturan hususların İçtüzük "
            "hükümlerine uygun hale getirilmeden önergenin (ilgi (c)) yinelendiği görülmektedir."
        )

    return (
        "Daha önce tarafınızca verilen ilgi (a) ve ilgi (c) önergelerin İçtüzük hükümlerine uygun olarak "
        "yeniden düzenlendiği takdirde işleme alınabileceği hususunun ilgi (b) ve ilgi (ç) Başkanlık yazıları ile "
        "tarafınıza bildirildiği; ancak anılan Başkanlık yazılarına konu oluşturan hususların İçtüzük "
        "hükümlerine uygun hale getirilmeden önergenin (ilgi (d)) yinelendiği görülmektedir."
    )


def esas_iade_paragrafi_uret(
    oner_sayisi: str,
    tamami_iade: bool,
    entries: list,
    tamami_maddeler: list,
    yeniden_iade_turu: str,
    ek_aciklama: str = ""
) -> str:
    if yeniden_iade_turu == "Bir önceki iade sonrası yeniden verilmiş":
        giris = "Bu kapsamda ilgi (c) önergeniz incelenmiş"
        sahiplik = "önergenizin"
        sonuc_ozne = "önergeniz"

    elif yeniden_iade_turu == "Birden fazla önceki iade sonrası yeniden verilmiş":
        giris = "Bu kapsamda ilgi (d) önergeniz incelenmiş"
        sahiplik = "önergenizin"
        sonuc_ozne = "önergeniz"

    else:
        if oner_sayisi == "Tek önerge":
            giris = "Bu çerçevede ilgide kayıtlı önergeniz incelenmiş"
            sahiplik = "önergenizin"
            sonuc_ozne = "önergeniz"
        else:
            giris = "Bu çerçevede ilgide kayıtlı önergeleriniz incelenmiş"
            sahiplik = "önergelerinizin"
            sonuc_ozne = "önergeleriniz"

    ek_aciklama = ek_aciklama.strip()

    if tamami_iade:
        hukum_ifadesi = madde_yonelme_ifadesi(tamami_maddeler)
        sonuc_hukum = sonuc_hukum_ifadesi(tamami_maddeler)

        metin = (
            f"{giris} ve {sahiplik} yukarıda aktarılan "
            f"{hukum_ifadesi} aykırılık taşıdığı değerlendirilmiştir. "
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
            "Henüz iadeye konu kısım eklenmedi. Giriş kısmı veya soru kısmı seçilerek en az bir iadeye konu yer eklenmelidir."
        )

    sorunlu_kisim_cumlesi = sorunlu_kisimler_cumlesi_uret(entries)
    sonuc_nesnesi = sonuc_nesnesi_uret(entries)
    maddeler = tum_maddeleri_topla(entries)
    sonuc_hukum = sonuc_hukum_ifadesi(maddeler)
    ek_belge_var = any(e["tip"] == "ek_belge" for e in entries)

    metin = (
        f"{giris} ve {sahiplik} "
        f"{sorunlu_kisim_cumlesi} değerlendirilmiştir. "
    )

    if ek_aciklama:
        metin += f"{ek_aciklama} "

    if ek_belge_var:
        metin += (
            f"Dolayısıyla {sonuc_ozne}, {sonuc_nesnesi} yukarıda belirtilen "
            f"{sonuc_hukum} uygun olarak yeniden düzenlendiği takdirde işleme alınabilecektir."
        )
    else:
        metin += (
            f"Dolayısıyla {sonuc_ozne}, {sonuc_nesnesi} çıkarıldığı veya yukarıda belirtilen "
            f"{sonuc_hukum} uygun olarak yeniden düzenlendiği takdirde işleme alınabilecektir."
        )

    return metin


def yazi_govdesi_uret(
    esas_paragraf: str,
    maddeler: list,
    gerekceler: dict,
    yeniden_iade_turu: str
) -> str:
    paragraflar = []

    paragraflar.append(STANDART_ACIKLAMA_PARAGRAFI)

    madde_paragraflari = madde_aciklama_paragraflarini_uret(maddeler, gerekceler)
    paragraflar.extend(madde_paragraflari)

    yeniden_paragraf = yeniden_iade_paragrafi_uret(yeniden_iade_turu)
    if yeniden_paragraf:
        paragraflar.append(yeniden_paragraf)

    paragraflar.append(esas_paragraf)

    paragraflar.append("Bilgilerinizi rica ederim.")

    return "\n\n".join(paragraflar)


def gerekce_secimleri_goster(prefix: str, maddeler: list) -> dict:
    gerekce_67 = None
    gerekce_96 = None

    if "TBMM İçtüzüğü’nün 67’nci maddesi" in maddeler:
        gerekce_67 = st.selectbox(
            "İçtüzük 67 Gerekçesi",
            IC67_GEREKCE_SECENEKLERI,
            key=f"{prefix}_gerekce_67"
        )

    if "TBMM İçtüzüğü’nün 96’ncı maddesi" in maddeler:
        gerekce_96 = st.selectbox(
            "İçtüzük 96 Gerekçesi",
            IC96_GEREKCE_SECENEKLERI,
            key=f"{prefix}_gerekce_96"
        )

    return {
        "gerekce_67": gerekce_67,
        "gerekce_96": gerekce_96,
    }


# =========================================================
# SESSION STATE
# =========================================================
if "giris_ids" not in st.session_state:
    st.session_state.giris_ids = [1]

if "next_giris_id" not in st.session_state:
    st.session_state.next_giris_id = 2

if "soru_ids" not in st.session_state:
    st.session_state.soru_ids = [1]

if "next_soru_id" not in st.session_state:
    st.session_state.next_soru_id = 2


def giris_satiri_ekle():
    st.session_state.giris_ids.append(st.session_state.next_giris_id)
    st.session_state.next_giris_id += 1


def soru_satiri_ekle():
    st.session_state.soru_ids.append(st.session_state.next_soru_id)
    st.session_state.next_soru_id += 1


def giris_satiri_sil(row_id: int):
    st.session_state.giris_ids = [x for x in st.session_state.giris_ids if x != row_id]


def soru_satiri_sil(row_id: int):
    st.session_state.soru_ids = [x for x in st.session_state.soru_ids if x != row_id]


# =========================================================
# ARAYÜZ
# =========================================================
st.title("İade Yazısı Gövdesi Üretici")

st.info(
    "Bu demo uygulama yalnızca iade yazısı gövdesini üretir. "
    "Gerçek önerge PDF'i yüklenmez; EBYS antet, sayı, konu, ilgi, imza ve ek kısımları üretilmez."
)

st.subheader("1. İade Türü")

iade_turu = st.selectbox(
    "İade Türü",
    [
        "Olağan İade Usulü",
        "Seçim Çevresi Düzeltme"
    ]
)

if iade_turu == "Seçim Çevresi Düzeltme":
    st.subheader("Üretilen Yazı Gövdesi")

    st.text_area("Yazı Gövdesi", SECIM_CEVRESI_GOVDESI, height=500)

    st.download_button(
        label="Yazı Gövdesini TXT Olarak İndir",
        data=SECIM_CEVRESI_GOVDESI,
        file_name="secim_cevresi_duzeltme_govdesi.txt",
        mime="text/plain"
    )

    st.warning(
        "Not: Bu metin taslaktır. EBYS’ye aktarılmadan önce ilgili önerge ve Başkanlık uygulaması bakımından kontrol edilmelidir."
    )

    st.stop()


st.subheader("2. Genel Bilgiler")

col1, col2 = st.columns(2)

with col1:
    oner_sayisi = st.radio(
        "Önerge Sayısı",
        ["Tek önerge", "Birden fazla önerge"],
        horizontal=True
    )

with col2:
    yeniden_iade_turu = st.selectbox(
        "Yeniden Verilen Önerge Mi?",
        [
            "Hayır",
            "Bir önceki iade sonrası yeniden verilmiş",
            "Birden fazla önceki iade sonrası yeniden verilmiş"
        ]
    )

tamami_iade = st.checkbox(
    "Önergenin Tamamı İadeye Konu Edilecek",
    value=False,
    help="Bu seçenek işaretlenirse giriş ve soru kısmı seçimleri kapatılır."
)

entries = []
tamami_maddeler = []
tamami_gerekceler = {
    "67": [],
    "96": [],
}

if tamami_iade:
    st.warning(
        "Önergenin tamamı seçildiği için giriş kısmı ve soru kısmı alanları devre dışı bırakıldı."
    )

    tamami_maddeler = st.multiselect(
        "Önergenin Tamamı İçin İlgili Hüküm/Hükümler",
        TAMAMI_MADDE_SECENEKLERI,
        default=["TBMM İçtüzüğü’nün 96’ncı maddesi"],
        format_func=madde_kisa_adi
    )

    gerekce_secimleri = gerekce_secimleri_goster("tamami", tamami_maddeler)

    if gerekce_secimleri["gerekce_67"]:
        tamami_gerekceler["67"].append(gerekce_secimleri["gerekce_67"])

    if gerekce_secimleri["gerekce_96"]:
        tamami_gerekceler["96"].append(gerekce_secimleri["gerekce_96"])

else:
    st.subheader("3. İadeye Konu Bölüm Seçimi")

    bolum_col1, bolum_col2 = st.columns(2)

    with bolum_col1:
        giris_secili = st.checkbox("Giriş Kısmı", value=True, key="bolum_giris_secili")

    with bolum_col2:
        soru_secili = st.checkbox("Soru Kısmı", value=False, key="bolum_soru_secili")

    if giris_secili:
        st.subheader("4. Giriş Kısmındaki İadeye Konu Yerler")

        c1, c2 = st.columns([1, 1])

        with c1:
            if st.button("➕ Giriş Kısmı İçin Yeni İadeye Konu Yer Ekle"):
                giris_satiri_ekle()
                st.rerun()

        with c2:
            if st.button("Giriş Kısmı Satırlarını Sıfırla"):
                st.session_state.giris_ids = [1]
                st.session_state.next_giris_id = 2
                st.rerun()

        for row_id in list(st.session_state.giris_ids):
            with st.expander(f"Giriş Kısmı - İadeye Konu Yer #{row_id}", expanded=True):
                sil_col, _ = st.columns([1, 5])

                with sil_col:
                    if st.button("🗑️ Kaldır", key=f"giris_sil_{row_id}"):
                        giris_satiri_sil(row_id)
                        st.rerun()

                col_a, col_b, col_c = st.columns(3)

                with col_a:
                    paragraf = st.number_input(
                        "Paragraf Numarası",
                        min_value=1,
                        max_value=50,
                        value=1,
                        step=1,
                        key=f"giris_paragraf_{row_id}"
                    )

                with col_b:
                    cumle_turu = st.radio(
                        "Kapsam",
                        ["Paragrafın tamamı", "Belirli cümle"],
                        horizontal=False,
                        key=f"giris_cumle_turu_{row_id}"
                    )

                with col_c:
                    if cumle_turu == "Belirli cümle":
                        cumle = st.number_input(
                            "Cümle Numarası",
                            min_value=1,
                            max_value=30,
                            value=1,
                            step=1,
                            key=f"giris_cumle_{row_id}"
                        )
                    else:
                        cumle = None

                maddeler = st.multiselect(
                    "Bu İadeye Konu Yer İçin İlgili Hüküm/Hükümler",
                    GIRIS_MADDE_SECENEKLERI,
                    default=["TBMM İçtüzüğü’nün 96’ncı maddesi"],
                    key=f"giris_maddeler_{row_id}",
                    format_func=madde_kisa_adi
                )

                gerekce_secimleri = gerekce_secimleri_goster(f"giris_{row_id}", maddeler)

                if maddeler:
                    entries.append({
                        "tip": "giris",
                        "paragraf": int(paragraf),
                        "cumle": int(cumle) if cumle is not None else None,
                        "maddeler": maddeler,
                        "gerekce_67": gerekce_secimleri["gerekce_67"],
                        "gerekce_96": gerekce_secimleri["gerekce_96"],
                    })

    if soru_secili:
        st.subheader("5. Soru Kısmındaki İadeye Konu Yerler")

        c1, c2 = st.columns([1, 1])

        with c1:
            if st.button("➕ Soru Kısmı İçin Yeni İadeye Konu Yer Ekle"):
                soru_satiri_ekle()
                st.rerun()

        with c2:
            if st.button("Soru Kısmı Satırlarını Sıfırla"):
                st.session_state.soru_ids = [1]
                st.session_state.next_soru_id = 2
                st.rerun()

        for row_id in list(st.session_state.soru_ids):
            with st.expander(f"Soru Kısmı - İadeye Konu Yer #{row_id}", expanded=True):
                sil_col, _ = st.columns([1, 5])

                with sil_col:
                    if st.button("🗑️ Kaldır", key=f"soru_sil_{row_id}"):
                        soru_satiri_sil(row_id)
                        st.rerun()

                col_a, col_b, col_c = st.columns(3)

                with col_a:
                    soru_no = st.number_input(
                        "Soru Numarası",
                        min_value=1,
                        max_value=100,
                        value=1,
                        step=1,
                        key=f"soru_no_{row_id}"
                    )

                with col_b:
                    soru_kapsam = st.radio(
                        "Kapsam",
                        ["Sorunun tamamı", "Belirli cümle"],
                        horizontal=False,
                        key=f"soru_kapsam_{row_id}"
                    )

                with col_c:
                    if soru_kapsam == "Belirli cümle":
                        soru_cumle = st.number_input(
                            "Cümle Numarası",
                            min_value=1,
                            max_value=30,
                            value=1,
                            step=1,
                            key=f"soru_cumle_{row_id}"
                        )
                    else:
                        soru_cumle = None

                soru_metni_iadeye_konu = st.checkbox(
                    "Bu Soru Metni İadeye Konu Edilecek",
                    value=True,
                    key=f"soru_metni_iade_{row_id}"
                )

                if soru_metni_iadeye_konu:
                    maddeler = st.multiselect(
                        "Bu İadeye Konu Soru/Kısım İçin İlgili Hüküm/Hükümler",
                        SORU_MADDE_SECENEKLERI,
                        default=[
                            "TBMM İçtüzüğü’nün 96’ncı maddesi",
                            "TBMM İçtüzüğü’nün 97’nci maddesi"
                        ],
                        key=f"soru_maddeler_{row_id}",
                        format_func=madde_kisa_adi
                    )

                    gerekce_secimleri = gerekce_secimleri_goster(f"soru_{row_id}", maddeler)

                    if maddeler:
                        entries.append({
                            "tip": "soru",
                            "soru_no": int(soru_no),
                            "cumle": int(soru_cumle) if soru_cumle is not None else None,
                            "maddeler": maddeler,
                            "gerekce_67": gerekce_secimleri["gerekce_67"],
                            "gerekce_96": gerekce_secimleri["gerekce_96"],
                        })

                ek_belge_var = st.checkbox(
                    "Bu Soruya Ek Belge Eklenmiş",
                    value=False,
                    key=f"ek_belge_{row_id}"
                )

                if ek_belge_var:
                    st.info("Ek belge yasağı, İçtüzük 96 kapsamında değerlendirilecektir.")

                    entries.append({
                        "tip": "ek_belge",
                        "soru_no": int(soru_no),
                        "maddeler": ["TBMM İçtüzüğü’nün 96’ncı maddesi"],
                        "gerekce_67": None,
                        "gerekce_96": "Ek belge yasağı",
                    })

with st.expander("6. İsteğe Bağlı Özel Açıklama"):
    st.caption(
        "Bu alan, standart kalıba girmeyen istisnai bir açıklama eklemek için bırakılmıştır. "
        "Boş bırakılırsa metne hiçbir şey eklenmez."
    )

    ek_aciklama = st.text_area(
        "Özel Açıklama Cümlesi",
        height=80,
        placeholder="Gerekirse esas iade değerlendirme paragrafına ilave edilecek açıklamayı yazabilirsiniz. Boş bırakılabilir."
    )

if tamami_iade:
    kullanilan_maddeler = maddeleri_sirala(tamami_maddeler)
    kullanilan_gerekceler = tamami_gerekceler
else:
    kullanilan_maddeler = tum_maddeleri_topla(entries)
    kullanilan_gerekceler = tum_gerekceleri_topla(entries)

esas_paragraf = esas_iade_paragrafi_uret(
    oner_sayisi=oner_sayisi,
    tamami_iade=tamami_iade,
    entries=entries,
    tamami_maddeler=tamami_maddeler,
    yeniden_iade_turu=yeniden_iade_turu,
    ek_aciklama=ek_aciklama
)

yazi_govdesi = yazi_govdesi_uret(
    esas_paragraf=esas_paragraf,
    maddeler=kullanilan_maddeler,
    gerekceler=kullanilan_gerekceler,
    yeniden_iade_turu=yeniden_iade_turu
)

st.subheader("7. Üretilen Yazı Gövdesi")

st.text_area("Yazı Gövdesi", yazi_govdesi, height=550)

st.download_button(
    label="Yazı Gövdesini TXT Olarak İndir",
    data=yazi_govdesi,
    file_name="iade_yazisi_govdesi.txt",
    mime="text/plain"
)

with st.expander("Sadece Esas İade Değerlendirme Paragrafını Göster"):
    st.text_area("Esas İade Değerlendirme Paragrafı", esas_paragraf, height=180)

st.warning(
    "Not: Bu metin taslaktır. EBYS’ye aktarılmadan önce ilgili önerge, madde gerekçesi "
    "ve Başkanlık uygulaması bakımından uzman/yönetici tarafından kontrol edilmelidir."
)
