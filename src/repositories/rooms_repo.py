from ..db.run_sql import run_sql
from datetime import datetime, timedelta

def fetch_room(id: int):
    
    query = 'SELECT rooms.id, rooms.name, room_types.name AS type_name, rooms.capacity \
        FROM rooms \
        JOIN room_types ON rooms.type_id = room_types.id \
        WHERE rooms.id = %s'
    
    result = run_sql(query, id)

    if len(result)<=0:
        return None
    
    r = result[0]
    return {
        "id": r['id'],
        "name": r['name'],
        "type": r['type_name'],
        "capacity": r['capacity']
    }


def fetch_rooms_by_page(page: int):

    query = 'WITH rooms_ordered AS ( SELECT * FROM rooms \
    ORDER BY capacity OFFSET {} LIMIT 10 ) SELECT *, \
    (SELECT COUNT(*) FROM rooms) AS total_count FROM rooms_ordered'.format(str((int(page)-1)*10))

    sql_result = run_sql(query)

    if len(sql_result)>0:
        results = []
        for row in sql_result:
            results.append({'id': row['id'], 'name': row['name'], 'type': row['type_id'], 'capacity': row['capacity']})
        return {'page': page, 'count': sql_result[0][4], 'page_size': 10, 'results': results}
    
    query = 'SELECT COUNT(*) FROM rooms'
    sql_result = run_sql(query)
    return {'page': page, 'count': sql_result[0][0], 'page_size': 10, 'results': []}


def fetch_rooms_by_search(search: str):

    query = "WITH rooms_ordered AS (SELECT * FROM rooms WHERE name LIKE '%{}%' \
    ORDER BY capacity LIMIT 10 ) SELECT *, \
    (SELECT COUNT(*) FROM rooms WHERE name LIKE '%{}%') AS total_count FROM rooms_ordered".format(search, search)

    sql_result = run_sql(query)

    if len(sql_result)>0:
        results = []
        for row in sql_result:
            results.append({'id': row['id'], 'name': row['name'], 'type': row['type_id'], 'capacity': row['capacity']})
        return {'page': 1, 'count': sql_result[0]['total_count'], 'page_size': 10, 'results': results}

    return {'page': 1, 'count': 0, 'page_size': 10, 'results': None}


def fetch_room_availability(id: int, date: datetime):

    query = "SELECT * FROM bookings WHERE room_id={} AND start_::date = date '{}' ORDER BY start_".format(id, date)

    sql_result = run_sql(query)
    
    result = []
    not_available_periods = []

    for row in sql_result:
        not_available_periods.append({
            'start_time': str(row['start_']), 
            'end_time': str(row['end_'])
            })
        
    # calculating free periods # inversing busy periods of room
    previus_period_end = date
    day_end = date + timedelta(seconds=86399)

    for busy_period in not_available_periods:
        
        busy_period_start = datetime.strptime(busy_period['start_time'], '%Y-%m-%d %H:%M:%S')
        busy_period_end = datetime.strptime(busy_period['end_time'], '%Y-%m-%d %H:%M:%S')
        
        free_period_start = previus_period_end + timedelta(seconds=1)
        free_period_end = busy_period_start - timedelta(seconds=1)

        if busy_period_start == free_period_start:
            previus_period_end = busy_period_end
            continue

        result.append({"start": str(free_period_start), "end": str(free_period_end)})
        previus_period_end = busy_period_end

    if previus_period_end != day_end and \
        previus_period_end + timedelta(seconds=1) != day_end:
        free_period_start = previus_period_end + timedelta(seconds=1)
        free_period_end = day_end
        result.append({"start": str(free_period_start), "end": str(free_period_end)})

    return result

def book_room(id: int, resident_id: str, start: datetime, end: datetime):

    query = "SELECT * FROM bookings WHERE room_id={} AND start_::date = date '{}' ORDER BY start_".format(id, start.date())
    sql_result = run_sql(query)

    for row in sql_result:
        if start == row['start_'] or start == row['end_'] or end == row['start_'] or end == row['end_'] or\
            row['start_'] < start and start < row['end_'] or \
            row['start_'] < end and end < row['end_']:
            return {"error": "uzr, siz tanlagan vaqtda xona band"}

    query = "insert into bookings (room_id, resident_id, start_, end_) values({}, {}, '{}', '{}')".format(id, resident_id, start, end)
    sql_result = run_sql(query)
    print(sql_result)
    return {'message': 'xona muvaffaqiyatli band qilindi'}

def resident(name: str):
    resident_id = None
    query = "SELECT id FROM RESIDENTS WHERE name = '{}'".format(name)
    sql_result = run_sql(query)
    for row in sql_result:
        resident_id = row['id']

    return resident_id

