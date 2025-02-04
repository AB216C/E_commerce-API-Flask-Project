**E_Commerce API with Flask, SQLAlchemy, Marshmallow, and MYSQL**

*Overview*

This project main goal is to build API using different software packages such as Flask, SQLAlchemy, Marshmallow, and MYSQL. 

The proejct starts by setting up Virtual Environment. Virtual environment make this project unique and not get mixed up with other projects on the desktop. After activating virtual environmentt, app.py file is created and flask, sqlalchemy, marshmallow and mysql packages are installed. After, flask appp is created, get connected to the database, and get initialized.

The project is about online shopping. Because of that, user, product, and order tables are created. Since user can place multiple orders, one to many relationship is created by inserting foreign key in order table. Since one order can have multiple products and one product can be on multiple and different orders, many to many relationship is established using order_product association table.

After, Marshmallow schemas are created for each table/model to help in serialization, deserialization, and validation of data.

Lastly, creating API end points. In this section, API endpoints are ready to be tested using CRUD(create, read, update and delete)operations. These operations are used to manage API. Postmen application is used to test these endpoints by sending HTTP requests to the server using four ways(POST, GET, PUT AND DELETE). Testing API endpoints using postman allows you  to confirm that your API has been created and fully functioning.