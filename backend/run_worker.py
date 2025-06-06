from celery.bin.celery import main as celery_main

if __name__ == '__main__':
    celery_main(["worker", "--app=app.worker", "--loglevel=info", "--pool=solo"]) 