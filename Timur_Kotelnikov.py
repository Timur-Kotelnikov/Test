import psycopg2
from config import host, user, password, db_name, port


def create_tables():
    return f"CREATE TABLE IF NOT EXISTS Users (user_id SERIAL PRIMARY KEY, user_age INTEGER NOT NULL);" \
           f"CREATE TABLE IF NOT EXISTS Items (item_id SERIAL PRIMARY KEY,item_price MONEY NOT NULL);" \
           f"CREATE TABLE IF NOT EXISTS Purchases (purchase_id SERIAL PRIMARY KEY, " \
           f"user_id INTEGER REFERENCES Users(user_id), item_id INTEGER REFERENCES Items(item_id), " \
           f"purchase_date DATE NOT NULL);"


def insert_data():
    return f"INSERT INTO Users (user_age) VALUES ('18'), ('25'), ('26'), ('35'), ('36'), ('39');" \
           f"INSERT INTO Items (item_price) VALUES ('10'), ('20'), ('30'), ('40'), ('50'), ('60');" \
           f"INSERT INTO Purchases (user_id, item_id, purchase_date) VALUES ('1', '1', '2021-01-08'), " \
           f"('1', '2', '2021-02-08'), ('1', '3', '2021-03-08'), ('1', '4', '2021-04-08'), ('1', '5', '2021-05-08'), " \
           f"('1', '6', '2021-06-08'), ('1', '1', '2021-07-08'), ('1', '2', '2021-08-08'), ('1', '3', '2021-09-08'), " \
           f"('1', '4', '2021-10-08'), ('1', '5', '2021-11-08'), ('1', '6', '2021-12-08'), ('1', '5', '2021-12-09');" \
           f"INSERT INTO Purchases (user_id, item_id, purchase_date) VALUES ('2', '2', '2021-01-08'), " \
           f"('2', '3', '2021-02-08'), ('2', '4', '2021-03-08'), ('2', '5', '2021-04-08'), ('2', '6', '2021-05-08'), " \
           f"('2', '1', '2021-06-08'), ('2', '2', '2021-07-08'), ('2', '3', '2021-08-08'), ('2', '4', '2021-09-08'), " \
           f"('2', '5', '2021-10-08'), ('2', '6', '2021-11-08'), ('2', '1', '2021-12-08'), ('2', '5', '2021-12-09');" \
           f"INSERT INTO Purchases (user_id, item_id, purchase_date) VALUES ('3', '3', '2021-01-08'), " \
           f"('3', '4', '2021-02-08'), ('3', '5', '2021-03-08'), ('3', '6', '2021-04-08'), ('3', '1', '2021-05-08'), " \
           f"('3', '2', '2021-06-08'), ('3', '3', '2021-07-08'), ('3', '4', '2021-08-08'), ('3', '5', '2021-09-08'), " \
           f"('3', '6', '2021-10-08'), ('3', '1', '2021-11-08'), ('3', '2', '2021-12-08'), ('3', '4', '2021-12-09');" \
           f"INSERT INTO Purchases (user_id, item_id, purchase_date) VALUES ('4', '4', '2021-01-08'), " \
           f"('4', '5', '2021-02-08'), ('4', '6', '2021-03-08'), ('4', '1', '2021-04-08'), ('4', '2', '2021-05-08'), " \
           f"('4', '3', '2021-06-08'), ('4', '4', '2021-07-08'), ('4', '5', '2021-08-08'), ('4', '6', '2021-09-08'), " \
           f"('4', '1', '2021-10-08'), ('4', '2', '2021-11-08'), ('4', '3', '2021-12-08'), ('4', '4', '2021-12-09');" \
           f"INSERT INTO Purchases (user_id, item_id, purchase_date) VALUES ('5', '5', '2021-01-08'), " \
           f"('5', '6', '2021-02-08'), ('5', '1', '2021-03-08'), ('5', '2', '2021-04-08'), ('5', '3', '2021-05-08'), " \
           f"('5', '4', '2021-06-08'), ('5', '5', '2021-07-08'), ('5', '6', '2021-08-08'), ('5', '1', '2021-09-08'), " \
           f"('5', '2', '2021-10-08'), ('5', '3', '2021-11-08'), ('5', '4', '2021-12-08'), ('5', '6', '2021-12-09'), " \
           f"('5', '6', '2021-12-10');" \
           f"INSERT INTO Purchases (user_id, item_id, purchase_date) VALUES ('6', '6', '2021-01-08'), " \
           f"('6', '1', '2021-02-08'), ('6', '2', '2021-03-08'), ('6', '3', '2021-04-08'), ('6', '4', '2021-05-08'), " \
           f"('6', '5', '2021-06-08'), ('6', '6', '2021-07-08'), ('6', '1', '2021-08-08'), ('6', '2', '2021-09-08'), " \
           f"('6', '3', '2021-10-08'), ('6', '4', '2021-11-08'), ('6', '5', '2021-12-08');"


