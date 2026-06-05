import telebot

# توكن البوت الثاني الجديد (بوت التحكم)
TOKEN = '8973586545:AAHaJQgY8dBzEtaFNyttkc2ij5HvCGfg3p4'

# الـ ID الشخصي بتاعك عشان رسايل وطلبات المستخدمين تجيلك أنت
ADMIN_ID = 5419401732  

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    name = message.from_user.first_name
    
    if user_id == ADMIN_ID:
        bot.send_message(ADMIN_ID, "👑 أهلاً بك يا مشرفنا في لوحة تحكم البوت.\n\nهنا هتستقبل طلبات النقاط من المستخدمين ومعاها الـ ID بتاعهم جاهز.")
    else:
        # الرسالة التي تظهر للمستخدم لما يدخل البوت الثاني يطلب نقاط
        bot.send_message(
            message.chat.id, 
            f"مرحباً بك يا {name} في قسم الدعم والتحكم الخاص بنقاط الألعاب. 🎯\n\n"
            "اكتب رسالة الآن للمشرف تطلب فيها النقاط (مثال: عايز 50 نقطة)، وانتظر حتى يقوم المشرف بتحويلها لك."
        )
        
        # إشعار يوصلك أنت كآدمن فوراً فيه بيانات المستخدم والـ ID بتاعه جاهز للنسخ
        bot.send_message(
            ADMIN_ID, 
            f"🔔 **طلب نقاط جديد!**\n\n"
            f"👤 الاسم: {name}\n"
            f"🆔 الـ ID: `{user_id}`\n\n"
            f"💡 لإضافة نقاط له، انسخ الـ ID ده وروح لبوت الألعاب واكتب:\n"
            f"`/add {user_id} 50`",
            parse_mode="Markdown"
        )

@bot.message_handler(func=lambda message: True)
def forward_to_admin(message):
    user_id = message.from_user.id
    name = message.from_user.first_name
    text = message.text
    
    if user_id != ADMIN_ID:
        # لو المستخدم بعت أي رسالة تانية (مثلاً يوزر نيم أو سؤال)، بتجيلك برضه مع الـ ID بتاعه
        bot.send_message(
            ADMIN_ID,
            f"📩 **رسالة جديدة من:** {name}\n"
            f"🆔 **الـ ID:** `{user_id}`\n"
            f"💬 **الرسالة:** {text}\n\n"
            f"💡 لإضافة نقاط له اكتب في بوت الألعاب:\n"
            f"`/add {user_id} 50`",
            parse_mode="Markdown"
        )
    else:
        bot.send_message(ADMIN_ID, "❌ الرد المباشر من هنا غير مدعوم، استخدم بوت الألعاب لإضافة النقاط بالأمر المخصص.")

print("⚡ بوت التحكم الثاني شغال وجاهز لاستقبال الحسابات...")
bot.infinity_polling()
