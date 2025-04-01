from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import string
import random
db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.Text(), nullable=False)
    role = db.Column(db.String(20), default='user')  # admin hoặc user
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.now())

    def __repr__(self) -> str:
        return f'User>>> {self.username}'


class Menu(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))  # Tối đa 2 title, ngăn cách bằng dấu chấm phẩy
    menu_name = db.Column(db.String(50), nullable=False)
    menu_url = db.Column(db.String(100), nullable=False)
    menu_order = db.Column(db.Integer, default=0)  # Thứ tự hiển thị menu
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.now())


class About(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)  # Tối đa 5 content, ngăn cách bằng dấu chấm phẩy
    image = db.Column(db.String(200))  # URL của hình ảnh
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.now())


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)  # Thêm title cho project
    image = db.Column(db.String(200))
    description = db.Column(db.Text, nullable=False)
    project_url = db.Column(db.String(200))  # URL của project (nếu có)
    github_url = db.Column(db.String(200))  # URL GitHub (nếu có)
    technologies = db.Column(db.String(200))  # Công nghệ sử dụng
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.now())


class Skill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    skill_name = db.Column(db.String(100), nullable=False)
    icon_skill = db.Column(db.String(200))  # URL của icon
    short_desc = db.Column(db.String(200))
    proficiency = db.Column(db.Integer)  # Mức độ thành thạo (%)
    category = db.Column(db.String(50))  # Phân loại skill (Frontend, Backend, etc.)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.now())


class Experience(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(200), nullable=False)
    role_name = db.Column(db.String(200), nullable=False)
    desc_role = db.Column(db.Text)  # Mô tả được ngăn cách bằng dấu chấm phẩy
    company_location = db.Column(db.String(200))  # Thêm địa điểm công ty
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date)
    is_current = db.Column(db.Boolean, default=False)  # Đánh dấu công việc hiện tại
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.now())


class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    subject = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default='pending')  # Trạng thái: pending, replied, spam
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.now())