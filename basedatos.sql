drop table if exists producto;
drop table if exists cerveza;
drop table if exists bodega;
drop table if exists producto_reserva;
drop table if exists reserva;
drop table if exists cliente;
drop table if exists empresa_cliente;

create table producto (
  id integer primary key autoincrement,
  nombre text not null,
  descripcion text not null,
  precio_neto integer,
  stock integer,
  img_url text,
  id_cerveza integer,
  foreign key(id_cerveza) REFERENCES cerveza(id)
);

create table cerveza (
  id integer primary key autoincrement,
  nombre text not null,
  descripcion text not null,
  grados integer,
  img_url text
);

create table bodega (
  id integer primary key autoincrement,
  stock integer not null,
  id_producto integer,
  foreign key(id_producto) REFERENCES producto(id)
);

create table producto_reserva (
  id_reserva integer,
  id_producto integer,
  cantidad integer not null,
  foreign key(id_reserva) REFERENCES reserva(id),
  foreign key(id_producto) REFERENCES producto(id)
);

create table reserva (
  id integer primary key autoincrement,
  fecha date,
  tipo_documento text,
  id_cliente integer,
  foreign key(id_cliente) REFERENCES cliente(id)
);

create table cliente (
  id integer primary key autoincrement,
  correo text,
  clave text
);

create table empresa_cliente (
  id integer primary key autoincrement,
  nombre text,
  direccion text,
  ciudad text,
  fono integer,
  email text,
  id_cliente integer,
  foreign key(id_cliente) REFERENCES cliente(id)
);

insert into cerveza (nombre, descripcion, grados,img_url) 
	values ('Cerveza Lager','Graduación en torno a 5%. De color son rubias doradas con reflejos ámbar. Sus aromas están marcados por la malta con notas ligeramente tostadas y de lúpulo. Su cremosidad queda marcada en las paredes del vaso........................',8,'imagenes/cerveza01.jpg');


insert into cerveza (nombre, descripcion, grados,img_url) 
	values ('Cerveza Stout','La cerveza Porter es una cerveza menos amarga, densidades originales más bajas y menor grado de alcohol que las Stout. La cerveza Stout, recibe este nombre por ser la porter más fuerte. La stout es una cerveza de color..............',8,'imagenes/cerveza02.jpg');

insert into cerveza (nombre, descripcion, grados,img_url) 
	values ('Cerveza de Trigo','Su característica principal es su cáracter ácido, refrescante y espumoso, por lo que no es de extrañar que sea una cerveza muy popular en las areas donde tradicionalmente se produce, como son el sur de Alemania, Berlín y Bélgica.',8,'imagenes/cerveza03.jpg');


insert into producto (nombre, descripcion, precio_neto,img_url,id_cerveza) 
	values ('Barril 30L', 'Barril de 30 Litros Cerveza Lager',22000,'imagenes/barril.jpg',1);
insert into producto (nombre, descripcion, precio_neto,img_url,id_cerveza) 
	values ('Botella 350cc', 'Botella 350cc Cerveza Lager',3000,'imagenes/botella350.jpg',1);
insert into producto (nombre, descripcion, precio_neto,img_url,id_cerveza) 
	values ('Botella 500cc', 'Botella 500cc Cerveza Lager',4500,'imagenes/botella500.jpg',1);

insert into producto (nombre, descripcion, precio_neto,img_url,id_cerveza) 
  values ('Barril 45L', 'Barril de 45 Litros Cerveza Stout',34000,'imagenes/barril.jpg',2);
insert into producto (nombre, descripcion, precio_neto,img_url,id_cerveza) 
  values ('Botella 350cc', 'Botella 350cc Cerveza Stout',3000,'imagenes/botella350.jpg',2);
insert into producto (nombre, descripcion, precio_neto,img_url,id_cerveza) 
  values ('Botella 500cc', 'Botella 500cc Cerveza Lager',3500,'imagenes/botella500.jpg',2);

insert into producto (nombre, descripcion, precio_neto,img_url,id_cerveza) 
  values ('Barril 50L', 'Barril de 45 Litros Cerveza Trigo',45000,'imagenes/barril.jpg',3);
insert into producto (nombre, descripcion, precio_neto,img_url,id_cerveza) 
  values ('Botella 350cc', 'Botella 350cc Cerveza Trigo',2500,'imagenes/botella350.jpg',3);

insert into bodega (stock, id_producto) values (20,1);
insert into bodega (stock, id_producto) values (22,2);
insert into bodega (stock, id_producto) values (23,3);
insert into bodega (stock, id_producto) values (24,4);
insert into bodega (stock, id_producto) values (25,5);
insert into bodega (stock, id_producto) values (26,6);
insert into bodega (stock, id_producto) values (27,7);
insert into bodega (stock, id_producto) values (28,8);


insert into cliente (correo, clave) values ("nico@araneda.cl","1234");
insert into cliente (correo, clave) values ("alonso@parra.cl","1234");
insert into cliente (correo, clave) values ("rodolfo@diaz.cl","1234");
insert into cliente (correo, clave) values ("miguel@silva.cl","1234");

insert into empresa_cliente (id_cliente) values (1);
insert into empresa_cliente (id_cliente) values (2);
insert into empresa_cliente (id_cliente) values (3);
insert into empresa_cliente (id_cliente) values (4);