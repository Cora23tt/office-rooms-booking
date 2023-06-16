# office-rooms-booking
## REST-API for booking coworking center rooms.
### goal: 
```
to demonstrate the skills of developing a simple web application and skills in web technologies.
```
### conclusion:
```
Wrote a .sql file that contains queries for building tables and entering dummy data in PostgreSQL database.
The psysopg2 driver is used to work with the database.
For routing endpoints I used a flask.
```

## API to get available rooms

```
GET /api/rooms
```

Parametrlar:

- `search`: Search by room name
- `type`: sort by room type (`focus`, `team`, `conference`)
- `page`: page sequence number
- `page_size`: maximum number of results per page

HTTP 200

```json
{
  "page": 1,
  "count": 3,
  "page_size": 10,
  "results": [
    {
      "id": 1,
      "name": "mytaxi",
      "type": "focus",
      "capacity": 1
    },
    {
      "id": 2,
      "name": "workly",
      "type": "team",
      "capacity": 5
    },
    {
      "id": 3,
      "name": "express24",
      "type": "conference",
      "capacity": 15
    }
  ]
}
```

---

## API to get room by id

```
GET /api/rooms/{id}
```

HTTP 200

```json
{
  "id": 3,
  "name": "express24",
  "type": "conference",
  "capacity": 15
}
```

HTTP 404

```json
{
  "error": "topilmadi"
}
```

---

## API to get room availability

```
GET /api/rooms/{id}/availability
```

Parameters:

- `date`: date (if not specified, today's date is taken)

Response 200

```json
[
  {
    "start": "05-06-2023 9:00:00",
    "end": "05-06-2023 11:00:00"
  },
  {
    "start": "05-06-2023 13:00:00",
    "end": "05-06-2023 18:00:00"
  }
]
```

---

## API for booking a room

```
POST /api/rooms/{id}/book
```

```json
{
  "resident": {
    "name": "Anvar Sanayev"
  },
  "start": "05-06-2023 9:00:00",
  "end": "05-06-2023 10:00:00"
}
```

---

HTTP 201: When the room is successfully booked

```json
{
  "message": "xona muvaffaqiyatli band qilindi"
}
```

HTTP 410: When the room is occupied at the selected time

```json
{
  "error": "uzr, siz tanlagan vaqtda xona band"
}
```