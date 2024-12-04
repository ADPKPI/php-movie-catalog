# Використовуємо офіційний образ PHP з підтримкою Apache
FROM php:8.2-apache

# Встановлюємо необхідні залежності для PHP та Node.js
RUN apt-get update && apt-get install -y \
    libpq-dev libzip-dev zip unzip curl \
    nodejs npm \
    && docker-php-ext-install pdo pdo_mysql

# Встановлюємо робочу директорію
WORKDIR /var/www/html

# Копіюємо всі файли проекту у контейнер
COPY . .

# Встановлюємо залежності Node.js та генеруємо фінальний CSS
RUN npm install && npx tailwindcss -i ./styles.css -o ./output.css --minify

# Налаштовуємо права доступу до файлів
RUN chown -R www-data:www-data /var/www/html && chmod -R 755 /var/www/html

# Включаємо модуль Apache mod_rewrite для підтримки URL
RUN a2enmod rewrite

# Запускаємо Apache
CMD ["apache2-foreground"]
