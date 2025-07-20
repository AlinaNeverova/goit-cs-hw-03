-- Отримати всі завдання певного користувача
select *
from tasks
where user_id = 1;

-- Вибрати завдання за певним статусом
select *
from tasks
where status_id = (select id from status where name = 'completed'); -- якщо хочемо шукати за ім'ям саме, а не id

-- Оновити статус конкретного завдання
update tasks
set status_id = (select id from status where name = 'in progress')
where id = 4;

-- Отримати список користувачів, які не мають жодного завдання
select u.*
from users u 
where id not in (select distinct user_id from tasks);

-- Додати нове завдання для конкретного користувача
insert into tasks (title, description, status_id, user_id)
values 
('Fix something', 
'Some description',
(select id from status where name = 'new'),
2);

-- Отримати всі завдання, які ще не завершено
select *
from  tasks
where status_id != (select id from status where name = 'completed');

-- Видалити конкретне завдання
delete from tasks
where id = 6;

-- Знайти користувачів з певною електронною поштою
select *
from users 
where email like '%erik%';

-- Оновити ім'я користувача
update users
set fullname = 'Alina N'
where id = 3;

-- Отримати кількість завдань для кожного статусу
select
s.name,
count(t.id) as tasks_count
from tasks t 
join status s on s.id = t.status_id
group by s.name;

-- Отримати завдання, які призначені користувачам з певною доменною частиною електронної пошти
select t.*
from tasks t 
left join users u on u.id = t.user_id
where u.email like '%@example.com';

-- Отримати список завдань, що не мають опису
select *
from tasks
where description is null;

-- Вибрати користувачів та їхні завдання, які є у статусі 'in progress'
select
u.id,
u.fullname,
t.title,
t.description,
t.created_at
from users u
inner join tasks t on u.id = t.user_id
where t.status_id = (select id from status where name = 'in progress')
order by u.id;

-- Отримати користувачів та кількість їхніх завдань
select
u.id,
u.fullname,
count(t.id) as tasks_count
from users u
left join tasks t on u.id = t.user_id
group by u.id, u.fullname
order by u.id;