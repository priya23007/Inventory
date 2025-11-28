def individual_data(todo):
    return{
        "item_id": str(todo["_id"]),
        "item_name": todo["item_name"],
        "category": todo["category"],
        "quantity": todo["quantity"]
    }

def all_task(todos):
    return[individual_data(todo) for todo in todos ]