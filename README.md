# Django Celery Stack

English |  [中文](README.zh.md)

A comprehensive stack solution that ensures seamless compatibility between Celery and Django, integrating key components
such as django-celery-beat, django-celery-result, and django-celery-progress. This integration provides web developers
with a robust framework for handling asynchronous tasks, scheduling, and tracking task execution within their Django
projects.

In addition, its interface and interaction are very friendly and modern, and it has overcome the traditional interaction
shortcomings of Django by referencing [DjangoAsyncAdmin](https://github.com/Haoke98/DjangoAsyncAdmin).

![](assets/registeredTaskRunForm.png)

### Django Celery Stack & Admin offers the following key features:

* **Asynchronous Task Queue** :

      Utilize Celery’s distributed message passing system to delegate CPU-bound tasks to the background, improving the responsiveness and performance of the application.

* Scheduled Task Scheduler:

      With the built-in Celery Beat scheduler, easily arrange periodic tasks such as data synchronization, report generation, etc.

* Task Result Tracking:

      Leverage Celery’s result backend to persist task execution results, making it easier to debug and monitor task status.

* Progress Updates:

      By integrating with django-celery-progress, provide real-time task progress updates to users for interactive feedback.

* Optimized Management Interface:

      Building on the foundation of the three projects, DjangoAsyncAdmin is used to optimize and enhance the interaction and management pages, making it more intuitive and convenient to manage tasks and monitor progress.

* Easy to Integrate and Extend:

      The design of Django Celery Stack & Admin is flexible, allowing for easy integration with other Django applications and Celery components to meet various requirements.

![](assets/registeredTaskList.png)
For both traditional web developers handling substantial data processing needs and system administrators tasked with
intricate scheduling, this full stack solution for Celery and Django compatibility is the optimal selection.
It delivers a proficient and scalable framework for managing asynchronous tasks and scheduling, enhancing the
performance of your Django projects. Embrace this solution today and begin reaping the benefits of streamlined task
management and scheduling within your Django environment.
### Usage
1. Install
    ```shell
    pip install django-celery-stack
    ```
2. Django project configuration
    
    * Register APP (settings.py)
      ```python
        # Application definition
        INSTALLED_APPS = [
          ...
          django_celery_stack
          ...
        ]
      ```
    
    * configure the result backend (settings.py)
        ```python
        CELERY_RESULT_BACKEND = "django_celery_stack.backends:CustomDatabaseBackend"
        ```
### Develop & Contribution

1. Clone the project to your local.
    ```shell
    git clone https://github.com/Haoke98/django-celery-stack.git
   ```
2. Build the package.
    ```shell
    python setup.py build sdist
    ```
3. Deploy to [PyPI](https://pypi.org).
    ```shell
    twine upload dist/* 
   ```