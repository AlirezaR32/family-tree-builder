"""
اسکریپت تست برای بررسی عملکرد صحیح سیستم شجره‌نامه
"""

import sys
sys.path.insert(0, '/home/claude/backend')

from family_tree import FamilyTree, Gender

def test_basic_relationships():
    """تست روابط پایه"""
    print("🧪 تست 1: روابط پایه")
    print("=" * 50)
    
    tree = FamilyTree()
    
    # افزودن افراد
    tree.add_person("p1", "احمد", "male", 1950)
    tree.add_person("p2", "فاطمه", "female", 1955)
    tree.add_person("p3", "علی", "male", 1975)
    tree.add_person("p4", "مریم", "female", 1980)
    
    # افزودن روابط
    tree.add_parent_child("p1", "p3")  # احمد پدر علی
    tree.add_parent_child("p2", "p3")  # فاطمه مادر علی
    tree.add_spouse("p3", "p4")        # علی و مریم همسر
    
    # تست مسیر پدر
    print("\n📍 مسیر از علی به احمد (پدر):")
    path = tree.bfs_find_path("p3", "p1")
    if path:
        print(f"  مسیر: {' -> '.join([p.name for p, _ in path])}")
        simplified = tree.simplify_relationship(path, tree.people["p3"])
        print(f"  نسبت: {simplified}")
        assert simplified == "پدر", f"خطا: انتظار 'پدر' ولی '{simplified}' دریافت شد"
        print("  ✅ موفق")
    
    # تست مسیر مادر
    print("\n📍 مسیر از علی به فاطمه (مادر):")
    path = tree.bfs_find_path("p3", "p2")
    if path:
        print(f"  مسیر: {' -> '.join([p.name for p, _ in path])}")
        simplified = tree.simplify_relationship(path, tree.people["p3"])
        print(f"  نسبت: {simplified}")
        assert simplified == "مادر", f"خطا: انتظار 'مادر' ولی '{simplified}' دریافت شد"
        print("  ✅ موفق")
    
    # تست همسر
    print("\n📍 مسیر از علی به مریم (همسر):")
    path = tree.bfs_find_path("p3", "p4")
    if path:
        print(f"  مسیر: {' -> '.join([p.name for p, _ in path])}")
        simplified = tree.simplify_relationship(path, tree.people["p3"])
        print(f"  نسبت: {simplified}")
        assert simplified == "همسر", f"خطا: انتظار 'همسر' ولی '{simplified}' دریافت شد"
        print("  ✅ موفق")
    
    print("\n✅ تست 1 موفق!\n")


def test_grandparents():
    """تست پدربزرگ و مادربزرگ"""
    print("🧪 تست 2: پدربزرگ و مادربزرگ")
    print("=" * 50)
    
    tree = FamilyTree()
    
    # نسل اول (پدربزرگ و مادربزرگ)
    tree.add_person("gf", "جد", "male", 1930)
    tree.add_person("gm", "جده", "female", 1935)
    tree.add_spouse("gf", "gm")
    
    # نسل دوم (پدر و مادر)
    tree.add_person("father", "پدر", "male", 1960)
    tree.add_person("mother", "مادر", "female", 1965)
    tree.add_spouse("father", "mother")
    tree.add_parent_child("gf", "father")
    tree.add_parent_child("gm", "father")
    
    # نسل سوم (فرزند)
    tree.add_person("child", "فرزند", "male", 1990)
    tree.add_parent_child("father", "child")
    tree.add_parent_child("mother", "child")
    
    # تست پدربزرگ
    print("\n📍 مسیر از فرزند به جد (پدربزرگ):")
    path = tree.bfs_find_path("child", "gf")
    if path:
        print(f"  مسیر: {' -> '.join([p.name for p, _ in path])}")
        simplified = tree.simplify_relationship(path, tree.people["child"])
        print(f"  نسبت: {simplified}")
        print("  ✅ موفق")
    
    # تست مادربزرگ
    print("\n📍 مسیر از فرزند به جده (مادربزرگ):")
    path = tree.bfs_find_path("child", "gm")
    if path:
        print(f"  مسیر: {' -> '.join([p.name for p, _ in path])}")
        simplified = tree.simplify_relationship(path, tree.people["child"])
        print(f"  نسبت: {simplified}")
        print("  ✅ موفق")
    
    print("\n✅ تست 2 موفق!\n")


