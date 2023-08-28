{
    'super_admin': {
        'iam': ['*'],
        'store': ["*"]
    },
    'iam_admin': {
        'iam': ['*'],
        'store': ["*"]
    },
    'store_admin': {
        'store': ['*']
    },
    'store_customer': {
        'store': ['get_items', 'create_order', 'delete_order', 'add_item_to_cart', 'add_address']
    },
    'store_manager':{
        'store': ['add_cateogry']
    },
    'store_manager':{
        'store': ['add_cateogry']
    },
    'vendor' : {
        'inventory': ['add_item']
    }
    
    
}



'''class PermissionMiddleware:
    async def __call__(self, request: Request, call_next):
        # Get the JWT token from the request headers
        auth_header = request.headers.get("Authorization")

        if not auth_header or "Bearer" not in auth_header:
            raise HTTPException(status_code=401, detail="Unauthorized")

        token = auth_header.split(" ")[1]

        try:
            # Decode the JWT token to obtain user's permissions
            payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
            user_permissions = payload["permissions"]

            # Define the required permission based on the requested URL
            path = request.url.path
            required_permission = None
            if path.startswith("/products"):
                required_permission = "manage_products"
            elif path.startswith("/orders"):
                required_permission = "manage_orders"
            # Add more conditions to map URLs to permissions

            if required_permission and not user_has_permission(user_permissions, required_permission):
                raise HTTPException(status_code=403, detail="Forbidden: Insufficient permissions")
        except jwt.PyJWTError:
            raise HTTPException(status_code=401, detail="Unauthorized")

        response = await call_next(request)
        return response

app.middleware("http")(PermissionMiddleware())'''



permissions_dict = {
    "admin": [
        "create_product",
        "edit_product",
        "delete_product",
        "view_products",
        "manage_orders",
        "manage_users",
        "view_reports",
        "manage_coupons",
        "manage_store",
        "manage_customer_support",
    ],
    "store_manager": [
        "create_product",
        "edit_product",
        "view_products",
        "manage_orders",
        "manage_users",
        "view_reports",
        "manage_coupons",
        "manage_store",
    ],
    "customer_support": [
        "view_products",
        "manage_orders",
        "manage_users",
        "manage_customer_support",
    ],
    "content_editor": [
        "create_product",
        "edit_product",
        "view_products",
    ],
    "marketing": [
        "view_products",
        "manage_orders",
        "view_reports",
        "manage_coupons",
    ],
    "customer": [
        "view_products",
        "create_order",
        "edit_order",
        "view_own_orders",
    ],
}

    # accountant: [
    #     { action: ['list', 'show'], resource: 'products' },
    #     { action: 'read', resource: 'products.*' },
    #     { type: 'deny', action: 'read', resource: 'products.description' },
    #     { action: 'list', resource: 'categories' },
    #     { action: 'read', resource: 'categories.*' },
    #     { action: ['list', 'show'], resource: 'customers' },
    #     { action: 'read', resource: 'customers.*' },
    #     { action: '*', resource: 'invoices' },
    # ],
