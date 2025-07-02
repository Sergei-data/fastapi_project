-- Категории питомцев
INSERT INTO pet_categories (id, animal_type, size, slug) VALUES
  (1, 'Кошка', 'Маленький', 'cat-small'),
  (2, 'Собака', 'Средний', 'dog-medium');

-- Питомцы
INSERT INTO pets (id, name, description, age, breed, color, cuteness_rating, image_url, category_id, slug) VALUES
  (1, 'Барсик', 'Рыжий котенок', 2, 'Дворовая', 'Рыжий', 8.5, 'http://example.com/barsik.jpg', 1, 'barsik'),
  (2, 'Мурка', 'Белая кошка с зелеными глазами', 3, 'Сибирская', 'Белый', 9.2, 'http://example.com/murka.jpg', 1, 'murka'),
  (3, 'Шарик', 'Веселый и дружелюбный', 4, 'Лабрадор', 'Коричневый', 7.8, 'http://example.com/sharik.jpg', 2, 'sharik'),
  (4, 'Бобик', 'Большой и спокойный пес', 5, 'Овчарка', 'Черный', 7.0, 'http://example.com/bobik.jpg', 2, 'bobik'),
  (5, 'Рэкс', 'Активный и умный', 3, 'Бультерьер', 'Белый с пятнами', 8.0, 'http://example.com/reks.jpg', 2, 'reks');

-- Пользователи
INSERT INTO users (id, first_name, last_name, username, email, hashed_password, is_active, is_admin, is_supplier, is_customer) VALUES
  (1, 'Алексей', 'Иванов', 'alex', 'alex@example.com', 'hashed_password_admin', TRUE, TRUE, FALSE, FALSE),
  (2, 'Марина', 'Петрова', 'marina', 'marina@example.com', 'hashed_password_supplier', TRUE, FALSE, TRUE, FALSE);