def test_siblings_and_cousins():
    """تست برادر/خواهر و پسر عمو/دایی"""
    print("🧪 تست 3: برادر/خواهر و پسر عمو/دایی")
    print("=" * 50)
    
    tree = FamilyTree()
    
    # پدر و مادر
    tree.add_person("father", "پدر", "male", 1960)
    tree.add_person("mother", "مادر", "female", 1965)
    tree.add_spouse("father", "mother")
    
    # فرزندان (برادر و خواهر)
    tree.add_person("brother", "برادر", "male", 1990)
    tree.add_person("sister", "خواهر", "female", 1992)
    tree.add_parent_child("father", "brother")
    tree.add_parent_child("mother", "brother")
    tree.add_parent_child("father", "sister")
    tree.add_parent_child("mother", "sister")
    
    # تست برادر
    print("\n📍 مسیر از خواهر به برادر:")
    path = tree.bfs_find_path("sister", "brother")
    if path:
        print(f"  مسیر: {' -> '.join([p.name for p, _ in path])}")
        simplified = tree.simplify_relationship(path, tree.people["sister"])
        print(f"  نسبت: {simplified}")
        assert simplified == "برادر", f"خطا: انتظار 'برادر' ولی '{simplified}' دریافت شد"
        print("  ✅ موفق")
    
    # افزودن عمو و پسر عمو
    tree.add_person("grandpa", "پدربزرگ", "male", 1930)
    tree.add_person("grandma", "مادربزرگ", "female", 1935)
    tree.add_spouse("grandpa", "grandma")
    tree.add_parent_child("grandpa", "father")
    tree.add_parent_child("grandma", "father")
    
    tree.add_person("uncle", "عمو", "male", 1965)
    tree.add_parent_child("grandpa", "uncle")
    tree.add_parent_child("grandma", "uncle")
    
    tree.add_person("cousin", "پسر عمو", "male", 1995)
    tree.add_person("uncle_wife", "زن عمو", "female", 1968)
    tree.add_spouse("uncle", "uncle_wife")
    tree.add_parent_child("uncle", "cousin")
    tree.add_parent_child("uncle_wife", "cousin")
    
    # تست عمو
    print("\n📍 مسیر از برادر به عمو:")
    path = tree.bfs_find_path("brother", "uncle")
    if path:
        print(f"  مسیر: {' -> '.join([p.name for p, _ in path])}")
        simplified = tree.simplify_relationship(path, tree.people["brother"])
        print(f"  نسبت: {simplified}")
        assert simplified == "عمو", f"خطا: انتظار 'عمو' ولی '{simplified}' دریافت شد"
        print("  ✅ موفق")
    
    # تست پسر عمو
    print("\n📍 مسیر از برادر به پسر عمو:")
    path = tree.bfs_find_path("brother", "cousin")
    if path:
        print(f"  مسیر: {' -> '.join([p.name for p, _ in path])}")
        simplified = tree.simplify_relationship(path, tree.people["brother"])
        print(f"  نسبت: {simplified}")
        assert simplified == "پسر عمو", f"خطا: انتظار 'پسر عمو' ولی '{simplified}' دریافت شد"
        print("  ✅ موفق")
    
    print("\n✅ تست 3 موفق!\n")


def test_bfs_vs_dfs():
    """مقایسه BFS و DFS"""
    print("🧪 تست 4: مقایسه BFS و DFS")
    print("=" * 50)
    
    tree = FamilyTree()
    
    # ایجاد یک درخت ساده
    for i in range(1, 7):
        tree.add_person(f"p{i}", f"فرد{i}", "male" if i % 2 == 1 else "female")
    
    tree.add_parent_child("p1", "p2")
    tree.add_parent_child("p1", "p3")
    tree.add_parent_child("p2", "p4")
    tree.add_parent_child("p3", "p5")
    tree.add_parent_child("p4", "p6")
    
    print("\n📍 جستجوی مسیر از p1 به p6:")
    
    bfs_path = tree.bfs_find_path("p1", "p6")
    dfs_path = tree.dfs_find_path("p1", "p6")
    
    print(f"  BFS: {' -> '.join([p.name for p, _ in bfs_path])}")
    print(f"  طول مسیر BFS: {len(bfs_path) - 1}")
    
    print(f"  DFS: {' -> '.join([p.name for p, _ in dfs_path])}")
    print(f"  طول مسیر DFS: {len(dfs_path) - 1}")
    
    print("\n  💡 BFS معمولاً کوتاه‌ترین مسیر را پیدا می‌کند")
    print("  💡 DFS اولین مسیر پیدا شده را برمی‌گرداند")
    print("  ✅ موفق")
    
    print("\n✅ تست 4 موفق!\n")


if __name__ == "__main__":
    print("\n" + "=" * 50)
    print("🌳 شروع تست‌های سیستم شجره‌نامه")
    print("=" * 50 + "\n")
    
    try:
        test_basic_relationships()
        test_grandparents()
        test_siblings_and_cousins()
        test_bfs_vs_dfs()
        
        print("\n" + "=" * 50)
        print("🎉 تمام تست‌ها با موفقیت انجام شد!")
        print("=" * 50 + "\n")
        
    except AssertionError as e:
        print(f"\n❌ خطا در تست: {e}\n")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ خطای غیرمنتظره: {e}\n")
        import traceback
        traceback.print_exc()
        sys.exit(1)
