import requests
from datetime import datetime, timedelta
import os
import frontmatter
from pytz import timezone
from dotenv import load_dotenv
from resend import Resend
from babel.dates import format_date

load_dotenv()

server = "https://newsletters.cho.sh/api/campaigns"
username = os.environ["NEWSLETTERS_CHO_SH_USERNAME"]
password = os.environ["NEWSLETTERS_CHO_SH_PASSWORD"]
resend = Resend(os.environ["RESEND_KEY"])
notification = ""

CONFIG = {
    "zh": 34,
    "uk": 33,
    "tr": 32,
    "sv": 31,
    "sl": 30,
    "sk": 29,
    "ru": 28,
    "ro": 27,
    "pt": 26,
    "pl": 25,
    "nb": 24,
    "nl": 23,
    "lv": 22,
    "lt": 21,
    "ko": 20,
    "ja": 19,
    "it": 18,
    "id": 17,
    "hu": 16,
    "fr": 15,
    "fi": 14,
    "et": 13,
    "es": 12,
    "en": 11,
    "el": 10,
    "de": 9,
    "da": 8,
    "cs": 7,
    "bg": 6,
}

EMAIL_CTA = {
    "en": "This is an early research beta, so surprises and mistakes are possible 😃 Please hold tight while we learn and improve!",
    "bg": "Това е ранна изследователска бета-версия, така че са възможни изненади и грешки 😃 Моля, не се колебайте, докато се учим и подобряваме!",
    "cs": "Jedná se o ranou výzkumnou betaverzi, takže je možné, že vás překvapí a uděláte chyby 😃 Prosím, vydržte, dokud se budeme učit a zlepšovat!",
    "da": "Dette er en tidlig forskningsbetaversion, så overraskelser og fejl er mulige 😃 Hold ud, mens vi lærer og forbedrer!",
    "de": "Dies ist eine frühe Forschungs-Beta, also sind Überraschungen und Fehler möglich 😃 Bitte haltet durch, während wir lernen und uns verbessern!",
    "el": "Αυτή είναι μια πρώιμη ερευνητική beta έκδοση, οπότε είναι πιθανές οι εκπλήξεις και τα λάθη 😃 Παρακαλώ κρατηθείτε όσο μαθαίνουμε και βελτιωνόμαστε!",
    "es": "Se trata de una beta de investigación temprana, por lo que es posible que haya sorpresas y errores 😃 ¡Por favor, agárrate fuerte mientras aprendemos y mejoramos!",
    "et": "Tegemist on varase uurimisbeta versiooniga, nii et üllatused ja vead on võimalikud 😃 Palun hoidke kinni, kuni me õpime ja täiustame!",
    "fi": "Tämä on varhainen tutkimusbeta, joten yllätykset ja virheet ovat mahdollisia 😃 Pidä kiinni, kun opimme ja parannamme!",
    "fr": "Il s'agit d'une version bêta de recherche précoce, des surprises et des erreurs sont donc possibles 😃 Veuillez patienter pendant que nous apprenons et que nous nous améliorons !",
    "hu": "Ez egy korai kutatási béta, így lehetségesek meglepetések és hibák 😃 Kérjük, tartsatok ki, amíg tanulunk és javítunk!",
    "id": "Ini adalah penelitian beta awal, jadi kejutan dan kesalahan mungkin saja terjadi 😃 Mohon bersabar sementara kami belajar dan memperbaiki diri!",
    "it": "Si tratta di una beta di ricerca iniziale, quindi sono possibili sorprese ed errori 😃 Vi preghiamo di tenere duro mentre impariamo e miglioriamo!",
    "ja": "これは初期研究のベータ版なので、驚きや間違いはありえます😃 私たちが学び、改善する間、じっと耐えていてください！",
    "ko": "현재 모델은 연구용 베타이기에 예상치 못한 오류나 실수가 있을 수 있습니다 😃 모델을 학습하고 개선하는 동안 기다려주세요!",
    "lt": "Tai ankstyvoji beta versija, todėl galimi netikėtumai ir klaidos 😃 Prašome laikytis, kol mokysimės ir tobulėsime!",
    "lv": "Šī ir agrīna izpētes beta versija, tāpēc iespējami pārsteigumi un kļūdas 😃 Lūdzu, turieties cieši, kamēr mēs mācāmies un uzlabojamies!",
    "nl": "Dit is een vroege onderzoeksbèta, dus verrassingen en fouten zijn mogelijk 😃 Hou je vast terwijl we leren en verbeteren!",
    "nb": "Dette er en tidlig forskningsbeta, så overraskelser og feil er mulig 😃 Vennligst hold deg fast mens vi lærer og forbedrer oss!",
    "pl": "To jest wczesna beta badawcza, więc niespodzianki i błędy są możliwe 😃 Proszę trzymać się mocno, podczas gdy my uczymy się i poprawiamy!",
    "pt": "Este é um beta de investigação precoce, por isso são possíveis surpresas e erros 😃 Por favor, segurem-se bem enquanto aprendemos e melhoramos!",
    "ro": "Aceasta este o versiune beta de cercetare timpurie, așa că sunt posibile surprize și greșeli 😃 Vă rugăm să țineți bine în timp ce învățăm și îmbunătățim!",
    "ru": "Это ранняя исследовательская бета-версия, поэтому возможны сюрпризы и ошибки 😃 Пожалуйста, держитесь крепче, пока мы учимся и совершенствуемся!",
    "sk": "Ide o skorú výskumnú beta verziu, takže sú možné prekvapenia a chyby 😃 Prosím, vydržte, kým sa budeme učiť a zlepšovať!",
    "sl": "To je zgodnja raziskovalna beta različica, zato so možna presenečenja in napake 😃 Počakajte z nami, medtem ko se učimo in izboljšujemo!",
    "sv": "Detta är en tidig betaversion, så överraskningar och misstag är möjliga 😃 Vänligen håll ut medan vi lär oss och förbättrar!",
    "tr": "Bu bir erken araştırma betasıdır, bu nedenle sürprizler ve hatalar mümkündür 😃 Biz öğrenirken ve geliştirirken lütfen sıkı durun!",
    "uk": "Це рання бета-версія дослідження, тому можливі сюрпризи та помилки 😃 Будь ласка, тримайтеся міцніше, поки ми вчимося та вдосконалюємося!",
    "zh": "这是一个早期的研究测试版，所以可能会出现意外和错误😃请在我们学习和改进的时候抓紧时间!",
}

