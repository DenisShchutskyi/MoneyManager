import psycopg2
from config import str_connect_to_db
import traceback


def create_connection():
    """
    метод создания подключения к БД
    :return: или подключение или None
    """
    conn = None
    try:
        conn = psycopg2.connect(str_connect_to_db)
    except:
        print("I am unable to connect to the database")
    return conn


def decorator_db(fn):
    def wrap(*args, **kwargs):
        conn = create_connection()
        try:
            if conn:
                kwargs['conn'] = conn
                data = fn(*args,
                          **kwargs)
                conn.close()
                return data
            return None
        except:
            traceback.print_exc()
            conn.close()
            return None
    return wrap


@decorator_db
def registration(id_user,
                 first_name,
                 last_name,
                 *args,
                 **kwargs):
    conn = kwargs['conn']
    cur = conn.cursor()
    select_find = '''
        SELECT id_user_in_telegram
        FROM users
        WHERE id_user_in_telegram = {}
    '''.format(id_user)
    cur.execute(select_find)
    row = cur.fetchone()
    if row:
        return True
    select_insert = '''
        INSERT INTO users (id_user_in_telegram, first_name, last_name)
        VALUES ({},'{}','{}');
    '''.format(id_user, first_name,last_name)
    cur.execute(select_insert)
    conn.commit()
    return True


@decorator_db
def set_valuta(id_user,
               valuta,
               *args,
               **kwargs):
    conn = kwargs['conn']
    cur = conn.cursor()
    select = '''
        UPDATE users
        SET valuta = '{}'
        WHERE id_user_in_telegram = {}
    '''.format(valuta, id_user )
    cur.execute(select)
    conn.commit()
    return True


@decorator_db
def add_pay(id_user,
            value,
            id_category,
            *args,
            **kwargs):
    conn = kwargs['conn']
    cur = conn.cursor()
    insert_pay = '''
        INSERT INTO expenses (id_expenses, ref_id_category_expenses, ref_id_users, "date", pay) 
        VALUES (DEFAULT, {}, {}, DEFAULT, {}) returning id_expenses
    '''.format(id_category, id_user, value)
    cur.execute(insert_pay)
    id_ex = cur.fetchone()
    conn.commit()
    return id_ex[0]


@decorator_db
def set_comment_to_expenses(id_expenses,
                            comment,
                            *args,
                            **kwargs):
    conn = kwargs['conn']
    cur = conn.cursor()
    set_com = '''
        UPDATE expenses 
        SET comment = '{}'
        WHERE id_expenses = {}
    '''.format(comment,
               id_expenses)
    cur.execute(set_com)
    conn.commit()
    return 0


def get_category(cur):
    select = '''
        SELECT id_category_expenses, title_expenses
        FROM category_expenses
    '''
    cur.execute(select)
    return {
        r[1]: r[0]
        for r in cur.fetchall()
    }


@decorator_db
def get_pays_month_fpr_pie_diagramm(id_user,
                                    *args,
                                    **kwargs):
    conn = kwargs['conn']
    cur = conn.cursor()
    select = '''
        SELECT sum(e.pay)
        FROM expenses e
        WHERE e.ref_id_category_expenses = {}
        AND e.ref_id_users = {}
        AND EXTRACT(MONTH FROM e.date) = EXTRACT(MONTH FROM  now())
        AND EXTRACT(YEAR FROM  e.date) = EXTRACT(YEAR FROM  now())
    '''

    categories = get_category(cur)
    for i in list(categories.keys()):
        cur.execute(select.format(categories[i],
                                        id_user))
        sum = cur.fetchone()[0]
        if sum:
            categories[i] = float(sum)
        else:
            categories[i] = 0
    return categories


@decorator_db
def get_pays_month_user_in_category(id_user,
                                    id_category,
                                    *args,
                                    **kwargs):
    conn = kwargs['conn']
    cur = conn.cursor()
    select = '''
        SELECT e.pay, e."date", e.comment, e.id_expenses
        FROM expenses e
        WHERE e.ref_id_category_expenses = {}
        AND e.ref_id_users = {}
        AND EXTRACT(MONTH FROM e.date) = EXTRACT(MONTH FROM  now())
        AND EXTRACT(YEAR FROM  e.date) = EXTRACT(YEAR FROM  now())
        ORDER BY e."date" ASC, e.pay DESC 
    '''.format(id_category, id_user)
    cur.execute(select)
    data = [
        {
            'id_expenses': r[3],
            'pay': r[0],
            'date': '{}-{}-{}'.format(r[1].day,r[1].month,r[1].year),
            'comment':r[2]
        }
    for r in cur.fetchall()]
    return data


@decorator_db
def get_by_categories_pay_month(id_user,
                                *args,
                                **kwargs):
    conn = kwargs['conn']
    cur = conn.cursor()
    select = '''
        SELECT id_category_expenses, title_expenses
        FROM category_expenses
    '''
    cur.execute(select)
    data = {
        r[1]: get_pays_month_user_in_category(id_user, r[0])
        for r in cur.fetchall()
    }
    return data



@decorator_db
def get_statistic(id_user,
                  id_category,
                  period='day',
                  *args,
                  **kwargs):
    conn = kwargs['conn']
    cur = conn.cursor()

    select = '''
    SELECT e.id_expenses, e.comment, e.pay,e."date" 
    FROM expenses e
    WHERE date_trunc('{}', e.date) = date_trunc('{}', now())
    AND e.ref_id_users = {}
    AND e.ref_id_category_expenses = {}
    ORDER BY e
    '''.format(period, period, id_user, id_category)
    cur.execute(select)
    rows= cur.fetchall()
    sum = 0
    data = []
    for r in rows:
        data.append({
            'id_expenses': r[0],
            'pay': r[2],
            'comment': r[1],
            'date': '{}-{}-{}'.format(r[3].day,r[3].month,r[3].year)
        })
        sum += r[2]
    return data, sum
