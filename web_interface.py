#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
智能学习系统Web界面
"""

from flask import Flask, render_template, request, jsonify
import json
import os
from smart_learning_system import LearningSystem

app = Flask(__name__)
system = LearningSystem()

# 首页
@app.route('/')
def index():
    return render_template('index.html')

# 创建学生
@app.route('/api/students', methods=['POST'])
def create_student():
    data = request.json
    student_id = data.get('id')
    name = data.get('name')
    
    if not student_id or not name:
        return jsonify({'error': '缺少必要参数'}), 400
    
    student = system.create_student(student_id, name)
    return jsonify(student), 201

# 构建学习画像
@app.route('/api/students/<student_id>/profile', methods=['POST'])
def build_profile(student_id):
    data = request.json
    dialogue = data.get('dialogue', [])
    
    if not dialogue:
        return jsonify({'error': '缺少对话内容'}), 400
    
    profile = system.build_profile(student_id, dialogue)
    return jsonify(profile), 200

# 生成学习资源
@app.route('/api/students/<student_id>/resources', methods=['POST'])
def generate_resources(student_id):
    data = request.json
    requirements = data.get('requirements', {})
    
    resources = system.generate_resources(student_id, requirements)
    return jsonify(resources), 200

# 规划学习路径
@app.route('/api/students/<student_id>/path', methods=['GET'])
def get_learning_path(student_id):
    path = system.plan_learning_path(student_id)
    return jsonify(path), 200

# 获取智能辅导
@app.route('/api/students/<student_id>/tutor', methods=['POST'])
def get_tutoring(student_id):
    data = request.json
    question = data.get('question')
    
    if not question:
        return jsonify({'error': '缺少问题内容'}), 400
    
    tutoring = system.get_tutoring(student_id, question)
    return jsonify(tutoring), 200

# 评估学习效果
@app.route('/api/students/<student_id>/assessment', methods=['GET'])
def get_assessment(student_id):
    assessment = system.assess_learning(student_id)
    return jsonify(assessment), 200

# 获取学生信息
@app.route('/api/students/<student_id>', methods=['GET'])
def get_student(student_id):
    if student_id in system.students:
        return jsonify(system.students[student_id]), 200
    else:
        return jsonify({'error': '学生不存在'}), 404

if __name__ == '__main__':
    # 确保templates目录存在
    if not os.path.exists('templates'):
        os.makedirs('templates')
        
        # 创建index.html模板
        index_html = '''
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>智能学习系统</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: Arial, sans-serif;
            background-color: #f5f5f5;
            color: #333;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }
        
        h1 {
            color: #2c3e50;
            margin-bottom: 30px;
            text-align: center;
        }
        
        .card {
            background-color: white;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            padding: 20px;
            margin-bottom: 20px;
        }
        
        h2 {
            color: #3498db;
            margin-bottom: 15px;
        }
        
        .form-group {
            margin-bottom: 15px;
        }
        
        label {
            display: block;
            margin-bottom: 5px;
            font-weight: bold;
        }
        
        input, textarea, select {
            width: 100%;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 4px;
            font-size: 14px;
        }
        
        textarea {
            height: 100px;
            resize: vertical;
        }
        
        button {
            background-color: #3498db;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 4px;
            cursor: pointer;
            font-size: 14px;
        }
        
        button:hover {
            background-color: #2980b9;
        }
        
        .response {
            margin-top: 20px;
            padding: 15px;
            background-color: #e8f4f8;
            border-radius: 4px;
        }
        
        .response h3 {
            color: #2c3e50;
            margin-bottom: 10px;
        }
        
        .response pre {
            background-color: #f8f9fa;
            padding: 10px;
            border-radius: 4px;
            overflow-x: auto;
        }
        
        .nav {
            background-color: #2c3e50;
            color: white;
            padding: 10px 0;
            margin-bottom: 20px;
        }
        
        .nav ul {
            list-style: none;
            display: flex;
            justify-content: center;
        }
        
        .nav li {
            margin: 0 15px;
        }
        
        .nav a {
            color: white;
            text-decoration: none;
            font-weight: bold;
        }
        
        .nav a:hover {
            color: #3498db;
        }
    </style>
</head>
<body>
    <div class="nav">
        <ul>
            <li><a href="#">首页</a></li>
            <li><a href="#student">学生管理</a></li>
            <li><a href="#profile">学习画像</a></li>
            <li><a href="#resources">资源生成</a></li>
            <li><a href="#path">学习路径</a></li>
            <li><a href="#tutor">智能辅导</a></li>
            <li><a href="#assessment">学习评估</a></li>
        </ul>
    </div>
    
    <div class="container">
        <h1>智能学习系统</h1>
        
        <!-- 学生管理 -->
        <div id="student" class="card">
            <h2>学生管理</h2>
            <div class="form-group">
                <label for="student-id">学生ID</label>
                <input type="text" id="student-id" placeholder="请输入学生ID">
            </div>
            <div class="form-group">
                <label for="student-name">学生姓名</label>
                <input type="text" id="student-name" placeholder="请输入学生姓名">
            </div>
            <button onclick="createStudent()">创建学生</button>
            <div class="response" id="student-response"></div>
        </div>
        
        <!-- 学习画像 -->
        <div id="profile" class="card">
            <h2>学习画像构建</h2>
            <div class="form-group">
                <label for="profile-student-id">学生ID</label>
                <input type="text" id="profile-student-id" placeholder="请输入学生ID">
            </div>
            <div class="form-group">
                <label for="dialogue">对话内容（每行一条）</label>
                <textarea id="dialogue" placeholder="例如：我是计算机专业的学生\n我的学习目标是掌握机器学习"></textarea>
            </div>
            <button onclick="buildProfile()">构建画像</button>
            <div class="response" id="profile-response"></div>
        </div>
        
        <!-- 资源生成 -->
        <div id="resources" class="card">
            <h2>学习资源生成</h2>
            <div class="form-group">
                <label for="resource-student-id">学生ID</label>
                <input type="text" id="resource-student-id" placeholder="请输入学生ID">
            </div>
            <div class="form-group">
                <label for="course">课程名称</label>
                <input type="text" id="course" placeholder="例如：机器学习">
            </div>
            <div class="form-group">
                <label for="level">难度级别</label>
                <select id="level">
                    <option value="初级">初级</option>
                    <option value="中级">中级</option>
                    <option value="高级">高级</option>
                </select>
            </div>
            <button onclick="generateResources()">生成资源</button>
            <div class="response" id="resource-response"></div>
        </div>
        
        <!-- 学习路径 -->
        <div id="path" class="card">
            <h2>学习路径规划</h2>
            <div class="form-group">
                <label for="path-student-id">学生ID</label>
                <input type="text" id="path-student-id" placeholder="请输入学生ID">
            </div>
            <button onclick="getLearningPath()">获取学习路径</button>
            <div class="response" id="path-response"></div>
        </div>
        
        <!-- 智能辅导 -->
        <div id="tutor" class="card">
            <h2>智能辅导</h2>
            <div class="form-group">
                <label for="tutor-student-id">学生ID</label>
                <input type="text" id="tutor-student-id" placeholder="请输入学生ID">
            </div>
            <div class="form-group">
                <label for="question">问题</label>
                <textarea id="question" placeholder="例如：什么是线性回归？"></textarea>
            </div>
            <button onclick="getTutoring()">获取辅导</button>
            <div class="response" id="tutor-response"></div>
        </div>
        
        <!-- 学习评估 -->
        <div id="assessment" class="card">
            <h2>学习效果评估</h2>
            <div class="form-group">
                <label for="assessment-student-id">学生ID</label>
                <input type="text" id="assessment-student-id" placeholder="请输入学生ID">
            </div>
            <button onclick="getAssessment()">评估学习效果</button>
            <div class="response" id="assessment-response"></div>
        </div>
    </div>
    
    <script>
        // 创建学生
        function createStudent() {
            const studentId = document.getElementById('student-id').value;
            const studentName = document.getElementById('student-name').value;
            
            fetch('/api/students', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ id: studentId, name: studentName })
            })
            .then(response => response.json())
            .then(data => {
                document.getElementById('student-response').innerHTML = `
                    <h3>创建成功</h3>
                    <pre>${JSON.stringify(data, null, 2)}</pre>
                `;
            })
            .catch(error => {
                document.getElementById('student-response').innerHTML = `<h3>错误</h3><p>${error}</p>`;
            });
        }
        
        // 构建学习画像
        function buildProfile() {
            const studentId = document.getElementById('profile-student-id').value;
            const dialogue = document.getElementById('dialogue').value.split('\n').filter(line => line.trim() !== '');
            
            fetch(`/api/students/${studentId}/profile`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ dialogue: dialogue })
            })
            .then(response => response.json())
            .then(data => {
                document.getElementById('profile-response').innerHTML = `
                    <h3>学习画像</h3>
                    <pre>${JSON.stringify(data, null, 2)}</pre>
                `;
            })
            .catch(error => {
                document.getElementById('profile-response').innerHTML = `<h3>错误</h3><p>${error}</p>`;
            });
        }
        
        // 生成学习资源
        function generateResources() {
            const studentId = document.getElementById('resource-student-id').value;
            const course = document.getElementById('course').value;
            const level = document.getElementById('level').value;
            
            fetch(`/api/students/${studentId}/resources`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ 
                    requirements: { 
                        course: course, 
                        level: level, 
                        needs: ['理论讲解', '实践案例'] 
                    } 
                })
            })
            .then(response => response.json())
            .then(data => {
                document.getElementById('resource-response').innerHTML = `
                    <h3>生成的资源</h3>
                    <pre>${JSON.stringify(data, null, 2)}</pre>
                `;
            })
            .catch(error => {
                document.getElementById('resource-response').innerHTML = `<h3>错误</h3><p>${error}</p>`;
            });
        }
        
        // 获取学习路径
        function getLearningPath() {
            const studentId = document.getElementById('path-student-id').value;
            
            fetch(`/api/students/${studentId}/path`)
            .then(response => response.json())
            .then(data => {
                document.getElementById('path-response').innerHTML = `
                    <h3>学习路径</h3>
                    <pre>${JSON.stringify(data, null, 2)}</pre>
                `;
            })
            .catch(error => {
                document.getElementById('path-response').innerHTML = `<h3>错误</h3><p>${error}</p>`;
            });
        }
        
        // 获取智能辅导
        function getTutoring() {
            const studentId = document.getElementById('tutor-student-id').value;
            const question = document.getElementById('question').value;
            
            fetch(`/api/students/${studentId}/tutor`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ question: question })
            })
            .then(response => response.json())
            .then(data => {
                document.getElementById('tutor-response').innerHTML = `
                    <h3>智能辅导</h3>
                    <pre>${JSON.stringify(data, null, 2)}</pre>
                `;
            })
            .catch(error => {
                document.getElementById('tutor-response').innerHTML = `<h3>错误</h3><p>${error}</p>`;
            });
        }
        
        // 获取学习评估
        function getAssessment() {
            const studentId = document.getElementById('assessment-student-id').value;
            
            fetch(`/api/students/${studentId}/assessment`)
            .then(response => response.json())
            .then(data => {
                document.getElementById('assessment-response').innerHTML = `
                    <h3>学习评估</h3>
                    <pre>${JSON.stringify(data, null, 2)}</pre>
                `;
            })
            .catch(error => {
                document.getElementById('assessment-response').innerHTML = `<h3>错误</h3><p>${error}</p>`;
            });
        }
    </script>
</body>
</html>
        '''
        
        with open('templates/index.html', 'w', encoding='utf-8') as f:
            f.write(index_html)
    
    print("智能学习系统Web服务启动中...")
    print("访问地址: http://127.0.0.1:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)