def get_result_1():
    return f'SELECT SUM(item_price*(SELECT COUNT(*) FROM Purchases WHERE Purchases.item_id = Items.item_id AND ' \
           f'user_id IN (SELECT user_id FROM Users WHERE user_age >= 18 AND user_age <= 25)))/(SELECT ' \
           f'((MAX(purchase_date)-MIN(purchase_date))/30) FROM Purchases WHERE user_id IN (SELECT user_id FROM ' \
           f'Users WHERE user_age >= 18 AND user_age <= 25)) as "18-25 per month avg" FROM Items;'


def get_result_2():
    return f'SELECT SUM(item_price*(SELECT COUNT(*) FROM Purchases WHERE Purchases.item_id = Items.item_id AND ' \
           f'user_id IN (SELECT user_id FROM Users WHERE user_age >= 26 AND user_age <= 35)))/(SELECT ' \
           f'((MAX(purchase_date)-MIN(purchase_date))/30) FROM Purchases WHERE user_id IN (SELECT user_id FROM ' \
           f'Users WHERE user_age >= 26 AND user_age <= 35)) as "26-35 per month avg" FROM Items;'


def get_result_3():
    return f"SELECT date_part('month', Purchases.purchase_date) FROM Items JOIN Purchases ON " \
           f"Purchases.item_id = Items.item_id WHERE user_id IN (SELECT user_id FROM Users WHERE user_age > 35) " \
           f"GROUP BY date_part('month', Purchases.purchase_date) ORDER BY SUM(Items.item_price) DESC LIMIT 1;"


def get_result_4():
    return f"SELECT item_id FROM Items GROUP BY item_id ORDER BY (SELECT SUM(item_price*(SELECT COUNT(*) FROM " \
           f"Purchases WHERE Purchases.item_id = Items.item_id AND purchase_date BETWEEN '2021-01-01' AND " \
           f"'2021-12-31'))) DESC LIMIT 1;"


def get_result_5():
    return f"SELECT item_id FROM Items GROUP BY item_id ORDER BY (SELECT SUM(item_price*(SELECT COUNT(*) FROM " \
           f"Purchases WHERE Purchases.item_id = Items.item_id))) DESC LIMIT 3;"


def call_functions(function):
    try:
        connection = psycopg2.connect(host=host, user=user, password=password, database=db_name, port=port)
        with connection.cursor() as cursor:
            cursor.execute(function)
            connection.commit()
            try:
                a = cursor.fetchall()
                return f'Result of query is {a[0][0] if len(a) == 1 else [i[0] for i in a]}'
            except Exception:
                pass
    except Exception as _ex:
        print('Error!', _ex)


call_functions(create_tables())
call_functions(insert_data())
print(call_functions(get_result_1()))
print(call_functions(get_result_2()))
print(call_functions(get_result_3()))
print(call_functions(get_result_4()))
print(call_functions(get_result_5()))