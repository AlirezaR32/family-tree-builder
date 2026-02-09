"""
سیستم شجره‌نامه خانوادگی با الگوریتم‌های DFS و BFS
"""

from collections import deque
from typing import Optional, List, Dict, Tuple
from enum import Enum
import json


class Gender(Enum):
    MALE = "male"
    FEMALE = "female"


class RelationType(Enum):
    PARENT = "parent"
    CHILD = "child"
    SPOUSE = "spouse"


class Person:
    """کلاس نمایش یک فرد در شجره‌نامه"""
    
    def __init__(self, person_id: str, name: str, gender: Gender, birth_year: Optional[int] = None):
        self.id = person_id
        self.name = name
        self.gender = gender
        self.birth_year = birth_year
        self.parents: List[Person] = []
        self.children: List[Person] = []
        self.spouse: Optional[Person] = None
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "gender": self.gender.value,
            "birth_year": self.birth_year,
            "parents": [p.id for p in self.parents],
            "children": [c.id for c in self.children],
            "spouse": self.spouse.id if self.spouse else None
        }


class FamilyTree:
    """کلاس اصلی درخت خانوادگی"""
    
    def __init__(self):
        self.people: Dict[str, Person] = {}
    
    def add_person(self, person_id: str, name: str, gender: str, birth_year: Optional[int] = None) -> Person:
        """افزودن فرد جدید"""
        if person_id in self.people:
            raise ValueError(f"فرد با شناسه {person_id} قبلاً وجود دارد")
        
        person = Person(person_id, name, Gender(gender), birth_year)
        self.people[person_id] = person
        return person
    
    def remove_person(self, person_id: str) -> bool:
        """حذف فرد از درخت"""
        if person_id not in self.people:
            return False
        
        person = self.people[person_id]
        
        # حذف ارتباطات
        for parent in person.parents:
            if person in parent.children:
                parent.children.remove(person)
        
        for child in person.children:
            if person in child.parents:
                child.parents.remove(person)
        
        if person.spouse:
            person.spouse.spouse = None
        
        del self.people[person_id]
        return True
    
    def add_parent_child(self, parent_id: str, child_id: str):
        """افزودن رابطه والد-فرزند"""
        if parent_id not in self.people or child_id not in self.people:
            raise ValueError("فرد مورد نظر یافت نشد")
        
        parent = self.people[parent_id]
        child = self.people[child_id]
        
        if parent not in child.parents:
            child.parents.append(parent)
        if child not in parent.children:
            parent.children.append(child)
    
    def add_spouse(self, person1_id: str, person2_id: str):
        """افزودن رابطه همسری"""
        if person1_id not in self.people or person2_id not in self.people:
            raise ValueError("فرد مورد نظر یافت نشد")
        
        person1 = self.people[person1_id]
        person2 = self.people[person2_id]
        
        person1.spouse = person2
        person2.spouse = person1
    
    def bfs_find_path(self, start_id: str, end_id: str) -> Optional[List[Tuple[Person, str]]]:
        """پیدا کردن مسیر با الگوریتم BFS"""
        if start_id not in self.people or end_id not in self.people:
            return None
        
        if start_id == end_id:
            return [(self.people[start_id], "خود")]
        
        visited = set()
        queue = deque([(self.people[start_id], [(self.people[start_id], "شروع")])])
        
        while queue:
            current, path = queue.popleft()
            
            if current.id in visited:
                continue
            visited.add(current.id)
            
            if current.id == end_id:
                return path
            
            # بررسی والدین
            for parent in current.parents:
                if parent.id not in visited:
                    new_path = path + [(parent, "والد")]
                    queue.append((parent, new_path))
            
            # بررسی فرزندان
            for child in current.children:
                if child.id not in visited:
                    new_path = path + [(child, "فرزند")]
                    queue.append((child, new_path))
            
            # بررسی همسر
            if current.spouse and current.spouse.id not in visited:
                new_path = path + [(current.spouse, "همسر")]
                queue.append((current.spouse, new_path))
        
        return None
    
    def dfs_find_path(self, start_id: str, end_id: str) -> Optional[List[Tuple[Person, str]]]:
        """پیدا کردن مسیر با الگوریتم DFS"""
        if start_id not in self.people or end_id not in self.people:
            return None
        
        if start_id == end_id:
            return [(self.people[start_id], "خود")]
        
        visited = set()
        
        def dfs_recursive(current: Person, path: List[Tuple[Person, str]]) -> Optional[List[Tuple[Person, str]]]:
            if current.id in visited:
                return None
            
            visited.add(current.id)
            
            if current.id == end_id:
                return path
            
            # بررسی والدین
            for parent in current.parents:
                result = dfs_recursive(parent, path + [(parent, "والد")])
                if result:
                    return result
            
            # بررسی فرزندان
            for child in current.children:
                result = dfs_recursive(child, path + [(child, "فرزند")])
                if result:
                    return result
            
            # بررسی همسر
            if current.spouse:
                result = dfs_recursive(current.spouse, path + [(current.spouse, "همسر")])
                if result:
                    return result
            
            return None
        
        return dfs_recursive(self.people[start_id], [(self.people[start_id], "شروع")])
    
    def simplify_relationship(self, path: List[Tuple[Person, str]], start_person: Person) -> str:
        """ساده‌سازی مسیر به نسبت‌های فارسی"""
        if not path or len(path) <= 1:
            return "خود"
        
        # حذف گره شروع
        relations = [rel for _, rel in path[1:]]
        people = [person for person, _ in path]
        
        # تحلیل مسیر
        return self._analyze_persian_relationship(relations, people, start_person)
    
    def _analyze_persian_relationship(self, relations: List[str], people: List[Person], start_person: Person) -> str:
        """تحلیل و تبدیل مسیر به نسبت فارسی"""
        if not relations:
            return "خود"
        
        # ساده‌سازی مسیرهای مستقیم
        if len(relations) == 1:
            rel = relations[0]
            target = people[-1]
            
            if rel == "والد":
                if target.gender == Gender.MALE:
                    return "پدر"
                else:
                    return "مادر"
            elif rel == "فرزند":
                if target.gender == Gender.MALE:
                    return "پسر"
                else:
                    return "دختر"
            elif rel == "همسر":
                if target.gender == Gender.MALE:
                    return "شوهر"
                else:
                    return "همسر"
        
        # ساده‌سازی مسیرهای دو مرحله‌ای
        if len(relations) == 2:
            return self._two_step_relationship(relations, people, start_person)
        
        # ساده‌سازی مسیرهای پیچیده‌تر
        if len(relations) >= 3:
            return self._multi_step_relationship(relations, people, start_person)
        
        return " -> ".join(relations)
    
    def _two_step_relationship(self, relations: List[str], people: List[Person], start_person: Person) -> str:
        """تحلیل نسبت‌های دو مرحله‌ای"""
        rel1, rel2 = relations
        target = people[-1]
        middle = people[1]
        
        # والد -> والد
        if rel1 == "والد" and rel2 == "والد":
            if target.gender == Gender.MALE:
                return "پدربزرگ" if middle.gender == Gender.MALE else "پدربزرگ مادری"
            else:
                return "مادربزرگ" if middle.gender == Gender.MALE else "مادربزرگ مادری"
        
        # والد -> فرزند (برادر/خواهر)
        if rel1 == "والد" and rel2 == "فرزند":
            if target.id == start_person.id:
                return "خود"
            if target.gender == Gender.MALE:
                return "برادر"
            else:
                return "خواهر"
        
        # فرزند -> فرزند (نوه)
        if rel1 == "فرزند" and rel2 == "فرزند":
            if target.gender == Gender.MALE:
                return "نوه پسر"
            else:
                return "نوه دختر"
        
        # والد -> همسر
        if rel1 == "والد" and rel2 == "همسر":
            if middle.gender == Gender.MALE:
                return "مادر" if target.gender == Gender.FEMALE else "پدر"
            else:
                return "پدر" if target.gender == Gender.MALE else "مادر"
        
        # همسر -> والد
        if rel1 == "همسر" and rel2 == "والد":
            if target.gender == Gender.MALE:
                return "پدر همسر" if start_person.gender == Gender.MALE else "پدر شوهر"
            else:
                return "مادر همسر" if start_person.gender == Gender.MALE else "مادر شوهر"
        
        # همسر -> فرزند
        if rel1 == "همسر" and rel2 == "فرزند":
            if target.gender == Gender.MALE:
                return "پسر همسر" if start_person.gender == Gender.MALE else "پسر شوهر"
            else:
                return "دختر همسر" if start_person.gender == Gender.MALE else "دختر شوهر"
        
        # فرزند -> همسر
        if rel1 == "فرزند" and rel2 == "همسر":
            child = middle
            if child.gender == Gender.MALE:
                return "عروس" if target.gender == Gender.FEMALE else "داماد"
            else:
                return "داماد" if target.gender == Gender.MALE else "عروس"
        
        return f"{rel1} -> {rel2}"
    
    def _multi_step_relationship(self, relations: List[str], people: List[Person], start_person: Person) -> str:
        """تحلیل نسبت‌های چند مرحله‌ای پیچیده"""
        target = people[-1]
        
        # والد -> والد -> فرزند (عمو، دایی، عمه، خاله)
        if len(relations) == 3 and relations[0] == "والد" and relations[1] == "والد" and relations[2] == "فرزند":
            grandparent = people[1]
            parent_sibling = people[3]
            
            if grandparent.gender == Gender.MALE:  # پدربزرگ
                if parent_sibling.gender == Gender.MALE:
                    return "عمو"
                else:
                    return "عمه"
            else:  # مادربزرگ
                if parent_sibling.gender == Gender.MALE:
                    return "دایی"
                else:
                    return "خاله"
        
        # والد -> فرزند -> فرزند (خواهرزاده، برادرزاده)
        if len(relations) == 3 and relations[0] == "والد" and relations[1] == "فرزند" and relations[2] == "فرزند":
            sibling = people[2]
            
            if sibling.gender == Gender.MALE:
                if target.gender == Gender.MALE:
                    return "پسر برادر"
                else:
                    return "دختر برادر"
            else:
                if target.gender == Gender.MALE:
                    return "پسر خواهر"
                else:
                    return "دختر خواهر"
        
        # والد -> والد -> فرزند -> فرزند (پسر/دختر عمو، دایی، عمه، خاله)
        if len(relations) == 4 and relations[:2] == ["والد", "والد"] and relations[2:] == ["فرزند", "فرزند"]:
            grandparent = people[1]
            parent_sibling = people[3]
            
            gender_prefix = "پسر" if target.gender == Gender.MALE else "دختر"
            
            if grandparent.gender == Gender.MALE:
                if parent_sibling.gender == Gender.MALE:
                    return f"{gender_prefix} عمو"
                else:
                    return f"{gender_prefix} عمه"
            else:
                if parent_sibling.gender == Gender.MALE:
                    return f"{gender_prefix} دایی"
                else:
                    return f"{gender_prefix} خاله"
        
        # همسر -> والد -> فرزند (برادر/خواهر شوهر/زن)
        if len(relations) == 3 and relations[0] == "همسر" and relations[1] == "والد" and relations[2] == "فرزند":
            spouse_sibling = people[3]
            spouse_gender = people[1].gender
            
            if spouse_gender == Gender.MALE:  # شوهر
                if spouse_sibling.gender == Gender.MALE:
                    return "برادر شوهر"
                else:
                    return "خواهر شوهر"
            else:  # زن
                if spouse_sibling.gender == Gender.MALE:
                    return "برادر زن"
                else:
                    return "خواهر زن"
        
        # مسیر پیچیده - نمایش مرحله به مرحله
        simple_path = []
        for i, rel in enumerate(relations):
            if i < len(people) - 1:
                person = people[i + 1]
                if rel == "والد":
                    simple_path.append("پدر" if person.gender == Gender.MALE else "مادر")
                elif rel == "فرزند":
                    simple_path.append("پسر" if person.gender == Gender.MALE else "دختر")
                elif rel == "همسر":
                    simple_path.append("همسر")
        
        return " ← ".join(simple_path)
    
    def get_all_people(self) -> List[Dict]:
        """دریافت لیست تمام افراد"""
        return [person.to_dict() for person in self.people.values()]
    
    def export_to_dict(self) -> Dict:
        """صادرات درخت به فرمت دیکشنری"""
        return {
            "people": self.get_all_people()
        }
