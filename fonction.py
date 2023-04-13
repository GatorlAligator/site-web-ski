def get_stations_by_price(self, price_type, sort_order):
    with self.conn.cursor() as cursor:
        if price_type == "day":
            price_field = "price_day"
        elif price_type == "week":
            price_field = "price_week"
        else:
            return None
        
        if sort_order == "asc":
            order_by = "ORDER BY {} ASC".format(price_field)
        elif sort_order == "desc":
            order_by = "ORDER BY {} DESC".format(price_field)
        else:
            return None
        
        sql = "SELECT * FROM stations {} {}".format(order_by)
        cursor.execute(sql)
        result = cursor.fetchall()
        stations = []
        for row in result:
            station = {
                "id": row[0],
                "name": row[1],
                "location": row[2],
                "price_day": row[3],
                "price_week": row[4],
                "comment": row[5],
                "pistes": self.get_pistes_by_station(row[0])
            }
            stations.append(station)
        return stations
