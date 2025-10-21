import os, json, re
from dotenv import load_dotenv
from openai import OpenAI
from models.products import Product

load_dotenv()

# === AI MODEL CONFIGURATION ===
API_KEY = os.getenv("OPENAI_API_KEY")
BASE_URL = os.getenv("BASE_URL", "https://models.github.ai/inference")
MODEL = os.getenv("MODEL", "openai/gpt-4.1")

if not API_KEY:
    raise ValueError("Missing OPENAI_API_KEY in .env")

client = OpenAI(base_url=BASE_URL, api_key=API_KEY)

# === TOOL METHODS ===
def get_all_products():
    """Return a list of all available products with basic info."""
    products = Product.objects()
    return [{"name": p.title, "price": p.price, "tags": p.tags} for p in products]


def get_product_info(name: str):
    """Return details about a product by name."""
    product = Product.objects(title__icontains=name).first()
    if not product:
        return f"No product found matching '{name}'."
    return {
        "name": product.title,
        "description": product.description,
        "price": product.price,
        "tags": product.tags,
    }


def get_convenient_price_for_client(budget: float):
    """Suggest an ideal price range based on the user's budget."""
    if budget <= 0:
        return "Invalid budget amount."
    low, high = round(budget * 0.8, 2), round(budget * 1.2, 2)
    return {
        "range": [low, high],
        "summary": f"For a budget of ${budget}, products priced between ${low} and ${high} are considered convenient.",
    }


def get_products_with_convenient_price(budget: float):
    """Return products within ±20% of the given budget."""
    if budget <= 0:
        return "Invalid budget value."

    low, high = budget * 0.8, budget * 1.2
    products = Product.objects(price__gte=low, price__lte=high)
    if not products:
        return f"No products found in the range ${low:.2f}–${high:.2f}."
    return [{"name": p.title, "price": p.price, "tags": p.tags} for p in products]


def analyze_budget(budget: float):
    """Compare the user's budget with the average market price."""
    prices = [p.price for p in Product.objects()]
    if not prices:
        return "No products in the database yet."

    avg = sum(prices) / len(prices)
    if budget > avg:
        return f"Your budget (${budget}) is above the average product price (${avg:.2f}), you can afford premium products."
    elif budget < avg:
        return f"Your budget (${budget}) is below average (${avg:.2f}), look for budget-friendly items."
    else:
        return f"Your budget matches the average price (${avg:.2f})."


# === MAIN AI AGENT CONTROLLER ===
def ai_agent_chat(prompt: str) -> str:
    tools = [
        {
            "type": "function",
            "function": {
                "name": "get_all_products",
                "description": "Get a list of all available products with name, price, and tags.",
                "parameters": {"type": "object", "properties": {}},
            },
        },
        {
            "type": "function",
            "function": {
                "name": "get_product_info",
                "description": "Retrieve details about a specific product by name.",
                "parameters": {
                    "type": "object",
                    "properties": {"name": {"type": "string"}},
                    "required": ["name"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "get_convenient_price_for_client",
                "description": "Suggest an ideal price range based on the client's budget.",
                "parameters": {
                    "type": "object",
                    "properties": {"budget": {"type": "number"}},
                    "required": ["budget"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "get_products_with_convenient_price",
                "description": "Find products within ±20% of a given budget.",
                "parameters": {
                    "type": "object",
                    "properties": {"budget": {"type": "number"}},
                    "required": ["budget"],
                },
            },
        },
    ]

    messages = [
        {
            "role": "system",
            "content": (
                "You are an intelligent product advisor that helps clients find "
                "products and pricing that match their budget and preferences."
            ),
        },
        {"role": "user", "content": prompt},
    ]

    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        tools=tools,
        tool_choice="auto",
    )

    message = response.choices[0].message
    tool_calls = getattr(message, "tool_calls", None)

    if tool_calls:
        messages.append(message)
        for tool_call in tool_calls:
            name = tool_call.function.name
            args = json.loads(tool_call.function.arguments or "{}")

            if name == "get_all_products":
                result = get_all_products()
            elif name == "get_product_info":
                result = get_product_info(args.get("name", ""))
            elif name == "get_convenient_price_for_client":
                result = get_convenient_price_for_client(args.get("budget", 0))
            elif name == "get_products_with_convenient_price":
                result = get_products_with_convenient_price(args.get("budget", 0))
            else:
                result = {"error": f"Unknown tool: {name}"}

            messages.append(
                {
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": name,
                    "content": json.dumps(result),
                }
            )

        final = client.chat.completions.create(model=MODEL, messages=messages)
        return final.choices[0].message.content.strip()

    match = re.search(r"(\d+(\.\d+)?)", prompt)
    if match:
        budget = float(match.group(1))
        suggestion = analyze_budget(budget)
        products = get_products_with_convenient_price(budget)
        return f"{suggestion}\n\nAffordable products:\n{json.dumps(products, indent=2)}"

    return message.content.strip()
