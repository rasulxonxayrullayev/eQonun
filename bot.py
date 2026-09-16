from pathlib import Path
from urllib.parse import quote_plus
from html import escape
import os

from dotenv import load_dotenv

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

# =========================
# BOT TOKEN
# =========================

load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
ADMIN_CHAT_ID = os.getenv("ADMIN_CHAT_ID")

if not TOKEN:
    raise RuntimeError("TELEGRAM_BOT_TOKEN .env faylida topilmadi")


if not ADMIN_CHAT_ID or not ADMIN_CHAT_ID.lstrip("-").isdigit():
    raise RuntimeError("ADMIN_CHAT_ID .env faylida to‘g‘ri ko‘rsatilmagan")

ADMIN_CHAT_ID = int(ADMIN_CHAT_ID)


BASE_DIR = Path(__file__).resolve().parent
CONSTITUTION_FILE = BASE_DIR / "constitution.pdf"


# =========================
# KODEKSLAR
# =========================

CODES = [
    (
        "⚖️ Jinoyat kodeksi",
        "https://lex.uz/docs/111453"
    ),
    (
        "⚖️ Fuqarolik kodeksi",
        "https://lex.uz/docs/111189"
    ),
    (
        "⚖️ Oila kodeksi",
        "https://lex.uz/docs/104720"
    ),
    (
        "⚖️ Jinoyat-protsessual kodeksi",
        "https://lex.uz/docs/111460"
    ),

    # Quyidagilar uchun LexUZ qidiruv emas,
    # alohida hujjat manzilini keyingi bosqichda
    # tekshirib qo‘shamiz.
    (
        "⚖️ Mehnat kodeksi",
        "https://lex.uz/uz/search/all?query="
        + quote_plus("Mehnat kodeksi")
    ),
    (
        "⚖️ Soliq kodeksi",
        "https://lex.uz/uz/search/all?query="
        + quote_plus("Soliq kodeksi")
    ),
    (
        "⚖️ Bojxona kodeksi",
        "https://lex.uz/uz/search/all?query="
        + quote_plus("Bojxona kodeksi")
    ),
    (
        "⚖️ Yer kodeksi",
        "https://lex.uz/uz/search/all?query="
        + quote_plus("Yer kodeksi")
    ),
    (
        "⚖️ Uy-joy kodeksi",
        "https://lex.uz/uz/search/all?query="
        + quote_plus("Uy-joy kodeksi")
    ),
    (
        "⚖️ Budjet kodeksi",
        "https://lex.uz/uz/search/all?query="
        + quote_plus("Budjet kodeksi")
    ),
    (
        "⚖️ Havo kodeksi",
        "https://lex.uz/uz/search/all?query="
        + quote_plus("Havo kodeksi")
    ),
    (
        "⚖️ Shaharsozlik kodeksi",
        "https://lex.uz/uz/search/all?query="
        + quote_plus("Shaharsozlik kodeksi")
    ),
    (
        "⚖️ Saylov kodeksi",
        "https://lex.uz/uz/search/all?query="
        + quote_plus("Saylov kodeksi")
    ),
    (
        "⚖️ Suv kodeksi",
        "https://lex.uz/uz/search/all?query="
        + quote_plus("Suv kodeksi")
    ),
    (
        "⚖️ Ma’muriy javobgarlik kodeksi",
        "https://lex.uz/uz/search/all?query="
        + quote_plus(
            "Ma’muriy javobgarlik to‘g‘risidagi kodeks"
        )
    ),
    (
        "⚖️ Jinoyat-ijroiya kodeksi",
        "https://lex.uz/uz/search/all?query="
        + quote_plus("Jinoyat-ijroiya kodeksi")
    ),
    (
        "⚖️ Fuqarolik protsessual kodeksi",
        "https://lex.uz/uz/search/all?query="
        + quote_plus("Fuqarolik protsessual kodeksi")
    ),
    (
        "⚖️ Iqtisodiy protsessual kodeksi",
        "https://lex.uz/uz/search/all?query="
        + quote_plus("Iqtisodiy protsessual kodeksi")
    ),
    (
        "⚖️ Ma’muriy sud ishlarini yuritish kodeksi",
        "https://lex.uz/uz/search/all?query="
        + quote_plus(
            "Ma’muriy sud ishlarini yuritish to‘g‘risidagi kodeks"
        )
    ),
]


