#!/usr/bin/env bash

APP_HOST=${APP_HOST:-"0.0.0.0"}
APP_PORT=${APP_PORT:-"8000"}

ProgName=$(basename $0)

sub_help(){
    echo "Usage: $ProgName <subcommand> [options]\n"
    echo "Subcommands:"
    echo "    migrate           Run migrations"
    echo "    collectstatic     Collect Static Files and exit"
    echo "    createsuperuser   Create default super admin user with login 'admin' and password='admin' and exit"
    echo "    django            Run any django command and exit"
    echo "    celery            Run Celery worker"
    echo "    serve             Run WSGI server"
    echo ""
    echo "For help with each subcommand run:"
    echo "$ProgName <subcommand> -h|--help"
    echo ""
}

sub_migrate(){
    django-admin createcachetable
    django-admin migrate --noinput
}

sub_collectstatic(){
    django-admin collectstatic --noinput
}

sub_createsuperuser(){
    echo "from django.contrib.auth import get_user_model; bool(get_user_model().objects.filter(username='admin').count()) or get_user_model().objects.create_superuser('admin', 'admin@example.com', 'admin')" | django-admin shell
}

sub_django(){
    django-admin $@
}

sub_devserver(){
    django-admin runserver ${APP_HOST}:${APP_PORT}
}

subcommand=$1
case $subcommand in
    "" | "-h" | "--help")
        sub_help
        ;;
    *)
        shift
        sub_${subcommand} $@
        if [ $? = 127 ]; then
            echo "Error: '$subcommand' is not a known subcommand." >&2
            echo "       Run '$ProgName --help' for a list of known subcommands." >&2
            exit 1
        fi
        ;;
esac