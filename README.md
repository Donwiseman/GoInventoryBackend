# GO Inventory Manager Backend Application
This is the Backend application which manages the business logic and database of the application.
## API DOCUMENTATION

### AUTHENTICATION RELATED ENDPOINTS

#### api/v1/signup
- This recieves required fields to register a new user
- **Methods**: POST
- **AUTHENTICATION**: NOT REQUIRED
    * POST DETAILS:
        + REQUIRED FORM FIELDS:
            - firstName
            - lastName
            - password
            - email
            - mobile (optional)
    * JSON RESPONSE:
    ```
    {
        "email_verified":false,
        "fullName":"Emmanuel Adaja",
        "jwt":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcwODQ5MTc0OCwianRpIjoiMWRlOThkNzctZDI3Yy00MjRkLWEwYzgtNGQ3OTAyN2VkYjViIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjE2MzJmMWZiLTFhNDYtNGU5Yy1hZDI5LTcyNzczYzA2MzNkMyIsIm5iZiI6MTcwODQ5MTc0OCwiY3NyZiI6IjIyODlhMzNhLTE2MTMtNDY4Ni05ZmYyLWJiNDhjM2JkYmNhNiIsImV4cCI6MTcwODQ5MjY0OH0._zQECRA-SvMzRKlCKRDPF2FA1vZuOAK4Wo3sLXByn4I",
        "message":"Signup successful. Verification email sent",
        "mobile_verified":false,
        "organization":[]
    }
    ```

#### api/v1/login
- This endpoint handles user login returning user details and JWT authentication
- **Methods**: POST
- **AUTHENTICATION**: NOT REQUIRED
    * POST DETAILS:
        + REQUIRED FORM FIELDS:
            - email
            - password,
    * JSON RESPONSE:
    ```
    {
        "email_verified":true,
        "fullName":"Emmanuel Adaja",
        "jwt":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcwODQ5MTc0OCwianRpIjoiMWRlOThkNzctZDI3Yy00MjRkLWEwYzgtNGQ3OTAyN2VkYjViIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjE2MzJmMWZiLTFhNDYtNGU5Yy1hZDI5LTcyNzczYzA2MzNkMyIsIm5iZiI6MTcwODQ5MTc0OCwiY3NyZiI6IjIyODlhMzNhLTE2MTMtNDY4Ni05ZmYyLWJiNDhjM2JkYmNhNiIsImV4cCI6MTcwODQ5MjY0OH0._zQECRA-SvMzRKlCKRDPF2FA1vZuOAK4Wo3sLXByn4I",
        "message":"Login Succesful",
        "mobile_verified":false,
        "organization":[
            {
                "name": "My Company",
                "id": "f562dcf9-c267-4c4f-83d9-626f96d9e998".
                "user_role": "Admin"
            }
        ]
    }
    ```

#### api/v1/token
- This endpoint sends a 6 digit verification code to the user
- **Methods**: POST
- **AUTHENTICATION**: NOT REQUIRED
    * POST DETAILS:
        + REQUIRED FORM FIELDS:
            - email
    * JSON RESPONSE:
    ```
    {
        "message": "Verification code has been sent"
    }
    ```

#### api/v1/reset
- This resets a user password after authentication with the token sent to their respective email
- **Methods**: POST
- **AUTHENTICATION**: NOT REQUIRED
    * POST DETAILS:
        + REQUIRED FORM FIELDS:
            - email
            - password
            - code: the 6 digit verification code recieved by the user via email
    * JSON RESPONSE:
    ```
    {
        "message": "User password has been updated"
    }
    ```

#### api/v1/verify
- This verifies that user given email is valid via code sent to user email
- **Methods**: POST
- **AUTHENTICATION**: JWT
    * POST DETAILS:
        + REQUIRED FORM FIELDS:
            - code: the 6 digit verification code recieved by the user via email
    * JSON RESPONSE:
    ```
    {
        "message": "message": "Email Verified"
    }
    ```

