# Lists available recipes
default:
  @just --list

# Run manage.py migrate
migrate:
  docker-compose exec -T application sh -c 'python manage.py migrate'

# Shell (backend)
shell:
  docker-compose exec application sh