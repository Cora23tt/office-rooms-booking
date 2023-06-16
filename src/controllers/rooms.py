import json
from datetime import datetime
from flask import Blueprint
from flask import request
from flask import Response
from ..repositories import rooms_repo

rooms=Blueprint("rooms", __name__, url_prefix="/api/rooms")

@rooms.get('/')
def get_room():
    id=request.args.get('id')

    if id:
        if not id.isdigit() or int(id) < 0:
            return Response(
                response=json.dumps({"error":"Invalid id number"}),
                status=400,
                content_type='application/json')

        id=int(id)
        result=rooms_repo.fetch_room(id)
        if result:

            return Response(
                response=json.dumps(result),
                content_type='application/json')
        
        return Response(
            response=json.dumps({"error": "topilmadi"}), 
            status=404, 
            content_type='application/json')


    search=request.args.get('search')
    if search:
        if isinstance(search, str):

            return Response(
                response=json.dumps(rooms_repo.fetch_rooms_by_search(search)),
                content_type='application/json')
        
        return Response(
            response=json.dumps({"error":"Invalid search keyword"}),
            status=400,
            content_type='application/json')
    

    page=request.args.get('page')
    if page:
        if not page.isdigit() or int(page) < 0:
            return Response(
                response=json.dumps({"error":"Invalid page number"}),
                status=400,
                content_type='application/json')
        
        return Response(
            response=json.dumps(rooms_repo.fetch_rooms_by_page(int(page))),
            content_type='application/json')
    
    return Response(
        response=json.dumps(rooms_repo.fetch_rooms_by_page(1)),
        content_type='application/json')


@rooms.route('/<id>/availability')
def get_aviability(id=None):    
    if id == None:
        return Response(
            response=json.dumps({"error":"Invalid id number"}),
            status=400,
            content_type='application/json')
    
    if not id.isdigit() or int(id) < 0:
        return Response(
            response=json.dumps({"error":"Invalid id number"}),
            status=400,
            content_type='application/json')

    date=request.args.get('date')
    if date:
        try:
            date=datetime.strptime(date, '%Y-%m-%d')
        except:
            return Response(
                response=json.dumps({"error":"Invalid date format"}),
                status=400,
                content_type='application/json')
    else:
        date=datetime.today()

    return Response(
        response=json.dumps(rooms_repo.fetch_room_availability(int(id), date)),
        content_type='application/json')


@rooms.route('/<id>/book')
def book_room(id=None):
    
    if id is None:
        return Response(status=404)

    if not id.isdigit() or int(id) < 0:
        return Response(status=404)

    request_data=request.get_json()
    if not request_data or "resident" not in request_data or "start" not in request_data or "end" not in request_data:
        return Response(status=400)

    resident_name=request_data['resident'].get('name')
    start_str=request_data['start']
    end_str=request_data['end']

    resident_id = rooms_repo.resident(resident_name)
    if resident_id == None:
        return Response(status=404)

    try:
        start=datetime.strptime(start_str, '%Y-%m-%d %H:%M:%S')
        end=datetime.strptime(end_str, '%Y-%m-%d %H:%M:%S')
    except ValueError:
        return Response(status=400)

    if start.date() != end.date() or start >= end:
        return Response(status=400)
        
    return Response(
        response=json.dumps(rooms_repo.book_room(id, resident_id, start, end)),
        content_type='application/json')