EMAIL_FOOTER = {
    "en": "How was today's newsletter? Let me know by filling out this [survey](https://airtable.com/shrty7OlhrLuBC6UX).",
    "bg": "Как беше днешният бюлетин? Споделете това с мен, като попълните тази [анкета](https://airtable.com/shrty7OlhrLuBC6UX).",
    "cs": "Jaký byl dnešní zpravodaj? Dejte mi vědět vyplněním tohoto [dotazníku](https://airtable.com/shrty7OlhrLuBC6UX).",
    "da": "Hvordan var dagens nyhedsbrev? Lad mig vide det ved at udfylde denne [undersøgelse] (https://airtable.com/shrty7OlhrLuBC6UX).",
    "de": "Wie war der heutige Newsletter? Lassen Sie es mich wissen, indem Sie diese [Umfrage](https://airtable.com/shrty7OlhrLuBC6UX) ausfüllen.",
    "el": "Πώς ήταν το σημερινό ενημερωτικό δελτίο; Ενημερώστε με συμπληρώνοντας αυτή την [έρευνα](https://airtable.com/shrty7OlhrLuBC6UX).",
    "es": "¿Qué tal el boletín de hoy? Házmelo saber rellenando esta [encuesta](https://airtable.com/shrty7OlhrLuBC6UX).",
    "et": "Kuidas oli tänane uudiskiri? Anna mulle teada, täites selle [küsitluse](https://airtable.com/shrty7OlhrLuBC6UX).",
    "fi": "Millainen oli tämänpäiväinen uutiskirje? Kerro minulle täyttämällä tämä [kysely](https://airtable.com/shrty7OlhrLuBC6UX).",
    "fr": "Comment s'est passée la lettre d'information d'aujourd'hui ? Faites-le moi savoir en remplissant cette [enquête] (https://airtable.com/shrty7OlhrLuBC6UX).",
    "hu": "Milyen volt a mai hírlevél? Tudassa velem, ha kitölti ezt a [felmérést](https://airtable.com/shrty7OlhrLuBC6UX).",
    "id": "Bagaimana buletin hari ini? Beri tahu saya dengan mengisi [survei] ini (https://airtable.com/shrty7OlhrLuBC6UX).",
    "it": "Com'era la newsletter di oggi? Fatemelo sapere compilando questo [sondaggio](https://airtable.com/shrty7OlhrLuBC6UX).",
    "ja": "本日のメルマガはいかがでしたでしょうか？この[アンケート](https://airtable.com/shrty7OlhrLuBC6UX)に答えて、教えてください。",
    "ko": "오늘 뉴스레터는 어땠나요? [설문조사](https://airtable.com/shrty7OlhrLuBC6UX)를 작성하여 알려주세요.",
    "lt": "Kaip sekėsi gauti šiandienos naujienlaiškį? Praneškite man apie tai užpildydami šią [apklausą] (https://airtable.com/shrty7OlhrLuBC6UX).",
    "lv": "Kā bija ar šodienas biļetenu? Dodiet man zināt, aizpildot šo [aptauju](https://airtable.com/shrty7OlhrLuBC6UX).",
    "nl": "Hoe was de nieuwsbrief van vandaag? Laat het me weten door deze [enquête] in te vullen (https://airtable.com/shrty7OlhrLuBC6UX).",
    "nb": "Hvordan var dagens nyhetsbrev? Gi meg beskjed ved å fylle ut denne [spørreundersøkelsen] (https://airtable.com/shrty7OlhrLuBC6UX).",
    "pl": "Jak wyglądał dzisiejszy newsletter? Daj mi znać wypełniając tę [ankietę](https://airtable.com/shrty7OlhrLuBC6UX).",
    "pt": "Como foi o boletim informativo de hoje? Avise-me preenchendo este [inquérito](https://airtable.com/shrty7OlhrLuBC6UX).",
    "ro": "Cum a fost buletinul informativ de astăzi? Spuneți-mi, completând acest [sondaj](https://airtable.com/shrty7OlhrLuBC6UX).",
    "ru": "Как вам сегодняшняя рассылка? Дайте мне знать, заполнив этот [опрос] (https://airtable.com/shrty7OlhrLuBC6UX).",
    "sk": "Aký bol dnešný bulletin? Dajte mi vedieť vyplnením tohto [dotazníka](https://airtable.com/shrty7OlhrLuBC6UX).",
    "sl": "Kako je bilo z današnjim glasilom? Povejte mi to tako, da izpolnite to [anketo](https://airtable.com/shrty7OlhrLuBC6UX).",
    "sv": "Hur var dagens nyhetsbrev? Låt mig veta det genom att fylla i denna [enkät] (https://airtable.com/shrty7OlhrLuBC6UX).",
    "tr": "Bugünkü bülten nasıldı? Bu [anketi] (https://airtable.com/shrty7OlhrLuBC6UX) doldurarak bana bildirin.",
    "uk": "Як вам сьогоднішня розсилка? Дайте мені знати, заповнивши це [опитування] (https://airtable.com/shrty7OlhrLuBC6UX).",
    "zh": "今天的通讯怎么样？请填写这个[调查](https://airtable.com/shrty7OlhrLuBC6UX)让我知道。",
}