#### api/v1/validate-token
- This verifies that the JWT is valid
- **Methods**: GET
- **AUTHENTICATION**: JWT
    * GET DETAILS:
        + NO REQUIRED FORM FIELDS:
    * JSON RESPONSE WITH 204 code:
    ```
    {
        "message": "JWT is valid"
    }
    ```


### USER RESOURCE API

#### api/v1/user
- This endpoint handles manipulation of the given user data
- **Methods**: GET, PUT, DELETE
- **AUTHENTICATION**: JWT
    * GET Details:
        + NO REQUIRED FIELD
        + JSON RESPONSE:
        ```
        {
            "first_name": "Emmanuel",
            "last_name": "Adaja",
            "email": "emmanueladaja@yahoo.com",
            "email_verified":true,
            "mobile": <phone number>,
            "mobile_verified":false,
            "organizations": [],
            "created_at": <datetime data>,
            "organizations_created": []
        }
        ```
    * PUT Details:
        + FORM FIELDS:
            - email (optional)
            - firstName (optional)
            - lastName (optional)
            - mobile (optional)
        + JSON RESPONSE
        ```
        {
            "message": "Email updated and verification code sent, Mobile number updated"
        }
        ```
    * DELETE Details
        + NO REQUIRED DATA
        + JSON RESPONSE
        ```
        {
            "message": "User account has been deleted"
        }
        ```


### ORGANIZATION RESOURCE API

#### api/v1/countries
- This sends all supported countries and their timezoones
- **Methods**: GET
- **AUTHENTICATION**: JWT
    * GET DETAILS:
        + NO REQUIRED FIELDS
        + JSON RESPONSE
        ```
        [
            {
                "country": "Nigeria",
                "timezones": ["Africa/Lagos"]
            },
            {
                "country": "Ghana",
                "timezones": ["Africa/Accra"]
            },
            ...
        ]
        ```

