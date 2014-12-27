drop table if exists entries;

create table producto (
  id integer primary key autoincrement,
  nombre text not null,
  descripcion text not null,
  precio_neto integer,
  img_url text
);
insert into entry (nombre, descripcion, precio_neto) values ('Producto01', 'Cerveza Lager',20,'/imagenes/imagen01.jpg');
insert into entry (nombre, descripcion, precio_neto) values ('Producto02', 'Cerveza Lager2',30,'/imagenes/imagen02.jpg');
insert into entry (nombre, descripcion, precio_neto) values ('Producto03', 'Cerveza Lager3',40,'/imagenes/imagen03.jpg');