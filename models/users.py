from mongoengine import Document, StringField, DateTimeField, BooleanField
from datetime import datetime
import bcrypt

class User(Document):

    # Schema fields
    username = StringField(required=True, unique=True, min_length=3, max_length=50)
    name = StringField(required=True)
    email = StringField(required=True, unique=True)
    password_hash = StringField(required=True)
    role = StringField(default="client", choices=["admin", "client"])
    is_active = BooleanField(default=True)
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)

    # MongoDB collection settings
    meta = {
        'collection': 'users',
        'indexes': [
            'email',
            'username', 
            'role',
            'created_at'
        ]
    }

    # Helper methods for password handling
    def set_password(self, password):
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))
    
    # Auto-update updated_at timestamp
    def save(self, *args, **kwargs):
        self.updated_at = datetime.utcnow()
        return super(User, self).save(*args, **kwargs)
    
    # for safe API responses

    def to_dict(self):
        return {
            "id": str(self.id),
            "username": self.username,
            "name": self.name,
            "email": self.email,
            "role": self.role,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
    }

    def __str__(self):
        return f"{self.username} ({self.role})"