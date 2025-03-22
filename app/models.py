from typing import Optional
from datetime import datetime, timezone
from app import db
import sqlalchemy as sa
import sqlalchemy.orm as so
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64), unique=True, index=True, nullable=False)
    email: so.Mapped[str] = so.mapped_column(sa.String(120), unique=True, index=True, nullable=False)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))
    #role: so.Mapped[int] = so.mapped_column(sa.SmallInteger, nullable=False)

    custom_courses: so.WriteOnlyMapped['UserCourse'] = so.relationship(back_populates='author')

    courses: so.WriteOnlyMapped['Course'] = so.relationship(back_populates='author_course')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)


    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'User <{self.username}>'


class Course(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    title: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, nullable=False)
    description: so.Mapped[str] = so.mapped_column(sa.Text, index=True, nullable=False)
    user_ref_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id), index=True)

    author_course: so.Mapped[User] = so.relationship(back_populates='courses')
    user_courses: so.WriteOnlyMapped['UserCourse'] = so.relationship(back_populates='original_course')

    def __repr__(self):
        return f'Course <{self.title}>'


class UserCourse(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, nullable=False)
    description: so.Mapped[str] = so.mapped_column(sa.Text, index=True, nullable=False)
    timestamp: so.Mapped[datetime] = so.mapped_column(index=True, default=lambda: datetime.now(timezone.utc))
    progress: so.Mapped[str] = so.mapped_column(sa.SmallInteger)
    user_ref_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id), index=True)
    course_ref_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Course.id), index=True)

    author_custom_course: so.Mapped[User] = so.relationship(back_populates='custom_courses')
    original_course: so.Mapped[Course] = so.relationship(back_populates='user_courses')

    def __repr__(self):
        return f"User's Course <{self.name}>"
