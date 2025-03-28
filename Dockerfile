FROM php:8.2-apache

WORKDIR /var/www/html

RUN apt-get update && \
    apt-get install -y libpng-dev && \
    docker-php-ext-install pdo pdo_mysql gd \

RUN pecl install redis \
    && docker-php-ext-enable redis

EXPOSE 80

CMD ["apache2-foreground"]