# =========================
# MUHIM QONUNCHILIK HUJJATLARI
# =========================

DOCUMENTS = [
    ("📄 Konstitutsiya", "https://lex.uz/docs/-6445145"),
    ("📄 Normativ-huquqiy hujjatlar to‘g‘risida", "https://lex.uz/docs/-5378966"),
    ("📄 Bola huquqlarining kafolatlari to‘g‘risida", "https://lex.uz/docs/-1297315"),
    ("📄 Fuqarolarning murojaatlari to‘g‘risida", "https://lex.uz/docs/-3336169"),
    ("📄 Davlat fuqarolik xizmati to‘g‘risida", "https://lex.uz/docs/-6145972"),
    ("📄 Korrupsiyaga qarshi kurashish to‘g‘risida", "https://lex.uz/docs/-3088008"),
    ("📄 Prokuratura to‘g‘risida", "https://lex.uz/docs/-105533"),
    ("📄 Advokatura to‘g‘risida", "https://lex.uz/docs/-54503"),
    ("📄 Sudlar to‘g‘risida", "https://lex.uz/docs/-68532"),
    ("📄 Siyosiy partiyalar to‘g‘risida", "https://lex.uz/docs/-54129"),
    ("📄 Jamoat birlashmalari to‘g‘risida", "https://lex.uz/docs/-111825"),
    ("📄 Vijdon erkinligi va diniy tashkilotlar to‘g‘risida", "https://lex.uz/docs/-54903"),
    ("📄 Axborot erkinligi prinsiplari va kafolatlari to‘g‘risida", "https://lex.uz/docs/-52268"),
    ("📄 Axborotlashtirish to‘g‘risida", "https://lex.uz/docs/-83472"),
    ("📄 Shaxsga doir ma’lumotlar to‘g‘risida", "https://lex.uz/docs/-4396419"),
    ("📄 Elektron hukumat to‘g‘risida", "https://lex.uz/docs/-2833860"),
    ("📄 Elektron hujjat aylanishi to‘g‘risida", "https://lex.uz/docs/-165079"),
    ("📄 Elektron raqamli imzo to‘g‘risida", "https://lex.uz/docs/-243835"),
    ("📄 Iste’molchilarning huquqlarini himoya qilish to‘g‘risida", "https://lex.uz/docs/-4704"),
    ("📄 Tadbirkorlik faoliyati erkinligining kafolatlari to‘g‘risida", "https://lex.uz/docs/-200678"),
    ("📄 Raqobat to‘g‘risida", "https://lex.uz/docs/-6517316"),
    ("📄 Litsenziyalash to‘g‘risida", "https://lex.uz/docs/-5679836"),
    ("📄 Davlat xaridlari to‘g‘risida", "https://lex.uz/docs/-5382974"),
    ("📄 Banklar va bank faoliyati to‘g‘risida", "https://lex.uz/docs/-4581969"),
    ("📄 Ta’lim to‘g‘risida", "https://lex.uz/docs/-5013007"),
    ("📄 Yoshlar siyosati to‘g‘risida", "https://lex.uz/docs/-3026246"),
    ("📄 Mehnatni muhofaza qilish to‘g‘risida", "https://lex.uz/docs/-263044"),
    ("📄 Davlat tili to‘g‘risida", "https://lex.uz/docs/-121051"),
    ("📄 Reklama to‘g‘risida", "https://lex.uz/docs/-6052631"),
    ("📄 Jamoatchilik nazorati to‘g‘risida", "https://lex.uz/docs/-3679097"),
    ("📄 Ommaviy axborot vositalari to‘g‘risida", "https://lex.uz/docs/-11006"),
    ("📄 Davlat sirlarini saqlash to‘g‘risida", "https://lex.uz/docs/-111453"),
    ("📄 Ekologik nazorat to‘g‘risida", "https://lex.uz/docs/-216989"),
    ("📄 Tabiatni muhofaza qilish to‘g‘risida", "https://lex.uz/docs/-107115"),
 ]

