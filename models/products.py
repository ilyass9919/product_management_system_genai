from mongoengine import Document, StringField, FloatField, DateTimeField, ReferenceField, BooleanField, ListField
from datetime import datetime
from .users import User


class Product(Document):
    # Core fields
    title = StringField(required=True, min_length=3, max_length=100)
    description = StringField()
    category = StringField(default="General")
    price = FloatField(required=True, min_value=0.0)
    is_active = BooleanField(default=True)
    # Relationships
    owner = ReferenceField(User, required=False)  # The user who created or manages the product
    # Optional metadata
    tags = ListField(StringField(), default=list)
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)

    # MongoDB collection settings
    meta = {
        'collection': 'products',
        'indexes': [
            'title',
            'category',
            'price',
            'is_active',
            'created_at'
        ]
    }

    # Override save() to auto-update timestamp
    def save(self, *args, **kwargs):
        self.updated_at = datetime.utcnow()
        return super(Product, self).save(*args, **kwargs)

    # Helper methods
    def to_dict(self):
        """Return a clean JSON-safe dictionary."""
        return {
            "id": str(self.id),
            "title": self.title,
            "description": self.description,
            "category": self.category,
            "price": self.price,
            "tags": self.tags,
            "is_active": self.is_active,
            "owner": str(self.owner.id) if self.owner else None,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }

    def __str__(self):
        """Readable representation for logs or admin panels."""
        return f"{self.title} (${self.price})"
