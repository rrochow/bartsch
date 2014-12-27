#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sqlite3

with sqlite3.connect("basedatos.db") as connection:
	c = connection.cursor()
	c.execute("DROP TABLE IF EXISTS producto")
	c.execute("create table producto (  id integer primary key autoincrement, nombre text not null, descripcion text not null, precio_neto integer, img_url text);")
	
	c.execute("insert into producto (nombre, descripcion, precio_neto,img_url) values ('Producto01', 'Cerveza Lager',2000,'imagenes/imagen01.jpg');")	
	c.execute("insert into producto (nombre, descripcion, precio_neto,img_url) values ('Producto02', 'Cerveza Lager2','3000','imagenes/imagen02.jpg');")
	c.execute("insert into producto (nombre, descripcion, precio_neto,img_url) values ('Producto03', 'Cerveza Lager3','3000','imagenes/imagen03.jpg');")

