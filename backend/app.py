"""
سرور بک‌اند Flask برای API شجره‌نامه
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from family_tree import FamilyTree, Gender
import json

app = Flask(__name__)
CORS(app)

# ایجاد نمونه درخت خانوادگی
family_tree = FamilyTree()


@app.route('/api/health', methods=['GET'])
def health_check():
    """بررسی سلامت سرور"""
    return jsonify({"status": "healthy", "message": "سرور شجره‌نامه فعال است"})


@app.route('/api/people', methods=['GET'])
def get_all_people():
    """دریافت لیست تمام افراد"""
    try:
        people = family_tree.get_all_people()
        return jsonify({"success": True, "data": people})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/person', methods=['POST'])
def add_person():
    """افزودن فرد جدید"""
    try:
        data = request.json
        person = family_tree.add_person(
            person_id=data['id'],
            name=data['name'],
            gender=data['gender'],
            birth_year=data.get('birth_year')
        )
        return jsonify({
            "success": True,
            "message": f"فرد {data['name']} با موفقیت اضافه شد",
            "data": person.to_dict()
        })
    except ValueError as e:
        return jsonify({"success": False, "error": str(e)}), 400
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/person/<person_id>', methods=['DELETE'])
def delete_person(person_id):
    """حذف فرد"""
    try:
        success = family_tree.remove_person(person_id)
        if success:
            return jsonify({
                "success": True,
                "message": f"فرد با شناسه {person_id} با موفقیت حذف شد"
            })
        else:
            return jsonify({
                "success": False,
                "error": "فرد مورد نظر یافت نشد"
            }), 404
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/relationship/parent-child', methods=['POST'])
def add_parent_child_relationship():
    """افزودن رابطه والد-فرزند"""
    try:
        data = request.json
        family_tree.add_parent_child(data['parent_id'], data['child_id'])
        return jsonify({
            "success": True,
            "message": "رابطه والد-فرزند با موفقیت اضافه شد"
        })
    except ValueError as e:
        return jsonify({"success": False, "error": str(e)}), 400
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/relationship/spouse', methods=['POST'])
def add_spouse_relationship():
    """افزودن رابطه همسری"""
    try:
        data = request.json
        family_tree.add_spouse(data['person1_id'], data['person2_id'])
        return jsonify({
            "success": True,
            "message": "رابطه همسری با موفقیت اضافه شد"
        })
    except ValueError as e:
        return jsonify({"success": False, "error": str(e)}), 400
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/path/bfs', methods=['POST'])
def find_path_bfs():
    """پیدا کردن مسیر با BFS"""
    try:
        data = request.json
        start_id = data['start_id']
        end_id = data['end_id']
        
        path = family_tree.bfs_find_path(start_id, end_id)
        
        if path is None:
            return jsonify({
                "success": False,
                "error": "مسیری بین این دو فرد یافت نشد"
            }), 404
        
        start_person = family_tree.people[start_id]
        simplified = family_tree.simplify_relationship(path, start_person)
        
        path_data = [
            {
                "id": person.id,
                "name": person.name,
                "relation": relation
            }
            for person, relation in path
        ]
        
        return jsonify({
            "success": True,
            "data": {
                "algorithm": "BFS (جستجوی سطح به سطح)",
                "path": path_data,
                "simplified_relationship": simplified,
                "path_length": len(path) - 1
            }
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/path/dfs', methods=['POST'])
def find_path_dfs():
    """پیدا کردن مسیر با DFS"""
    try:
        data = request.json
        start_id = data['start_id']
        end_id = data['end_id']
        
        path = family_tree.dfs_find_path(start_id, end_id)
        
        if path is None:
            return jsonify({
                "success": False,
                "error": "مسیری بین این دو فرد یافت نشد"
            }), 404
        
        start_person = family_tree.people[start_id]
        simplified = family_tree.simplify_relationship(path, start_person)
        
        path_data = [
            {
                "id": person.id,
                "name": person.name,
                "relation": relation
            }
            for person, relation in path
        ]
        
        return jsonify({
            "success": True,
            "data": {
                "algorithm": "DFS (جستجوی عمقی)",
                "path": path_data,
                "simplified_relationship": simplified,
                "path_length": len(path) - 1
            }
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/path/compare', methods=['POST'])
def compare_paths():
    """مقایسه مسیرهای BFS و DFS"""
    try:
        data = request.json
        start_id = data['start_id']
        end_id = data['end_id']
        
        bfs_path = family_tree.bfs_find_path(start_id, end_id)
        dfs_path = family_tree.dfs_find_path(start_id, end_id)
        
        if bfs_path is None or dfs_path is None:
            return jsonify({
                "success": False,
                "error": "مسیری بین این دو فرد یافت نشد"
            }), 404
        
        start_person = family_tree.people[start_id]
        
        bfs_simplified = family_tree.simplify_relationship(bfs_path, start_person)
        dfs_simplified = family_tree.simplify_relationship(dfs_path, start_person)
        
        bfs_data = [
            {"id": p.id, "name": p.name, "relation": r}
            for p, r in bfs_path
        ]
        
        dfs_data = [
            {"id": p.id, "name": p.name, "relation": r}
            for p, r in dfs_path
        ]
        
        return jsonify({
            "success": True,
            "data": {
                "bfs": {
                    "algorithm": "BFS (جستجوی سطح به سطح)",
                    "path": bfs_data,
                    "simplified_relationship": bfs_simplified,
                    "path_length": len(bfs_path) - 1
                },
                "dfs": {
                    "algorithm": "DFS (جستجوی عمقی)",
                    "path": dfs_data,
                    "simplified_relationship": dfs_simplified,
                    "path_length": len(dfs_path) - 1
                },
                "same_path": bfs_simplified == dfs_simplified
            }
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/sample-data', methods=['POST'])
def load_sample_data():
    """بارگذاری داده‌های نمونه"""
    try:
        # پاک کردن داده‌های قبلی
        family_tree.people.clear()
        
        # جد بزرگ
        family_tree.add_person("p1", "احمد", "male", 1920)
        family_tree.add_person("p2", "فاطمه", "female", 1925)
        family_tree.add_spouse("p1", "p2")
        
        # نسل دوم
        family_tree.add_person("p3", "حسن", "male", 1945)
        family_tree.add_person("p4", "زهرا", "female", 1950)
        family_tree.add_person("p5", "علی", "male", 1948)
        family_tree.add_person("p6", "مریم", "female", 1952)
        
        family_tree.add_parent_child("p1", "p3")
        family_tree.add_parent_child("p2", "p3")
        family_tree.add_parent_child("p1", "p5")
        family_tree.add_parent_child("p2", "p5")
        
        family_tree.add_spouse("p3", "p4")
        family_tree.add_spouse("p5", "p6")
        
        # نسل سوم
        family_tree.add_person("p7", "محمد", "male", 1970)
        family_tree.add_person("p8", "سارا", "female", 1972)
        family_tree.add_person("p9", "رضا", "male", 1975)
        family_tree.add_person("p10", "نرگس", "female", 1978)
        
        family_tree.add_parent_child("p3", "p7")
        family_tree.add_parent_child("p4", "p7")
        family_tree.add_parent_child("p3", "p8")
        family_tree.add_parent_child("p4", "p8")
        
        family_tree.add_parent_child("p5", "p9")
        family_tree.add_parent_child("p6", "p9")
        family_tree.add_parent_child("p5", "p10")
        family_tree.add_parent_child("p6", "p10")
        
        # همسران نسل سوم
        family_tree.add_person("p11", "لیلا", "female", 1972)
        family_tree.add_person("p12", "کامران", "male", 1970)
        
        family_tree.add_spouse("p7", "p11")
        family_tree.add_spouse("p8", "p12")
        
        # نسل چهارم
        family_tree.add_person("p13", "امیر", "male", 1995)
        family_tree.add_person("p14", "نیلوفر", "female", 1998)
        family_tree.add_person("p15", "سینا", "male", 1997)
        
        family_tree.add_parent_child("p7", "p13")
        family_tree.add_parent_child("p11", "p13")
        family_tree.add_parent_child("p7", "p14")
        family_tree.add_parent_child("p11", "p14")
        
        family_tree.add_parent_child("p8", "p15")
        family_tree.add_parent_child("p12", "p15")
        
        return jsonify({
            "success": True,
            "message": "داده‌های نمونه با موفقیت بارگذاری شد",
            "data": family_tree.get_all_people()
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/export', methods=['GET'])
def export_tree():
    """صادرات درخت"""
    try:
        return jsonify({
            "success": True,
            "data": family_tree.export_to_dict()
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


if __name__ == '__main__':
    print("🌳 سرور شجره‌نامه در حال اجرا...")
    print("📍 آدرس: http://localhost:5000")
    print("📚 API Documentation:")
    print("  GET  /api/health - بررسی سلامت سرور")
    print("  GET  /api/people - دریافت تمام افراد")
    print("  POST /api/person - افزودن فرد جدید")
    print("  DELETE /api/person/<id> - حذف فرد")
    print("  POST /api/relationship/parent-child - افزودن رابطه والد-فرزند")
    print("  POST /api/relationship/spouse - افزودن رابطه همسری")
    print("  POST /api/path/bfs - پیدا کردن مسیر با BFS")
    print("  POST /api/path/dfs - پیدا کردن مسیر با DFS")
    print("  POST /api/path/compare - مقایسه مسیرهای BFS و DFS")
    print("  POST /api/sample-data - بارگذاری داده نمونه")
    print("  GET  /api/export - صادرات درخت")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
