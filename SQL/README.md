
# SQL
```shell
> psql -h localhost -U postgresql -d postgresql
> create database shop;
> \c shop
create table customer(
   id serial primary key,
   name varchar(255),
   phone varchar(30),
   email varchar(255)
);
> \d customer
create table product(
   id serial primary key,
   name varchar(255),
   description text,
   price integer
);
create table product_photo(
   id serial primary key,
   url varchar(255),
   product_id integer references product(id)
);
create table cart(
   customer_id integer references customer(id),
   id serial primary key
);
create cart_product(
   cart_id integer references cart(id),
   product_id integer references product(id)
);

insert into customer(name, phone, email) values ('Vas', '001', 'vas@default.com');
insert into customer(name, phone, email) values ('Mik', '002', 'mik@default.com');

insert into product(name, description, price) values ('iPhone', 'cool phone', 100000);
insert into product(name, description, price) values ('Apple watch', 'cool watch', 50000);

insert into product_photo(url, product_id) values ('iphone_photo', 1);

select * from product_photo pp;
select pp.* from product_photo pp;

select pp.*, p.name from product_photo pp left join product p on p.id=pp.product_id;

alter table product_photo drop constraint product_photo_product_id_fkey;

delete from product_photo where id=2;

update product_photo set url='iphone_image_2' where id=1;

insert into cart(customer_id) value (1);
insert into cart_product(cart_id, product_id) values (1, 1), (1, 2);

select c.name, cart.id as cart_id
from customer c
left join cart on cart.customer_id=c.id;

```
