from librouteros import connect

def get_router_connection():
    try:
        api = connect(
            username='admin',
            password='alnjwmy@4',
            host='10.0.0.1',
            port=8728,
            timeout=5
        )
        return api
    except Exception as e:
        print(f"فشل الاتصال بالراوتر: {e}")
        return None

def show_system_resource(api):
    try:
        resource_path = api.path('system', 'resource')
        for res in resource_path:
            print(f"\n--- معلومات النظام الحية ---")
            print(f"إصدار النظام: {res.get('version')}")
            print(f"وقت التشغيل: {res.get('uptime')}")
            print(f"استهلاك المعالج: {res.get('cpu-load')}%")
            
            free_mem = int(res.get('free-memory', 0)) / 1024 / 1024
            total_mem = int(res.get('total-memory', 0)) / 1024 / 1024
            print(f"الذاكرة الحرة: {free_mem:.2f} MB من أصل {total_mem:.2f} MB")
    except Exception as e:
        print(f"خطأ أثناء جلب بيانات النظام: {e}")

def show_hotspot_active(api):
    try:
        active_path = api.path('ip', 'hotspot', 'active')
        print(f"\n--- المستخدمون المتصلون حالياً (Hotspot Active) ---")
        active_list = list(active_path)
        count = 0
        for user in active_list:
            count += 1
            print(f"{count}. ID: {user.get('.id')} | المستخدم: {user.get('user')} | الأيبي: {user.get('address')} | وقت الاتصال: {user.get('uptime')}")
        print(f"إجمالي المتصلين: {count}")
        return active_list
    except Exception as e:
        print(f"خطأ أثناء جلب المتصلين: {e}")
        return []

def kick_hotspot_user(api):
    try:
        active_list = show_hotspot_active(api)
        if not active_list:
            print("لا يوجد مستخدمون متصلون حالياً.")
            return
        
        choice = input("\nأدخل رقم المستخدم لفصله (أو اضغط Enter للإلغاء): ")
        if choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(active_list):
                user_id = active_list[idx].get('.id')
                username = active_list[idx].get('user')
                
                active_path = api.path('ip', 'hotspot', 'active')
                active_path.remove(**{'.id': user_id})
                print(f"تم فصل المستخدم {username} بنجاح!")
            else:
                print("رقم غير صحيح.")
    except Exception as e:
        print(f"خطأ أثناء فصل المستخدم: {e}")

def show_hotspot_users(api):
    try:
        users_path = api.path('ip', 'hotspot', 'user')
        print(f"\n--- قائمة مستخدمي الهوتسبوت المسجلين ---")
        count = 0
        for u in users_path:
            count += 1
            print(f"{count}. الاسم: {u.get('name')} | البروفايل: {u.get('profile', 'default')} | معطل: {u.get('disabled', 'false')}")
        print(f"إجمالي المستخدمين المسجلين: {count}")
    except Exception as e:
        print(f"خطأ أثناء جلب المستخدمين: {e}")

def add_hotspot_user(api):
    try:
        print(f"\n--- إضافة مستخدم هوتسبوت جديد ---")
        username = input("أدخل اسم المستخدم (Username): ").strip()
        password = input("أدخل كلمة المرور (Password): ").strip()
        profile = input("أدخل اسم البروفايل (Profile) [اتركه فارغاً لـ default]: ").strip() or 'default'
        
        if not username:
            print("اسم المستخدم لا يمكن أن يكون فارغاً.")
            return
            
        users_path = api.path('ip', 'hotspot', 'user')
        users_path.add(name=username, password=password, profile=profile)
        print(f"تم إضافة المستخدم '{username}' بنجاح بروفايل '{profile}'!")
    except Exception as e:
        print(f"خطأ أثناء إضافة المستخدم: {e}")

def show_dhcp_leases(api):
    try:
        leases_path = api.path('ip', 'dhcp-server', 'lease')
        print(f"\n--- عملاء DHCP المتصلون (DHCP Leases) ---")
        count = 0
        for lease in leases_path:
            count += 1
            host_name = lease.get('host-name', 'غير معروف')
            address = lease.get('address', '')
            mac = lease.get('mac-address', '')
            print(f"{count}. الجهاز: {host_name} | الأيبي: {address} | الماك: {mac}")
        print(f"إجمالي الأجهزة: {count}")
    except Exception as e:
        print(f"خطأ أثناء جلب بيانات DHCP: {e}")