#### api/v1/organizations
- This allows creation of an organization and returns organizations user belong to
- **Methods**: GET, POST
- **AUTHENTICATION**: JWT
    * POST DETAILS:
        + REQUIRED FORM FIELDS:
            - name
            - country
            - timezone
            - description (optional)
            - mobile (optional)
            - address (optional)
            - image (optional)
        + JSON RESPONSE:
        ```
        {
            "message": "Organization succesfully created",
            "name": "My Comapny",
            "id": "f562dcf9-c267-4c4f-83d9-626f96d9e998",
            "created_at": <datetime data>,
            "image": <url link>,
            "country": "Nigeria"
        }
    * GET Details:
        + NO REQUIRED FIELDS
        + JSON RESPONSE
        ```
        {
            "message":"Returning user organizations",
            "organizations":[
                {
                    "id":"d19dba13-2845-4564-8224-bf7983a2e873",
                    "name":"My Company",
                    "user_role":"Admin"
                }, ...
            ]
        }
        ```

#### api/v1/organizations/<organization_id>
- This handle getting and updating an organization details and deleting the organization account
- **Methods**: GET, PUT, DELETE
- **AUTHENTICATION**: JWT
    * GET Details:
        + No Required Fields
        + Admins and Employee can access endpoint
        + JSON Response:
        ```
        {
            "address":null,
            "country":"Nigeria",
            "created_at":"2024-02-24 14:00:47",
            "creator":"Emmanuel Adaja",
            "description":"My interesting company",
            "id":"9dcdda27-deb3-49c1-9a15-d4eb84335666",
            "image":null,
            "mobile":null,
            "name":"My Company",
            "time_zone":"Africa/Lagos",
            "total_products":0,
            "user_role":"Admin"
        }
        ```
    
    * PUT Details:
        + FORM FIELDS:
            - mobile (optional)
            - image (optional)
            - address (optional)
            - description (optional)
        + Access Limited to only Admins
        + JSON RESPONSE
        ```
        {
            "message": "mobile updated, Organization address Updated"
        }
        ```
    * DELETE Details
        + NO REQUIRED DATA
        + Access Limited to only Admins
        + JSON RESPONSE
        ```
        {
            "message": "Organization account is deleted"
        }
        ```

#### api/v1/organizations/<organization_id>/categories
- Handles creating and loading the various product categories
- **Methods**: GET, POST
- **AUTHENTICATION**: JWT
    * GET Details:
        + NO REQUIRED DATA
        + Aceessible to all staff
        + JSON RESPONSE
        ```
        [
            {
                "created_at":"2024-02-29 17:34:49", 
                "description":null,"
                id":"629bb559-d9bb-4653-a527-e144de36f805",
                "name":"analgesics"
            },
            {
                "created_at":"2024-02-29 17:37:56",
                "description":null,
                "id":"8b7f5399-3f7e-438c-b1eb-7d8e29b2081b",
                "name":"Antibiotics"
            }
        ]
        ```
    * POST Details:
        + REQUIRED FORM DATA
            - name: the category name
            - description (optional): brief description of category
        + Accessible to all staff
        + JSON RESPONSE
        ```
        {
            "created_at":"2024-02-29 17:34:49",
            "description":null,
            "id":"629bb559-d9bb-4653-a527-e144de36f805",
            "name":"analgesics"
        }
        ```

#### api/v1/organizations/<organization_id>/products
- Handles loading all products(with pagination) and creating new product
- **Methods**: GET, POST
- **AUTHENTICATION**: JWT
    * GET Details:
        + REQUIRED FORM DATA
            - page (default = 1): page number to product view
        + Accessible to all staff
        + JSON RESPONSE
        ```
        {
            "data":[
                {
                    "category_id":null,
                    "cost_price":70.0,
                    "id":"491e1810-39b6-4501-920a-eea9117dcee9",
                    "image":null,
                    "last_updated":"2024-02-29 20:30:24",
                    "name":"paracetamol",
                    "quantity":2,
                    "sale_price":100.0,
                    "unit":"satchet",
                    "recent_purchases":[],
                    "recent_sales":[]
                }
            ],
            "next":null,
            "page":1
        }
        ```
    * POST details
        + REQUIRED FORM DATA
            - name: name of product
            - costPrice (optional): the cost price of a unit of the product
            - salePrice: sale price for a unit of the product
            - quantity: Number of units of the product being added
            - totalCost (default = 0): total cost of purchasing the product
            - unit (optional): name for a unit of the time i.e satchet
            - categoryId (optional): id of category the product belongs to
        + Accesible to all staff
        + JSON RESPONSE
        ```
        {
            "category_id":"629bb559-d9bb-4653-a527-e144de36f805",
            "cost_price":100.0,
            "id":"93bdb5fd-e4ca-4ce1-b089-70bc12b8cdbb",
            "image":null,
            "last_updated":"2024-02-29 22:01:05",
            "name":"diclofenac",
            "quantity":10,
            "sale_price":150.0,
            "unit":"pack",
            "recent_purchases":[],
            "recent_sales":[]
        }
        ```

#### api/v1/organizations/<organization_id>/products/<product_id>
- Handles loading all products(with pagination) and creating new product
- **Methods**: GET, PUT, DELETE
- **AUTHENTICATION**: JWT
    * GET Details:
        + NO REQUIRED DATA
        + Accessible to all staff
        + JSON RESPONSE
        ```
        {
            "category_id":"629bb559-d9bb-4653-a527-e144de36f805",
            "cost_price":100.0,
            "id":"93bdb5fd-e4ca-4ce1-b089-70bc12b8cdbb",
            "image":null,
            "last_updated":"2024-03-01 11:19:08",
            "name":"diclofenac",
            "quantity":9,
            "recent_purchases":[
                {
                    "Product_id":"93bdb5fd-e4ca-4ce1-b089-70bc12b8cdbb",
                    "product_name":"diclofenac",
                    "products_in_store":10,
                    "quantity":10,"total_cost":1100.0,
                    "transaction_done_by":"Emmanuel Adaja",
                    "transaction_id":"53c8b493-ed3c-4c95-9d73-ec2191e3d350",
                    "transaction_time":"2024-02-29 22:01:05",
                    "transaction_type":"Purchase"
                }
            ],
            "recent_sales":[
                {
                    "Product_id":"93bdb5fd-e4ca-4ce1-b089-70bc12b8cdbb",
                    "product_name":"diclofenac",
                    "products_in_store":10,
                    "quantity":10,
                    "total_cost":1100.0,
                    "transaction_done_by":"Emmanuel Adaja",
                    "transaction_id":"53c8b493-ed3c-4c95-9d73-ec2191e3d350",
                    "transaction_time":"2024-02-29 22:01:05",
                    "transaction_type":"Purchase"
                }
            ],
            "sale_price":150.0,
            "unit":"pack"
        }
        ```
    * PUT Details:
        + REQUIRED FORM DATA
            - UPDATE Quantity with new purchase
                - quantity: amount of new units purchased
                - purchaseCost (optional): total purchase cost for new units
                - description (optional): descriptionor detail associated with purchase
            - UPDATE name
                - name: change product name
            - UPDATE cost price
                - costPrice
            - UPDATE sale price
                - salePrice
            - UPDATE image
                - image
            - UPDATE unit name
                - unit: updates what a unit of a product is called
            - UPDATE product category
                - categoryId: the id of the category the product is to belong to
            - UPDATE low stock Alert level
                -lowStockLevel: new quantity aamount to warn that stock is low
        + Accessible to all staff
        + JSON RESPONSE
            - STRUCTURE
                {
                    "message": contains a message noting all updates that carried out,
                    "transaction": a object conatining details of any purchase added (empty otherwise)
                }
            - EXAMPLE
            ```
            {
                "message":"paracetamol purchase succesfully added, Product sale price succesfully updated, Product category succesfully updated",
                "transaction":{
                    "Product_id":"491e1810-39b6-4501-920a-eea9117dcee9",
                    "products_in_store":10,
                    "quantity":8,
                    "total_cost":800.0,
                    "transaction_done_by":"Emmanuel Adaja",
                    "transaction_id":"b5f58af5-bb9f-49cc-8083-060a75fcc63e",
                    "transaction_time":"2024-02-29 22:39:10",
                    "transaction_type":"Purchase"
                }
            }
            ```
    * DELETE Details
        + REQUIRED FORM DATA
            - REMOVE PRODUCT UNIT
                - quantity: amount of new units sold or removed
                - sale (default is autocalculated from sale price): total cost from saling units
                - description (optional): description or detail associated with removal
        + Accesible to all staff
        + JSON RESPONSE
        ```
        {
            "message":"4 unit of paracetamol removed",
            "transaction":{
                "Product_id":"491e1810-39b6-4501-920a-eea9117dcee9",
                "products_in_store":6,
                "quantity":4,
                "total_cost":480.0,
                "transaction_done_by":"Emmanuel Adaja",
                "transaction_id":"3589a8e1-4df3-4368-9528-92b432f0a929",
                "transaction_time":"2024-02-29 23:08:09",
                "transaction_type":"Sale"
            }
        }
        ```

#### api/v1/organizations/<organization_id>/products/search
- Search the product list based on a keyword
- **Methods**: GET
- **AUTHENTICATION**: JWT
    * GET Details:
        + REQUIRED FORM DATA
            - page (default = 1): page number to product view
            - keyword: search parameter
        + Acessible to all staff
        + JSON RESPONSE
        ```
        {
            "data":[
                {
                    "category_id":"629bb559-d9bb-4653-a527-e144de36f805",
                    "cost_price":70.0,
                    "id":"491e1810-39b6-4501-920a-eea9117dcee9",
                    "image":null,
                    "last_updated":"2024-02-29 23:08:09",
                    "name":"paracetamol",
                    "quantity":6,
                    "sale_price":120.0,
                    "unit":"satchet",
                    "recent_purchases":[],
                    "recent_sales":[]
                }
            ],
            "next":null,
            "page":1
        }
        ```

#### api/v1/organizations/<organization_id>/products/category
- Returns the products within a category
- **Methods**: GET
- **AUTHENTICATION**: JWT
    * GET Details:
        + REQUIRED FORM DATA
            - page (default = 1): page number to product view
            - categoryId: id of the category
        + Accessible to all staff
        + JSON RESPONSE
        ```
        {
            "data":[
                {
                    "category_id":"629bb559-d9bb-4653-a527-e144de36f805",
                    "cost_price":100.0,
                    "id":"93bdb5fd-e4ca-4ce1-b089-70bc12b8cdbb",
                    "image":null,
                    "last_updated":"2024-02-29 22:01:05",
                    "name":"diclofenac",
                    "quantity":10,
                    "sale_price":150.0,
                    "unit":"pack",
                    "recent_purchases":[
                        {
                            "Product_id":"93bdb5fd-e4ca-4ce1-b089-70bc12b8cdbb",
                            "product_name":"diclofenac",
                            "products_in_store":10,
                            "quantity":10,"total_cost":1100.0,
                            "transaction_done_by":"Emmanuel Adaja",
                            "transaction_id":"53c8b493-ed3c-4c95-9d73-ec2191e3d350",
                            "transaction_time":"2024-02-29 22:01:05",
                            "transaction_type":"Purchase"
                        }
                    ],
                    "recent_sales":[
                        {
                            "Product_id":"93bdb5fd-e4ca-4ce1-b089-70bc12b8cdbb",
                            "product_name":"diclofenac",
                            "products_in_store":10,
                            "quantity":10,
                            "total_cost":1100.0,
                            "transaction_done_by":"Emmanuel Adaja",
                            "transaction_id":"53c8b493-ed3c-4c95-9d73-ec2191e3d350",
                            "transaction_time":"2024-02-29 22:01:05",
                            "transaction_type":"Purchase"
                        }
                    ]
                },
                {
                    "category_id":"629bb559-d9bb-4653-a527-e144de36f805",
                    "cost_price":70.0,
                    "id":"491e1810-39b6-4501-920a-eea9117dcee9",
                    "image":null,
                    "last_updated":"2024-02-29 23:08:09",
                    "name":"paracetamol",
                    "quantity":6,
                    "sale_price":120.0,
                    "unit":"satchet",
                    "recent_sales":[],
                    "recent_purchases":[]
                }
            ],
            "next":null,
            "page":0
        }
        ```

#### api/v1/organizations/<organization_id>/sales
- Performs a bulk sale of items
- **Methods**: POST, GET
- **AUTHENTICATION**: JWT
    * POST DETAILS
        + REQUIRED JSON DATA
            - STRUCTURE
            {
                "items": [
                    {
                        "id": id of product that was sold,
                        "quantity": quantity of item sold
                    },
                    ....
                ]
            }
        + Accessible to all staff members
        + JSON RESPONSE
        ```
        [
            {
                "Product_id":"491e1810-39b6-4501-920a-eea9117dcee9",
                "products_in_store":3,
                "quantity":3,
                "status":"succesful transaction",
                "total_cost":360.0,
                "transaction_done_by":"Emmanuel Adaja",
                "transaction_id":"95747a74-e0f6-473c-a637-2edc5232c4fc",
                "transaction_time":"2024-03-01 11:19:08",
                "transaction_type":"Sale"
            },
            {
                "Product_id":"93bdb5fd-e4ca-4ce1-b089-70bc12b8cdbb",
                "products_in_store":9,
                "quantity":1,
                "status":"succesful transaction",
                "total_cost":150.0,
                "transaction_done_by":"Emmanuel Adaja",
                "transaction_id":"fd624f64-3d94-461e-8572-3af359958b98",
                "transaction_time":"2024-03-01 11:19:08",
                "transaction_type":"Sale"
            }
        ]
        ```
    * GET Details
        + REQUIRED FORM DATA
            - page (default = 1): page number to product view
        + Accessible to all staff
        + JSON RESPONSE
        ```
        {
            "data":[
                {
                    "Product_id":"491e1810-39b6-4501-920a-eea9117dcee9",
                    "product_name":"paracetamol",
                    "products_in_store":3,
                    "quantity":3,
                    "total_cost":360.0,
                    "transaction_done_by":"Emmanuel Adaja",
                    "transaction_id":"95747a74-e0f6-473c-a637-2edc5232c4fc",
                    "transaction_time":"2024-03-01 11:19:08",
                    "transaction_type":"Sale"
                },
                {
                    "Product_id":"93bdb5fd-e4ca-4ce1-b089-70bc12b8cdbb",
                    "product_name":"diclofenac",
                    "products_in_store":9,
                    "quantity":1,
                    "total_cost":150.0,
                    "transaction_done_by":"Emmanuel Adaja",
                    "transaction_id":"fd624f64-3d94-461e-8572-3af359958b98",
                    "transaction_time":"2024-03-01 11:19:08",
                    "transaction_type":"Sale"
                },
                {
                    "Product_id":"491e1810-39b6-4501-920a-eea9117dcee9",
                    "product_name":"paracetamol",
                    "products_in_store":6,
                    "quantity":4,
                    "total_cost":480.0,
                    "transaction_done_by":"Emmanuel Adaja",
                    "transaction_id":"3589a8e1-4df3-4368-9528-92b432f0a929",
                    "transaction_time":"2024-02-29 23:08:09",
                    "transaction_type":"Sale"
                }
            ],
            "next":null,
            "page":1
        }
        ```

#### api/v1/organizations/<organization_id>/purchases
- Retrives purchases mae by the organization
- **Methods**: GET
- **AUTHENTICATION**: JWT
    * GET DETAILS
        + REQUIRED FORM DATA
            - page (default = 1): page number to product view
        + Accessible to all staff
        + JSON RESPONSE
        ```
        {
            "data":[
                {
                    "Product_id":"491e1810-39b6-4501-920a-eea9117dcee9",
                    "product_name":"paracetamol",
                    "products_in_store":10,
                    "quantity":8,
                    "total_cost":800.0,
                    "transaction_done_by":"Emmanuel Adaja",
                    "transaction_id":"b5f58af5-bb9f-49cc-8083-060a75fcc63e",
                    "transaction_time":"2024-02-29 22:39:10",
                    "transaction_type":"Purchase"
                },
                {
                    "Product_id":"93bdb5fd-e4ca-4ce1-b089-70bc12b8cdbb",
                    "product_name":"diclofenac",
                    "products_in_store":10,
                    "quantity":10,
                    "total_cost":1100.0,
                    "transaction_done_by":"Emmanuel Adaja",
                    "transaction_id":"53c8b493-ed3c-4c95-9d73-ec2191e3d350",
                    "transaction_time":"2024-02-29 22:01:05",
                    "transaction_type":"Purchase"
                },
                {
                    "Product_id":"491e1810-39b6-4501-920a-eea9117dcee9",
                    "product_name":"paracetamol",
                    "products_in_store":2,
                    "quantity":2,
                    "total_cost":0.0,
                    "transaction_done_by":"Emmanuel Adaja",
                    "transaction_id":"196df353-6859-468a-9e14-b09d2e9be506",
                    "transaction_time":"2024-02-29 20:30:24",
                    "transaction_type":"Purchase"
                }
            ],
            "next":null,
            "page":1
        }
        ```