def documents_menu():
    buttons = []
    for i in range(0, len(DOCUMENTS), 2):
        row = []
        for j in range(i, min(i + 2, len(DOCUMENTS))):
            title, _ = DOCUMENTS[j]
            row.append(InlineKeyboardButton(title, callback_data=f"doc_{j}"))
        buttons.append(row)
    buttons.append([InlineKeyboardButton("⬅️ Bosh menyu", callback_data="back_main")])
    return InlineKeyboardMarkup(buttons)


# =========================
# MENYU
# =========================

def main_menu():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "🔎 Qonun qidirish",
                callback_data="search"
            ),
        ],
        [
            InlineKeyboardButton(
                "📚 Kodekslar",
                callback_data="codes"
            ),
            InlineKeyboardButton(
                "📜 Konstitutsiya",
                callback_data="constitution"
            )
        ],
        [
            InlineKeyboardButton(
                "📄 Qonunchilik hujjatlari",
                callback_data="documents"
            ),
            InlineKeyboardButton(
                "📖 Huquqiy lug‘at",
                callback_data="dictionary"
            )
        ],
        [
            InlineKeyboardButton(
                "ℹ️ eQonun haqida",
                callback_data="about"
            ),
            InlineKeyboardButton(
                "📩 Murojaatlar",
                callback_data="appeals"
            )
        ]
    ])


def back_main():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "⬅️ Bosh menyu",
                callback_data="back_main"
            )
        ]
    ])


def codes_menu():
    buttons = []

    for i in range(0, len(CODES), 2):

        row = []

        for j in range(i, min(i + 2, len(CODES))):

            title, _ = CODES[j]

            row.append(
                InlineKeyboardButton(
                    title,
                    callback_data=f"code_{j}"
                )
            )

        buttons.append(row)

    buttons.append([
        InlineKeyboardButton(
            "⬅️ Bosh menyu",
            callback_data="back_main"
        )
    ])

    return InlineKeyboardMarkup(buttons)


# =========================
# MUROJAATLAR
# =========================

def appeals_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📝 Tavsiya yuborish", callback_data="appeal_suggestion")],
        [InlineKeyboardButton("⚠️ Shikoyat yuborish", callback_data="appeal_complaint")],
        [InlineKeyboardButton("📱 Telegram sahifamiz", url="https://t.me/rasulxonxayrullayev")],
        [InlineKeyboardButton("📸 Instagram sahifamiz", url="https://www.instagram.com/eqonun")],
        [InlineKeyboardButton("⬅️ Bosh menyu", callback_data="back_main")],
    ])


async def send_appeal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    text = update.message.text.strip()
    appeal_type = context.user_data.pop("appeal_type", "Murojaat")
    if not text:
        await update.message.reply_text("❌ Murojaat matni bo‘sh bo‘lmasin.")
        return
    username = f"@{user.username}" if user.username else "username mavjud emas"
    admin_text = (
        f"📩 <b>Yangi {escape(appeal_type.lower())}</b>\n\n"
        f"👤 Ism: {escape(user.full_name)}\n"
        f"🔹 Username: {escape(username)}\n"
        f"🆔 ID: <code>{user.id}</code>\n\n"
        f"📝 Matn:\n{escape(text)}"
    )
    await context.bot.send_message(chat_id=ADMIN_CHAT_ID, text=admin_text, parse_mode="HTML")
    await update.message.reply_text(
        "✅ Murojaatingiz qabul qilindi. Rahmat!",
        reply_markup=main_menu()
    )


# =========================
# START
# =========================

