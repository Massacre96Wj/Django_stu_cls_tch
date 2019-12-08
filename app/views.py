from django.shortcuts import HttpResponse, redirect, render
import pymysql, json
from utils.sqlhepler import get_list, modify, get_one

def classes(request):
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='123', db='django')
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute("select id, title from class")
    class_list = cursor.fetchall()
    cursor.close()
    conn.close()

    return render(request, 'classes.html', {'class_list' : class_list})

def add_class(request):
    if request.method == "GET":
        return render(request, 'add_class.html')
    else:
        print(request.POST)
        v = request.POST.get('title')
        print(v)
        if len(v)>0:
            conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='123', db='django')
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            cursor.execute("insert into class(title) values (%s)", [v, ])
            conn.commit()
            cursor.close()
            conn.close()
            return redirect('/classes/')
        else:
            return render(request, 'add_class.html', {'message': '班级名称不能为空!!!'})

def modal_add_class(request):
    title = request.POST.get('title')
    print(title)
    if title:
        modify("insert into class(title) values (%s)", [title, ])
        return HttpResponse('ok')
    else:
        return HttpResponse("班级标题不能为空")

def del_class(request):
    nid = request.GET.get('nid')
    print(nid)

    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='123', db='django')
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute("delete from class where id=%s", [nid, ])
    conn.commit()
    cursor.close()
    conn.close()
    return redirect('/classes/')

def edit_class(request):
    if request.method == "GET":
        nid = request.GET.get('nid')
        print(nid)
        conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='123', db='django')
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("select id,title from class where id=%s", [nid, ])
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        print(result)
        return render(request, 'edit_class.html', {'result': result})
    else:
        nid = request.GET.get('nid')
        title = request.POST.get('title')

        conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='123', db='django')
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("update class set title=%s where id=%s", [title, nid])
        conn.commit()
        cursor.close()
        conn.close()

        return redirect('/classes/')

def students(request):
    '''
    学生列表
    :param request: 封装请求信息
    :return:
    '''
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='123', db='django')
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute("select student.id, student.name, class.title from student left join class on student.class_id=class.id")
    student_list = cursor.fetchall()
    # print(student_list)
    cursor.close()
    conn.close()

    class_list = get_list("select id, title from class", [])
    return render(request, 'students.html', {"student_list": student_list, "class_list": class_list})

def add_student(request):
    if request.method == "GET":
        conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='123', db='django')
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("select id, title from class")
        class_list = cursor.fetchall()
        cursor.close()
        conn.close()

        return render(request, 'add_student.html', {'class_list': class_list})
    else:
        name = request.POST.get('student_name')
        class_id = request.POST.get('class_id')
        print(name, class_id)

        conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='123', db='django')
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("insert into student(name, class_id) values (%s, %s)", [name, class_id,])
        conn.commit()
        cursor.close()
        conn.close()

        return redirect('/students/')

def edit_student(request):
    if request.method == 'GET':
        nid = request.GET.get('nid')
        class_list = get_list("select id,title from class",[])
        current_student_info = get_one('select id,name,class_id from student where id=%s', [nid, ])
        return render(request, 'edit_student.html', {'class_list': class_list, 'current_student_info': current_student_info})
    else:
        id = request.GET.get('nid')
        name = request.POST.get('student_name')
        class_id = request.POST.get('class_id')
        modify("update student set name=%s,class_id=%s where id=%s",[name, class_id, id])
        return redirect('/students')

def del_student(request):

    id = request.GET.get('nid')
    print(id)

    modify("delete from student where id=%s", [id, ])
    return redirect('/students/')

def modal_add_student(request):
    ret = {'status': True, 'message': None}
    try:
        name = request.POST.get('name')
        class_id = request.POST.get('class_id')
        print(name, class_id)
        modify("insert into student(name, class_id) values(%s, %s)", [name, class_id, ])
    except Exception as e:
        ret['status'] = False
        ret['message'] = str(e)
        print(e)
    return HttpResponse(json.dumps(ret))

# 多对多
def teachers(request):
    # teacher_list = get_list('select id, name from teachers', [])
    teacher_list = get_list("""
            SELECT t.id, t.name,c.title FROM teachers t
            LEFT JOIN teacher2class tc
            ON t.id = tc.teacher_id
            LEFT JOIN class c
            ON c.id = tc.class_id;  
    """, [])
    print(teacher_list)
    result = {}
    for teacher in teacher_list:
        id = teacher['id']
        if id in result:
            result[id]['title'].append(teacher['title'])
        else:
            result[id] = {'id': teacher['id'], 'name': teacher['name'], 'title': [teacher['title']]}
    print(result)

    return render(request, "teachers.html", {"teacher_list": result.values()})

