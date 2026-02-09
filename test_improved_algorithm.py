"""
تست‌های پیشرفته برای بررسی الگوریتم بهبود یافته
"""

import sys
sys.path.insert(0, '/home/claude/backend')

from family_tree import FamilyTree, Gender

def test_aunt_uncle_relationships():
    """تست عمو، عمه، دایی، خاله"""
    print("🧪 تست: عمو، عمه، دایی، خاله (با حذف همسر از مسیر)")
    print("=" * 60)
    
    tree = FamilyTree()
    
    # پدربزرگ و مادربزرگ پدری
    tree.add_person("grandfather_p", "پدربزرگ پدری", "male", 1930)
    tree.add_person("grandmother_p", "مادربزرگ پدری", "female", 1935)
    tree.add_spouse("grandfather_p", "grandmother_p")
    
    # پدر و عمو
    tree.add_person("father", "پدر", "male", 1960)
    tree.add_person("uncle", "عمو", "male", 1965)
    tree.add_parent_child("grandfather_p", "father")
    tree.add_parent_child("grandmother_p", "father")
    tree.add_parent_child("grandfather_p", "uncle")
    tree.add_parent_child("grandmother_p", "uncle")
    
    # همسر پدر
    tree.add_person("mother", "مادر", "female", 1962)
    tree.add_spouse("father", "mother")
    
    # فرزند (من)
    tree.add_person("me", "من", "male", 1990)
    tree.add_parent_child("father", "me")
    tree.add_parent_child("mother", "me")
    
    # تست 1: من به عمو (باید از طریق پدر باشد، نه همسر)
    print("\n📍 تست 1: من → عمو")
    path = tree.bfs_find_path("me", "uncle")
    if path:
        print(f"  مسیر خام: {' -> '.join([f'{p.name}({r})' for p, r in path])}")
        simplified = tree.simplify_relationship(path, tree.people["me"])
        print(f"  نسبت ساده‌شده: {simplified}")
        assert simplified == "عمو", f"خطا: انتظار 'عمو' ولی '{simplified}' دریافت شد"
        print("  ✅ موفق")
    
    # حالا یک عمه اضافه کنیم
    tree.add_person("aunt", "عمه", "female", 1963)
    tree.add_parent_child("grandfather_p", "aunt")
    tree.add_parent_child("grandmother_p", "aunt")
    
    print("\n📍 تست 2: من → عمه")
    path = tree.bfs_find_path("me", "aunt")
    if path:
        print(f"  مسیر خام: {' -> '.join([f'{p.name}({r})' for p, r in path])}")
        simplified = tree.simplify_relationship(path, tree.people["me"])
        print(f"  نسبت ساده‌شده: {simplified}")
        assert simplified == "عمه", f"خطا: انتظار 'عمه' ولی '{simplified}' دریافت شد"
        print("  ✅ موفق")
    
    # پدربزرگ و مادربزرگ مادری
    tree.add_person("grandfather_m", "پدربزرگ مادری", "male", 1932)
    tree.add_person("grandmother_m", "مادربزرگ مادری", "female", 1937)
    tree.add_spouse("grandfather_m", "grandmother_m")
    tree.add_parent_child("grandfather_m", "mother")
    tree.add_parent_child("grandmother_m", "mother")
    
    # دایی
    tree.add_person("maternal_uncle", "دایی", "male", 1968)
    tree.add_parent_child("grandfather_m", "maternal_uncle")
    tree.add_parent_child("grandmother_m", "maternal_uncle")
    
    print("\n📍 تست 3: من → دایی")
    path = tree.bfs_find_path("me", "maternal_uncle")
    if path:
        print(f"  مسیر خام: {' -> '.join([f'{p.name}({r})' for p, r in path])}")
        simplified = tree.simplify_relationship(path, tree.people["me"])
        print(f"  نسبت ساده‌شده: {simplified}")
        assert simplified == "دایی", f"خطا: انتظار 'دایی' ولی '{simplified}' دریافت شد"
        print("  ✅ موفق")
    
    # خاله
    tree.add_person("maternal_aunt", "خاله", "female", 1970)
    tree.add_parent_child("grandfather_m", "maternal_aunt")
    tree.add_parent_child("grandmother_m", "maternal_aunt")
    
    print("\n📍 تست 4: من → خاله")
    path = tree.bfs_find_path("me", "maternal_aunt")
    if path:
        print(f"  مسیر خام: {' -> '.join([f'{p.name}({r})' for p, r in path])}")
        simplified = tree.simplify_relationship(path, tree.people["me"])
        print(f"  نسبت ساده‌شده: {simplified}")
        assert simplified == "خاله", f"خطا: انتظار 'خاله' ولی '{simplified}' دریافت شد"
        print("  ✅ موفق")
    
    print("\n✅ تست عمو/عمه/دایی/خاله موفق!")