SHARE = {
    "en": "Share",
    "bg": "Споделете",
    "cs": "Sdílet",
    "da": "Del",
    "de": "Teilen Sie",
    "el": "Μοιραστείτε το",
    "es": "Compartir",
    "et": "Jaga",
    "fi": "Jaa",
    "fr": "Partager",
    "hu": "Megosztás",
    "id": "Bagikan",
    "it": "Condividi",
    "ja": "シェア",
    "ko": "공유",
    "lt": "Dalintis",
    "lv": "Dalīties",
    "nl": "Deel",
    "nb": "Del",
    "pl": "Podziel się",
    "pt": "Partilhar",
    "ro": "Share",
    "ru": "Поделиться",
    "sk": "Zdieľať",
    "sl": "Delite",
    "sv": "Dela",
    "tr": "Paylaş",
    "uk": "Поділіться",
    "zh": "分享",
}


FEEDBACK = {
    "en": "Feedback",
    "bg": "Обратна връзка",
    "cs": "Zpětná vazba",
    "da": "Feedback",
    "de": "Rückmeldung",
    "el": "Ανατροφοδότηση",
    "es": "Comentarios",
    "et": "Tagasiside",
    "fi": "Palaute",
    "fr": "Retour d'information",
    "hu": "Visszajelzés",
    "id": "Umpan balik",
    "it": "Feedback",
    "ja": "フィードバック",
    "ko": "피드백",
    "lt": "Atsiliepimai",
    "lv": "Atsauksmes",
    "nl": "Feedback",
    "nb": "Tilbakemelding",
    "pl": "Informacja zwrotna",
    "pt": "Feedback",
    "ro": "Feedback",
    "ru": "Обратная связь",
    "sk": "Spätná väzba",
    "sl": "Povratne informacije",
    "sv": "Feedback",
    "tr": "Geri bildirim",
    "uk": "Зворотній зв'язок",
    "zh": "反馈信息",
}

SPONSOR = {
    "en": "Sponsor",
    "bg": "Спонсор",
    "cs": "Sponzor",
    "da": "Sponsor",
    "de": "Förderer",
    "el": "Χορηγός",
    "es": "Patrocinador",
    "et": "Sponsor",
    "fi": "Sponsori",
    "fr": "Parrainage",
    "hu": "Szponzor",
    "id": "Sponsor",
    "it": "Sponsor",
    "ja": "スポンサー",
    "ko": "스폰서",
    "lt": "Rėmėjas",
    "lv": "Sponsors",
    "nl": "Sponsor",
    "nb": "Sponsor",
    "pl": "Sponsor",
    "pt": "Patrocinador",
    "ro": "Sponsor",
    "ru": "Спонсор",
    "sk": "Sponzor",
    "sl": "Sponzor",
    "sv": "Sponsor",
    "tr": "Sponsor",
    "uk": "Спонсор",
    "zh": "赞助商",
}