async def start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    context.user_data["search_mode"] = False

    await update.message.reply_text(
        "⚖️ <b>eQonun</b> botiga xush kelibsiz!\n\n"
        "🇺🇿 O‘zbekiston qonunchiligiga oid "
        "raqamli huquqiy yordamchi.\n\n"
        "Kerakli bo‘limni tanlang:",
        reply_markup=main_menu(),
        parse_mode="HTML"
    )


# =========================
# QIDIRUV
# =========================

async def search_mode(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    context.user_data["search_mode"] = True

    await update.callback_query.edit_message_text(
        "🔎 <b>Qonun qidirish</b>\n\n"
        "Qonun nomi, modda raqami yoki kalit so‘zni "
        "yozing.\n\n"
        "Masalan:\n"
        "• Mehnat shartnomasi\n"
        "• 168-modda\n"
        "• Voyaga yetmaganlar huquqi",
        reply_markup=back_main(),
        parse_mode="HTML"
    )


async def text_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    user_text = update.message.text.strip()

    if context.user_data.get("appeal_type"):
        await send_appeal(update, context)
        return

    if not context.user_data.get("search_mode"):
        return

    context.user_data["search_mode"] = False

    query = update.message.text.strip()

    if not query:
        return

    url = (
        "https://lex.uz/uz/search/all?query="
        + quote_plus(query)
    )

    await update.message.reply_text(
        f"🔎 <b>{query}</b>\n\n"
        "LexUZ'da ushbu so‘rov bo‘yicha qidirish:",
        reply_markup=InlineKeyboardMarkup([
            [
                InlineKeyboardButton(
                    "🌐 Natijalarni ochish",
                    url=url
                )
            ],
            [
                InlineKeyboardButton(
                    "🔎 Yangi qidiruv",
                    callback_data="search"
                )
            ],
            [
                InlineKeyboardButton(
                    "⬅️ Bosh menyu",
                    callback_data="back_main"
                )
            ]
        ]),
        parse_mode="HTML"
    )



# =========================
# 100 TA HUQUQIY ATAMA
# =========================
DICTIONARY = [('Konstitutsiya', 'Davlatning asosiy qonuni.'), ('Qonun', 'Bajarilishi majburiy bo‘lgan normativ-huquqiy hujjat.'), ('Huquq', 'Shaxsga qonun bilan berilgan imkoniyat.'), ('Majburiyat', 'Shaxs bajarishi shart bo‘lgan huquqiy vazifa.'), ('Huquqiy norma', 'Umummajburiy huquqiy qoida.'), ('Huquqiy munosabat', 'Huquq normalari asosida vujudga keladigan munosabat.'), ('Fuqaro', 'Muayyan davlatga huquqiy mansub shaxs.'), ('Fuqarolik', 'Shaxsning davlat bilan doimiy huquqiy aloqasi.'), ('Shaxs', 'Huquq va majburiyatlarga ega inson.'), ('Inson huquqlari', 'Har bir insonga tegishli asosiy huquqlar.'), ('Erkinlik', 'Qonun doirasida mustaqil harakat qilish imkoniyati.'), ('Tenglik', 'Barcha shaxslarning qonun oldida tengligi.'), ('Adolat', 'Huquq va manfaatlarga xolis munosabat.'), ('Qonuniylik', 'Qonunlarga rioya qilish prinsipi.'), ('Javobgarlik', 'Huquqbuzarlik uchun qonuniy chora.'), ('Huquqbuzarlik', 'Qonunga xilof aybli harakat yoki harakatsizlik.'), ('Jinoyat', 'Ijtimoiy xavfli va jinoyat qonunida taqiqlangan qilmish.'), ('Ma’muriy huquqbuzarlik', 'Ma’muriy javobgarlik belgilangan qilmish.'), ('Fuqaroviy huquqbuzarlik', 'Fuqarolik huquqlarini buzish.'), ('Intizomiy huquqbuzarlik', 'Mehnat yoki xizmat intizomini buzish.'), ('Ayb', 'Shaxsning qilmishiga ruhiy munosabati.'), ('Qasd', 'Qilmishni anglab va istab sodir etish.'), ('Ehtiyotsizlik', 'Zarur ehtiyotkorlikka rioya qilmaslik.'), ('Jinoyat tarkibi', 'Jinoyatning asosiy huquqiy belgilari majmui.'), ('Jinoyat obyekti', 'Jinoyat zarar yetkazadigan ijtimoiy munosabat.'), ('Jinoyat subyekti', 'Jinoyat uchun javobgarlikka layoqatli shaxs.'), ('Jabrlanuvchi', 'Huquqbuzarlikdan zarar ko‘rgan shaxs.'), ('Gumon qilinuvchi', 'Jinoyat sodir etganlikda gumon qilinayotgan shaxs.'), ('Ayblanuvchi', 'Jinoyat sodir etganlikda ayblov qo‘yilgan shaxs.'), ('Sudlanuvchi', 'Jinoyat ishi sudda ko‘rilayotgan shaxs.'), ('Guvoh', 'Ishga oid ma’lumotni biladigan shaxs.'), ('Himoyachi', 'Gumon qilinuvchi yoki ayblanuvchini himoya qiluvchi shaxs.'), ('Advokat', 'Malakali huquqiy yordam ko‘rsatuvchi mutaxassis.'), ('Prokuror', 'Qonunlar ijrosi ustidan nazorat qiluvchi mansabdor shaxs.'), ('Tergovchi', 'Jinoyat ishlarini tergov qiluvchi mansabdor shaxs.'), ('Sudya', 'Odil sudlovni amalga oshiruvchi mansabdor shaxs.'), ('Sud', 'Odil sudlovni amalga oshiruvchi davlat organi.'), ('Prokuratura', 'Qonuniylikni ta’minlovchi organlar tizimi.'), ('Tergov', 'Jinoyat holatlarini aniqlashga qaratilgan faoliyat.'), ('Tezkor-qidiruv faoliyati', 'Jinoyatlarni oldini olish va fosh etishga qaratilgan faoliyat.'), ('Dalil', 'Ish uchun muhim qonuniy ma’lumot.'), ('Dalillarni tekshirish', 'Dalillarning ishonchliligini aniqlash jarayoni.'), ('Ekspertiza', 'Maxsus bilimlar asosidagi tekshiruv.'), ('Ekspert', 'Ekspertiza o‘tkazuvchi maxsus bilimli shaxs.'), ('Bayonnoma', 'Protsessual harakatni qayd etuvchi hujjat.'), ('Qaror', 'Vakolatli organ qabul qiladigan hujjat.'), ('Hukm', 'Sudning jinoyat ishi bo‘yicha yakuniy qarori.'), ('Ajrim', 'Sudning protsessual hujjati.'), ('Apellyatsiya', 'Sud qarorini yuqori sudda qayta ko‘rish so‘rovi.'), ('Kassatsiya', 'Sud hujjatini qonuniylik nuqtayi nazaridan tekshirtirish.'), ('Da’vo', 'Huquqni sud orqali himoya qilish talabi.'), ('Da’vogar', 'Sudga da’vo bilan murojaat qilgan shaxs.'), ('Javobgar', 'Da’vo talabi qaratilgan shaxs.'), ('Ariza', 'Vakolatli organga beriladigan rasmiy murojaat.'), ('Shikoyat', 'Buzilgan huquqni tiklashni so‘rab beriladigan murojaat.'), ('Murojaat', 'Ariza, taklif yoki shikoyat.'), ('Mediatsiya', 'Nizoni mediator yordamida hal qilish jarayoni.'), ('Mediator', 'Tomonlarga kelishuvga erishishda yordam beruvchi shaxs.'), ('Kelishuv', 'Tomonlarning o‘zaro rozilik asosidagi bitimi.'), ('Bitim', 'Huquq va majburiyatlarni vujudga keltiruvchi harakat.'), ('Shartnoma', 'Taraflarning huquq va majburiyatlarini belgilovchi kelishuv.'), ('Mehnat shartnomasi', 'Xodim va ish beruvchi o‘rtasidagi shartnoma.'), ('Ish beruvchi', 'Xodim bilan mehnat shartnomasi tuzuvchi shaxs yoki tashkilot.'), ('Xodim', 'Mehnat shartnomasi asosida ishlaydigan shaxs.'), ('Ish haqi', 'Xodim mehnati uchun to‘lanadigan pul.'), ('Mehnat ta’tili', 'Dam olish va mehnat qobiliyatini tiklash vaqti.'), ('Mehnat intizomi', 'Mehnat tartib-qoidalariga rioya qilish.'), ('Soliq', 'Davlat budjetiga to‘lanadigan majburiy to‘lov.'), ('Soliq to‘lovchi', 'Soliq to‘lash majburiyatiga ega shaxs yoki tashkilot.'), ('Budjet', 'Daromad va xarajatlar rejasi.'), ('Mulk', 'Shaxs yoki tashkilotga tegishli mol-mulk va huquqlar.'), ('Mulkdor', 'Mol-mulkka egalik qilish huquqiga ega shaxs.'), ('Egalik qilish', 'Mol-mulkni o‘z tasarrufida saqlash.'), ('Foydalanish', 'Mol-mulkning foydali xususiyatlaridan foydalanish.'), ('Tasarruf etish', 'Mol-mulkning huquqiy taqdirini belgilash.'), ('Meros', 'Vafot etgan shaxs huquq va majburiyatlarining o‘tishi.'), ('Vasiyatnoma', 'Vafotdan keyin mol-mulk taqdirini belgilovchi hujjat.'), ('Nikoh', 'Qonuniy tartibda tuzilgan er-xotinlik ittifoqi.'), ('Oila', 'Nikoh yoki qarindoshlik bilan bog‘langan shaxslar birligi.'), ('Aliment', 'Oila a’zolarini ta’minlash uchun to‘lanadigan mablag‘.'), ('Ma’muriy jazo', 'Ma’muriy huquqbuzarlik uchun qo‘llanadigan chora.'), ('Jarima', 'Huquqbuzarlik uchun undiriladigan pul jazosi.'), ('Ogohlantirish', 'Huquqbuzarlik oqibatlari haqida rasmiy ogohlantirish.'), ('Ma’muriy qamoq', 'Ma’muriy huquqbuzarlik uchun qisqa muddatli qamoq.'), ('Jazoni ijro etish', 'Sud tayinlagan jazoni bajarish.'), ('Amnistiya', 'Muayyan toifadagi shaxslarni jazodan ozod qilish yoki yengillashtirish.'), ('Afv', 'Muayyan mahkumga nisbatan jazoni yengillashtirish yoki bekor qilish.'), ('Reabilitatsiya', 'Nohaq ta’qib qilingan shaxs huquqlarini tiklash.'), ('Sudlanganlik', 'Sud hukmi bilan jazoga tortilganlik holati.'), ('Javobgarlikdan ozod qilish', 'Qonuniy asoslarda javobgarlikni qo‘llamaslik.'), ('Normativ-huquqiy hujjat', 'Huquq normalarini belgilovchi rasmiy hujjat.'), ('Prezident farmoni', 'Prezident tomonidan chiqariladigan hujjat.'), ('Prezident qarori', 'Prezident tomonidan qabul qilinadigan hujjat.'), ('Vazirlar Mahkamasi qarori', 'Vazirlar Mahkamasi qabul qiladigan hujjat.'), ('Qonunosti hujjati', 'Qonun asosida qabul qilinadigan hujjat.'), ('Kodifikatsiya', 'Huquq normalarini yagona tizimli hujjatga birlashtirish.'), ('Kodeks', 'Muayyan huquq sohasidagi normalar jamlangan qonun.'), ('Huquqiy davlat', 'Qonun ustuvor va inson huquqlari ta’minlangan davlat.'), ('Hokimiyatlar bo‘linishi', 'Qonun chiqaruvchi, ijro etuvchi va sud hokimiyatining ajratilishi.'), ('Huquqiy madaniyat', 'Huquqni bilish, hurmat qilish va unga rioya etish darajasi.')]


def dictionary_menu(page=0):
    per_page = 10
    start = page * per_page
    end = min(start + per_page, len(DICTIONARY))
    text = (
        "📖 <b>Huquqiy lug‘at</b>\n\n"
        "Bu bo‘limda <b>100 ta eng kerakli huquqiy atama</b> mavjud.\n"
        f"📄 Sahifa: <b>{page + 1}/10</b>\n\n"
    )
    for number, (term, explanation) in enumerate(DICTIONARY[start:end], start + 1):
        text += f"<b>{number}. {term}</b>\n{explanation}\n\n"

    buttons = []
    navigation = []
    if page > 0:
        navigation.append(InlineKeyboardButton("⬅️ Oldingi", callback_data=f"dict_{page - 1}"))
    if end < len(DICTIONARY):
        navigation.append(InlineKeyboardButton("Keyingi ➡️", callback_data=f"dict_{page + 1}"))
    if navigation:
        buttons.append(navigation)
    buttons.append([InlineKeyboardButton("🏠 Bosh menyu", callback_data="back_main")])
    return text, InlineKeyboardMarkup(buttons)

# =========================
# BUTTONLAR
# =========================

async def button_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()

    data = query.data


    # ---------------------
    # BOSH MENYU
    # ---------------------

    if data == "back_main":

        context.user_data["search_mode"] = False

        await query.edit_message_text(
            "⚖️ <b>eQonun</b>\n\n"
            "Kerakli bo‘limni tanlang:",
            reply_markup=main_menu(),
            parse_mode="HTML"
        )

        return


    # ---------------------
    # QONUN QIDIRISH
    # ---------------------

    if data == "search":

        await search_mode(
            update,
            context
        )

        return


    # ---------------------
    # KODEKSLAR
    # ---------------------

    if data == "codes":

        context.user_data["search_mode"] = False

        await query.edit_message_text(
            "📚 <b>O‘zbekiston Respublikasi kodekslari</b>\n\n"
            "Kerakli kodeksni tanlang:",
            reply_markup=codes_menu(),
            parse_mode="HTML"
        )

        return


    # ---------------------
    # ALOHIDA KODEKS
    # ---------------------

    if data.startswith("code_"):

        context.user_data["search_mode"] = False

        try:

            index = int(
                data.replace(
                    "code_",
                    ""
                )
            )

            title, url = CODES[index]

        except (ValueError, IndexError):

            await query.edit_message_text(
                "❌ Kodeks topilmadi.",
                reply_markup=back_main()
            )

            return


        await query.edit_message_text(
            f"{title}\n\n"
            "📚 Rasmiy LexUZ manbasi:",
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton(
                        "📖 Kodeksni ochish",
                        url=url
                    )
                ],
                [
                    InlineKeyboardButton(
                        "⬅️ Kodekslar",
                        callback_data="codes"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "🏠 Bosh menyu",
                        callback_data="back_main"
                    )
                ]
            ]),
            parse_mode="HTML"
        )

        return


    # ---------------------
    # KONSTITUTSIYA
    # ---------------------

    if data == "constitution":

        context.user_data["search_mode"] = False

        if not CONSTITUTION_FILE.exists():

            await query.edit_message_text(
                "❌ <b>constitution.pdf</b> topilmadi.\n\n"
                "PDF faylni bot.py bilan bir papkaga "
                "joylashtiring.",
                reply_markup=back_main(),
                parse_mode="HTML"
            )

            return


        with open(
            CONSTITUTION_FILE,
            "rb"
        ) as pdf:

            await query.message.reply_document(
                document=pdf,
                caption=(
                    "📜 <b>O‘zbekiston Respublikasi "
                    "Konstitutsiyasi</b>\n\n"
                    "PDF faylni Telegram orqali "
                    "o‘qishingiz mumkin."
                ),
                reply_markup=back_main(),
                parse_mode="HTML"
            )

        return


    # ---------------------
    # QONUNCHILIK HUJJATLARI
    # ---------------------

    if data == "documents":
        await query.edit_message_text(
            "📄 <b>Qonunchilik hujjatlari</b>\n\n"
            "Bu bo‘limda 35 ta muhim qonunchilik hujjati mavjud.\n"
            "Kerakli hujjatni tanlang:",
            reply_markup=documents_menu(),
            parse_mode="HTML"
        )
        return

    if data.startswith("doc_"):
        try:
            index = int(data.replace("doc_", ""))
            title, url = DOCUMENTS[index]
        except (ValueError, IndexError):
            await query.edit_message_text(
                "❌ Hujjat topilmadi.",
                reply_markup=back_main()
            )
            return

        await query.edit_message_text(
            f"{title}\n\n📚 Hujjatning rasmiy matni:",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📖 Hujjatni ochish", url=url)],
                [InlineKeyboardButton("⬅️ Hujjatlar", callback_data="documents")],
                [InlineKeyboardButton("🏠 Bosh menyu", callback_data="back_main")]
            ]),
            parse_mode="HTML"
        )
        return

    # ---------------------
    # LUG‘AT
    # ---------------------

    if data == "dictionary" or data.startswith("dict_"):
        page = 0
        if data.startswith("dict_"):
            try:
                page = int(data.replace("dict_", ""))
            except ValueError:
                page = 0
        text, markup = dictionary_menu(page)
        await query.edit_message_text(
            text,
            reply_markup=markup,
            parse_mode="HTML"
        )
        return


    # ---------------------
    # MUROJAATLAR
    # ---------------------

    if data == "appeals":
        context.user_data["search_mode"] = False
        context.user_data.pop("appeal_type", None)
        await query.edit_message_text(
            "📩 <b>Murojaatlar</b>\n\n"
            "Tavsiya yoki shikoyatingizni yuboring.\n"
            "Murojaat to‘g‘ridan-to‘g‘ri administratorga keladi.",
            reply_markup=appeals_menu(), parse_mode="HTML"
        )
        return

    if data in ("appeal_suggestion", "appeal_complaint"):
        context.user_data["appeal_type"] = (
            "Tavsiya" if data == "appeal_suggestion" else "Shikoyat"
        )
        context.user_data["search_mode"] = False
        await query.edit_message_text(
            ("📝 Tavsiya" if data == "appeal_suggestion" else "⚠️ Shikoyat") + "\n\n"
            "Murojaatingizni bitta xabar qilib yozing:",
            reply_markup=back_main(), parse_mode="HTML"
        )
        return

    # ---------------------
    # HAQIDA
    # ---------------------

    if data == "about":

        await query.edit_message_text(
            "ℹ️ <b>eQonun</b>\n\n"
            "🇺🇿 O‘zbekiston qonunchiligiga oid "
            "raqamli huquqiy yordamchi.\n\n"
            "📚 Kodekslar\n"
            "🔎 Qonun qidirish\n"
            "📜 Konstitutsiya\n\n"
            "⚠️ Huquqiy masalalarda rasmiy "
            "manbani tekshirish tavsiya etiladi.",
            reply_markup=back_main(),
            parse_mode="HTML"
        )

        return


# =========================
# MAIN
# =========================

def main():

    app = (
        Application.builder()
        .token(TOKEN)
        .concurrent_updates(True)
        .build()
    )

    app.add_handler(
        CommandHandler(
            "start",
            start
        )
    )

    app.add_handler(
        CallbackQueryHandler(
            button_handler
        )
    )

    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            text_handler
        )
    )

    print("⚖️ eQonun bot ishga tushdi...")

    app.run_polling(
        drop_pending_updates=True
    )


if __name__ == "__main__":
    main()