def test_grandchild_with_spouse():
    """تست نوه (با حذف همسر از مسیر)"""
    print("\n🧪 تست: نوه (با حذف همسر از مسیر)")
    print("=" * 60)
    
    tree = FamilyTree()
    
    # جد
    tree.add_person("grandfather", "پدربزرگ", "male", 1930)
    tree.add_person("grandmother", "مادربزرگ", "female", 1935)
    tree.add_spouse("grandfather", "grandmother")
    
    # پدر
    tree.add_person("son", "پسر", "male", 1960)
    tree.add_parent_child("grandfather", "son")
    tree.add_parent_child("grandmother", "son")
    
    # همسر پسر
    tree.add_person("daughter_in_law", "عروس", "female", 1965)
    tree.add_spouse("son", "daughter_in_law")
    
    # نوه
    tree.add_person("grandson", "نوه", "male", 1990)
    tree.add_parent_child("son", "grandson")
    tree.add_parent_child("daughter_in_law", "grandson")
    
    print("\n📍 تست: پدربزرگ → نوه")
    path = tree.bfs_find_path("grandfather", "grandson")
    if path:
        print(f"  مسیر خام: {' -> '.join([f'{p.name}({r})' for p, r in path])}")
        simplified = tree.simplify_relationship(path, tree.people["grandfather"])
        print(f"  نسبت ساده‌شده: {simplified}")
        assert "نوه" in simplified, f"خطا: انتظار 'نوه' در '{simplified}'"
        print("  ✅ موفق")
    
    print("\n✅ تست نوه موفق!")


def test_complex_paths_with_spouse():
    """تست مسیرهای پیچیده با همسر"""
    print("\n🧪 تست: مسیرهای پیچیده (با حذف همسر)")
    print("=" * 60)
    
    tree = FamilyTree()
    
    # خانواده
    tree.add_person("p1", "احمد", "male", 1940)
    tree.add_person("p2", "فاطمه", "female", 1945)
    tree.add_spouse("p1", "p2")
    
    tree.add_person("p3", "حسن", "male", 1965)
    tree.add_person("p4", "زهرا", "female", 1970)
    tree.add_spouse("p3", "p4")
    tree.add_parent_child("p1", "p3")
    tree.add_parent_child("p2", "p3")
    
    tree.add_person("p5", "علی", "male", 1967)
    tree.add_person("p6", "مریم", "female", 1972)
    tree.add_spouse("p5", "p6")
    tree.add_parent_child("p1", "p5")
    tree.add_parent_child("p2", "p5")
    
    tree.add_person("p7", "محمد", "male", 1990)
    tree.add_parent_child("p3", "p7")
    tree.add_parent_child("p4", "p7")
    
    tree.add_person("p8", "رضا", "male", 1992)
    tree.add_parent_child("p5", "p8")
    tree.add_parent_child("p6", "p8")
    
    # تست: محمد به علی (عمو)
    print("\n📍 تست: محمد → علی (عمو)")
    path = tree.bfs_find_path("p7", "p5")
    if path:
        print(f"  مسیر خام: {' -> '.join([f'{p.name}({r})' for p, r in path])}")
        simplified = tree.simplify_relationship(path, tree.people["p7"])
        print(f"  نسبت ساده‌شده: {simplified}")
        assert simplified == "عمو", f"خطا: انتظار 'عمو' ولی '{simplified}' دریافت شد"
        print("  ✅ موفق")
    
    # تست: محمد به رضا (پسر عمو)
    print("\n📍 تست: محمد → رضا (پسر عمو)")
    path = tree.bfs_find_path("p7", "p8")
    if path:
        print(f"  مسیر خام: {' -> '.join([f'{p.name}({r})' for p, r in path])}")
        simplified = tree.simplify_relationship(path, tree.people["p7"])
        print(f"  نسبت ساده‌شده: {simplified}")
        assert simplified == "پسر عمو", f"خطا: انتظار 'پسر عمو' ولی '{simplified}' دریافت شد"
        print("  ✅ موفق")
    
    print("\n✅ تست مسیرهای پیچیده موفق!")


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("🌳 تست‌های پیشرفته الگوریتم بهبود یافته")
    print("=" * 60 + "\n")
    
    try:
        test_aunt_uncle_relationships()
        test_grandchild_with_spouse()
        test_complex_paths_with_spouse()
        
        print("\n" + "=" * 60)
        print("🎉 تمام تست‌ها با موفقیت انجام شد!")
        print("=" * 60 + "\n")
        
    except AssertionError as e:
        print(f"\n❌ خطا در تست: {e}\n")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ خطای غیرمنتظره: {e}\n")
        import traceback
        traceback.print_exc()
        sys.exit(1)