def get_campaigns():
    """Get all campaigns"""
    return requests.get(server, auth=(username, password)).json()


def create_campaign(title, body, lang):
    """Create a new campaign"""
    utc = timezone("UTC")
    today = (
        datetime.now()
        .astimezone(utc)
        .replace(hour=0, minute=0, second=0, microsecond=0)
    )
    next_hour = datetime.now().astimezone(utc) + timedelta(
        minutes=CONFIG[lang] * 1 + 20
    )

    url = "https://hn.cho.sh/" + lang + "/" + today.strftime("%Y/%m/%d")

    menu = f"""\n\n[{SHARE[lang]}]({url}) • [{FEEDBACK[lang]}](https://airtable.com/shrty7OlhrLuBC6UX) • [{SPONSOR[lang]}](https://github.com/sponsors/anaclumos)"""

    prefix = menu

    suffix = f"""\n\n---\n\n""" + EMAIL_FOOTER[lang] + menu + "\n\n"

    res = requests.post(
        server,
        auth=(username, password),
        json={
            "name": f"{today.strftime('%Y-%m-%d')} {lang}",
            "subject": f"🗞️ {title} ({today.strftime('%Y-%m-%d')})",
            "type": "regular",
            "content_type": "markdown",
            "body": prefix + body + suffix,
            "altbody": prefix + body + suffix,
            "lists": [CONFIG[lang]],
            "send_at": f"{today.strftime('%Y-%m-%d')}T{next_hour.strftime('%H:%M:%S')}+00:00",
        },
    ).json()
    try:
        requests.put(
            server + "/" + str(res["data"]["id"]) + "/status",
            auth=(username, password),
            json={"status": "scheduled"},
        )
    except Exception as e:
        print(e)
        print(res)
        print("failed to create campaign for " + lang)
        return False
    print("successfully created campaign for " + lang)
    return True


def find_today_newsletters(lang):
    """Find the newsletter for today in the Research folder. All UTC."""
    utc = timezone("UTC")
    today = (
        datetime.now()
        .astimezone(utc)
        .replace(hour=0, minute=0, second=0, microsecond=0)
    )
    filename = f"legacy/pages/{today.strftime('%Y/%m')}/{today.strftime('%d')}.{lang}.mdx"
    if os.path.exists(filename):
        with open(filename, "r") as f:
            post = frontmatter.load(f)
            title = post.metadata["top_news"] or format_date(
                today, format="long", locale=lang
            )
            body = post.content
            body = (
                body.replace("import { Steps } from 'nextra-theme-docs'", "")
                .replace("<Steps>", "")
                .replace("</Steps>", "")
                .replace(
                    "import CallToAction from '../../../components/CallToAction'", ""
                )
                .replace("<CallToAction />", "")
            )
            return [(title, body)]


def collect_device_info():
    import platform
    import psutil

    collect_notification("\n\n\nCollecting device information...")
    uname = platform.uname()
    collect_notification(f"System: {uname.system}")
    collect_notification(f"Node Name: {uname.node}")
    collect_notification(f"Release: {uname.release}")
    collect_notification(f"Version: {uname.version}")
    collect_notification(f"Machine: {uname.machine}")
    collect_notification(f"Processor: {uname.processor}")
    collect_notification("Physical cores:", psutil.cpu_count(logical=False))
    collect_notification("Total cores:", psutil.cpu_count(logical=True))
    cpufreq = psutil.cpu_freq()
    collect_notification(f"Max Frequency: {cpufreq.max:.2f}Mhz")
    collect_notification(f"Min Frequency: {cpufreq.min:.2f}Mhz")
    collect_notification(f"Current Frequency: {cpufreq.current:.2f}Mhz")
    collect_notification(f"Total CPU Usage: {psutil.cpu_percent()}%")





def collect_notification(*args):
    args = [str(arg) for arg in args]
    text = " ".join(args)
    """Collect notifications and send them at the end."""
    global notification
    notification += text + "\n"


def schedule_newsletter(lang):
    """Schedule the newsletter for today."""
    newsletters = find_today_newsletters(lang)
    if newsletters:
        campaigns = get_campaigns()["data"]["results"]
        for title, post in newsletters:
            duplicate = False
            for campaign in campaigns:
                if title in campaign["name"]:
                    collect_notification("Duplicate... ", title)
                    duplicate = True
                    break
            if not duplicate:
                collect_notification("Scheduling... ", title)
                create_campaign(title, post, lang)
    else:
        collect_notification(f"{lang}: No newsletter for today.")


if __name__ == "__main__":
    for lang in CONFIG:
        schedule_newsletter(lang)