def show_interface_traffic(api):
    try:
        iface_path = api.path('interface')
        print(f"\n--- إحصائيات حركة مرور الواجهات (Traffic Stats) ---")
        for iface in iface_path:
            name = iface.get('name')
            rx_bytes = int(iface.get('rx-byte', 0)) / 1024 / 1024
            tx_bytes = int(iface.get('tx-byte', 0)) / 1024 / 1024
            print(f"الواجهة: {name} | الاستقبال (RX): {rx_bytes:.2f} MB | الإرسال (TX): {tx_bytes:.2f} MB")
    except Exception as e:
        print(f"خطأ أثناء جلب إحصائيات حركة المرور: {e}")

def show_hotspot_profiles(api):
    try:
        profiles_path = api.path('ip', 'hotspot', 'user', 'profile')
        print(f"\n--- بروفايلات الهوتسبوت (Hotspot Profiles) ---")
        count = 0
        for prof in profiles_path:
            count += 1
            name = prof.get('name')
            rate_limit = prof.get('rate-limit', 'غير محدود')
            shared_users = prof.get('shared-users', '1')
            print(f"{count}. البروفايل: {name} | السرعة (Rate Limit): {rate_limit} | المستخدمين المشتركين: {shared_users}")
        print(f"إجمالي البروفايلات: {count}")
    except Exception as e:
        print(f"خطأ أثناء جلب البروفايلات: {e}")

def show_interfaces(api):
    try:
        iface_path = api.path('interface')
        print(f"\n--- حالة واجهات الشبكة (Interfaces) ---")
        for iface in iface_path:
            name = iface.get('name')
            running = iface.get('running')
            print(f"الواجهة: {name} | تعمل: {running}")
    except Exception as e:
        print(f"خطأ أثناء جلب واجهات الشبكة: {e}")

def reboot_router(api):
    confirm = input("هل أنت متأكد من رغبتك في إعادة تشغيل الراوتر؟ (y/n): ").strip().lower()
    if confirm == 'y':
        try:
            api.path('system').call('reboot')
            print("جاري إعادة تشغيل الراوتر...")
        except Exception as e:
            print(f"خطأ أثناء إعادة التشغيل: {e}")
    else:
        print("تم إلغاء عملية إعادة التشغيل.")

def main_menu():
    print("جاري الاتصال بجهاز المايكروتيك...")
    api = get_router_connection()
    if not api:
        return
    print("تم الاتصال بنجاح!")

    while True:
        print("\n==================================")
        print("   لوحة تحكم الشبكة (Mini-WinBox)")
        print("==================================")
        print("1. عرض معلومات النظام الحية")
        print("2. عرض المستخدمين المتصلين (Hotspot Active)")
        print("3. فصل مستخدم نشط (Kick User)")
        print("4. عرض جميع المستخدمين المسجلين (Hotspot Users)")
        print("5. إضافة مستخدم هوتسبوت جديد (Add User)")
        print("6. عرض عملاء DHCP المتصلين (DHCP Leases)")
        print("7. مراقبة حركة المرور (Traffic Stats)")
        print("8. عرض بروفايلات الهوتسبوت (Hotspot Profiles)")
        print("9. عرض حالة واجهات الشبكة (Interfaces)")
        print("10. إعادة تشغيل الراوتر (Reboot)")
        print("11. الخروج")
        
        choice = input("\nاختر رقماً من القائمة (1-11): ").strip()
        
        if choice == '1':
            show_system_resource(api)
        elif choice == '2':
            show_hotspot_active(api)
        elif choice == '3':
            kick_hotspot_user(api)
        elif choice == '4':
            show_hotspot_users(api)
        elif choice == '5':
            add_hotspot_user(api)
        elif choice == '6':
            show_dhcp_leases(api)
        elif choice == '7':
            show_interface_traffic(api)
        elif choice == '8':
            show_hotspot_profiles(api)
        elif choice == '9':
            show_interfaces(api)
        elif choice == '10':
            reboot_router(api)
        elif choice == '11':
            print("إغلاق التطبيق. مع السلامة!")
            break
        else:
            print("خيار غير صحيح، يرجى المحاولة مرة أخرى.")

if __name__ == '__main__':
    main_menu()

