AI_PRODUCT_MANAGEMENT_SYSTEM/
│
├── app.py
├── .env
├── requirements.txt
│
├── models/
│   ├── __init__.py
│   ├── users.py
│   └── products.py
│   
├── controllers/
│   ├── __init__.py
│   ├── user_controller.py
│   └── product_controller.py
│   |__ ai_agent_controller.py
├── routes/
│   ├── web_routes.py
│   ├── auth.py
│   └── products.py
│   |__ ai_routes.py
├── middlewares/
│   ├── __init__.py
│   └── auth_middleware.py
│   |__ chack_password.py
|
|__ utils
|    |__ generate_token.py   
|    |__ openai_client.py
|   
└── templates/
    ├── base.html
    ├── login.html
    ├── register.html
    ├── products/
        ├── list.html
        ├── create.html
        ├── edit.html
