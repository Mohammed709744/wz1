import telebot
from telebot import types
import random
import json
import os

# التوكن الخاص ببوت الألعاب الحالي
TOKEN = '8846614151:AAG6sUtlbwH1RxAy8hcDaRvAWxMqYn7rsYA'

# معرف البوت الجديد الخاص بك بدون @ ليتم تحويل الناس إليه
NEW_BOT_USERNAME = 'wz1points_wzbot' 

# الـ ID الشخصي بتاعك لكي يقبل البوت منك أوامر تحويل النقاط
ADMIN_ID = 5419401732  

bot = telebot.TeleBot(TOKEN)
DB_FILE = 'users_data.json'

def load_data():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_data(data):
    with open(DB_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

user_data = load_data()

def get_user(user_id, name="مستخدم"):
    uid = str(user_id)
    if uid not in user_data:
        user_data[uid] = {"name": name, "points": 0, "requested": False}
        save_data(user_data)
    return user_data[uid]

def main_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_profile = types.KeyboardButton("👤 حسابي ونقاطي")
    btn_request = types.KeyboardButton("🎁 طلب 50 نقطة")
    btn_wheel = types.KeyboardButton("🎡 لَف عجلة الحظ")
    btn_box = types.KeyboardButton("📦 فتح صندوق المفاجآت")
    markup.add(btn_profile, btn_request)
    markup.add(btn_wheel, btn_box)
    return markup

# 🌟 أمر التحكم الخاص بك كآدمن لتحويل وإضافة النقاط من الشات
@bot.message_handler(commands=['add'])
def add_points_command(message):
    if message.from_user.id != ADMIN_ID:
        return
    
    try:
        # طريقة كتابة الأمر في الشات: /add 123456789 50
        parts = message.text.split()
        if len(parts) < 3:
            bot.reply_to(message, "❌ الاستخدام الصحيح للأمر:\n`/add ID_المستخدم النقاط`")
            return
            
        target_id = parts[1]
        amount = int(parts[2])
        
        if target_id not in user_data:
            bot.reply_to(message, "❌ هذا المستخدم لم يسجل في البوت بعد!")
            return
            
        user_data[target_id]['points'] += amount
        save_data(user_data)
        
        bot.reply_to(message, f"✅ تم إضافة {amount} نقطة بنجاح لحساب {user_data[target_id]['name']}.\n🌟 رصيده الحالي: {user_data[target_id]['points']}")
        
        # إرسال رسالة تلقائية للمستخدم لتنبيهه بالنقاط الجديدة
        try:
            bot.send_message(target_id, f"🎉 تم إضافة {amount} نقطة إلى حسابك من قبل المشرف! رصيدك الحالي: {user_data[target_id]['points']}")
        except Exception:
            pass
            
    except Exception as e:
        bot.reply_to(message, f"❌ حدث خطأ أثناء تنفيذ الأمر. تأكد من صحة البيانات.")

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user = get_user(message.from_user.id, message.from_user.first_name)
    bot.send_message(
        message.chat.id, 
        f"🎉 أهلاً بك يا {user['name']} في بوت التسلية والألعاب!\n\n"
        "هنا تقدر تطلب نقاط وتلعب بعجلة الحظ والصناديق للتسلية. 🎪", 
        reply_markup=main_keyboard()
    )

@bot.message_handler(func=lambda message: True)
def handle_messages(message):
    user_id = message.from_user.id
    uid = str(user_id)
    user = get_user(user_id, message.from_user.first_name)
    
    if message.text == "👤 حسابي ونقاطي":
        bot.send_message(message.chat.id, f"👤 الاسم: {user['name']}\n🌟 رصيدك الحالي: {user['points']} نقطة.")
        
    elif message.text == "🎁 طلب 50 نقطة":
        # الزر الذي يوجه المستخدمين لبوت التحكم لطلب نقاطك
        redirect_markup = types.InlineKeyboardMarkup()
        btn_go = types.InlineKeyboardButton("انتقل إلى بوت التحكم لطلب النقاط 🚀", url=f"t.me/{NEW_BOT_USERNAME}")
        redirect_markup.add(btn_go)
        
        bot.send_message(
            message.chat.id, 
            "🔄 لطلب النقاط، تم تحويل نظام التحكم إلى البوت الجديد. اضغط على الزر بالأسفل للتواصل وطلب النقاط مباشرة:", 
            reply_markup=redirect_markup
        )

    elif message.text == "🎡 لَف عجلة الحظ":
        if user['points'] < 10:
            bot.send_message(message.chat.id, "❌ تكلفة لفة العجلة 10 نقاط. رصيدك لا يكفي! اضغط على زر طلب نقاط.")
            return
            
        user['points'] -= 10
        prizes = [0, 5, 10, 20, 50]
        win = random.choice(prizes)
        user['points'] += win
        save_data(user_data)
        
        if win > 10:
            msg = f"🎡 العجلة دارت... وكسبت {win} نقطة! 🎉 رصيدك الحالي: {user['points']}"
        elif win == 10:
            msg = f"🎡 العجلة دارت... ورجعت لك نقاطك (10 نقاط)! رصيدك الحالي: {user['points']}"
        elif win == 5:
            msg = f"🎡 العجلة دارت... خسرت جزء وكسبت 5 نقاط فقط. الرصيد: {user['points']}"
        else:
            msg = f"💥 حظ سيء! العجلة وقفت على 0. الرصيد الحالي: {user['points']}"
            
        bot.send_message(message.chat.id, msg)

    elif message.text == "📦 فتح صندوق المفاجآت":
        if user['points'] < 15:
            bot.send_message(message.chat.id, "❌ تكلفة فتح الصندوق 15 نقطة. رصيدك لا يكفي!")
            return
            
        user['points'] -= 15
        outcomes = ["فاضي 🗑️", "هدية صغيرة 🎁 (+5 نقاط)", "جائزة كبرى 👑 (+100 نقطة)", "قنبلة 💣 (-10 نقاط)"]
        result = random.choice(outcomes)
        
        if "فاضي" in result:
            pass
        elif "صغيرة" in result:
            user['points'] += 5
        elif "كبرى" in result:
            user['points'] += 100
        elif "قنبلة" in result:
            user['points'] -= 10
            if user['points'] < 0: user['points'] = 0
            
        save_data(user_data)
        bot.send_message(message.chat.id, f"📦 فتحت الصندوق ووجدت بداخله:\n【 {result} 】\n🌟 رصيدك الجديد: {user['points']} نقطة.")

print("⚡ بوت الألعاب شغال وجاهز لاستقبال أوامر تحويل النقاط...")
bot.infinity_polling()
