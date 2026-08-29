from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from librouteros import connect

class NetAdminApp(App):
    def build(self):
        self.title = "النجومي نت - إدارة الشبكة"
        
        root = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # عنوان التطبيق
        root.add_widget(Label(text="لوحة تحكم النجومي نت", font_size=22, size_hint_y=None, height=50))
        
        # شاشة عرض النتائج
        self.output_label = Label(text="اضغط على أي زر لبدء الجلب...", halign='right', valign='top')
        self.output_label.bind(size=self.output_label.setter('text_size'))
        
        scroll = ScrollView(size_hint=(1, 0.7))
        scroll.add_widget(self.output_label)
        root.add_widget(scroll)
        
        # الأزرار
        btn_layout = BoxLayout(orientation='vertical', spacing=5, size_hint_y=None, height=150)
        
        btn_sys = Button(text="معلومات النظام", background_color=(0.1, 0.5, 0.8, 1))
        btn_sys.bind(on_press=self.get_system_info)
        btn_layout.add_widget(btn_sys)
        
        btn_active = Button(text="المتصلون حالياً", background_color=(0.1, 0.7, 0.3, 1))
        btn_active.bind(on_press=self.get_active_users)
        btn_layout.add_widget(btn_active)
        
        root.add_widget(btn_layout)
        return root

    def connect_router(self):
        try:
            return connect(username='admin', password='alnjwmy@4', host='10.0.0.1', port=8728, timeout=3)
        except Exception as e:
            return None

    def get_system_info(self, instance):
        api = self.connect_router()
        if not api:
            self.output_label.text = "فشل الاتصال بالراوتر!"
            return
        try:
            res = list(api.path('system', 'resource'))[0]
            info = f"إصدار النظام: {res.get('version')}\nوقت التشغيل: {res.get('uptime')}\nاستهلاك المعالج: {res.get('cpu-load')}%"
            self.output_label.text = info
        except Exception as e:
            self.output_label.text = f"خطأ: {e}"

    def get_active_users(self, instance):
        api = self.connect_router()
        if not api:
            self.output_label.text = "فشل الاتصال بالراوتر!"
            return
        try:
            users = list(api.path('ip', 'hotspot', 'active'))
            text = f"إجمالي المتصلين: {len(users)}\n\n"
            for u in users:
                text += f"- {u.get('user')} ({u.get('address')})\n"
            self.output_label.text = text
        except Exception as e:
            self.output_label.text = f"خطأ: {e}"

if __name__ == '__main__':
    NetAdminApp().run()

