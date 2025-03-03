import time
from datetime import datetime
import sqlite3
import CommonLayer.State.user_state
from DataAccessLayer import sqlite_database_name


def performance_logger_decorator(class_name):
    def decortor(main_function):
        def wrapper(*args, **kwargs):
            function_name = main_function.__name__
            call_datetime = datetime.now()
            start_time = time.time()
            output = main_function(*args, **kwargs)
            end_time = time.time()

            user_id = CommonLayer.State.user_state.current_user_id
            execution_time = end_time - start_time

            with sqlite3.connect(sqlite_database_name) as connection:
                cursor = connection.cursor()
                cursor.execute(f"""
                INSERT INTO PerformanceLogger(function_name,execution_time,call_datetime,user_id,class_name)
                VALUES ('{function_name}',{execution_time},'{call_datetime}',{user_id},'{class_name}')""")
                connection.commit()
            return output

        return wrapper

    return decortor
