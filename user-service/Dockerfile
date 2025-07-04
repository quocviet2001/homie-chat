FROM php:8.2-fpm

# Cài đặt các phụ thuộc cần thiết
RUN apt-get update && apt-get install -y \
    libpq-dev \
    zip unzip git \
    && docker-php-ext-install pdo pdo_pgsql

# Cài đặt Composer
RUN curl -sS https://getcomposer.org/installer | php -- --install-dir=/usr/local/bin --filename=composer

# Thiết lập thư mục làm việc
WORKDIR /var/www/html

# Sao chép code vào container
COPY . .

# Cài đặt dependencies của Laravel
RUN composer install --no-dev --optimize-autoloader

# Cấp quyền cho thư mục storage
RUN chown -R www-data:www-data storage bootstrap/cache
RUN chmod -R 775 storage bootstrap/cache

# Port 8001
EXPOSE 8001

# Chạy Laravel server
CMD ["php", "artisan", "serve", "--host=0.0.0.0", "--port=8001"]
