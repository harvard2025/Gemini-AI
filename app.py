from flask import Flask, render_template, request
import requests
from google import genai
import markdown
app = Flask(__name__)


# 🔧 دالة إرسال البرومبت للموديل
def ask_model(prompt):
    # >>>>>>>>>>>>>>>>>>>> هنا و يشتغل APIناقص بس تحط ال 
    # >>>>>>>>>>>> Gemini AI studio/Get your API key --> 
    a = "Put you API key Here"
    client = genai.Client(api_key=a)
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    return markdown.markdown(response.text)
    

# 📝 تجهيز البرومبت الذكي لتحليل النص
def build_prompt(user_text):
    return f"""
        قم بتحليل النص التالي الذي يُمثل جزءًا من شروط الاستخدام أو سياسة الخصوصية. قم بالآتي بدقة:

        1. استخرج أي بنود تنتهك خصوصية المستخدم أو تمنح الشركة صلاحيات مبالغ فيها، مثل:
        - جمع بيانات المستخدم أو بيعها لطرف ثالث.
        - تتبع موقع المستخدم أو سلوكه دون موافقة واضحة.
        - حرمان المستخدم من الحق في حذف بياناته.
        - منح الشركة الحق في تعديل الشروط دون إشعار.

        2. صنّف كل بند مشبوه حسب مستوى الخطورة: (منخفض، متوسط، عالي الخطورة).

        3. ترجم كل بند قانوني أو غامض إلى لغة عربية بسيطة وواضحة يفهمها أي مستخدم.

        4. إذا لم يحتوي النص على أي مشاكل، فقل ذلك بوضوح، واذكر الأسباب.

        5. إذا كان النص غير كافٍ للحكم، فاشرح لماذا، واطلب من المستخدم تزويدك بجزء أطول أو أكثر تحديدًا.

        النص:
        \"\"\"
        {user_text}
        \"\"\"
    """ 


# 🌐 Route رئيسية للموقع
@app.route("/", methods=["GET", "POST"])
def index():
    reply = None
    if request.method == "POST":
        user_input = request.form.get("text")
        prompt = build_prompt(user_input)
        reply = ask_model(prompt)
    return render_template("layout.html", nigga=reply)

# 🚀 تشغيل السيرفر
if __name__ == "__main__":
    app.run()