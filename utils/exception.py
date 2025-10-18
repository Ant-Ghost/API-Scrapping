def print_exception(exception: Exception):

    traceback = exception.__traceback__

    if traceback:
        line_no = traceback.tb_lineno
        file_name = traceback.tb_frame.f_code.co_filename
        function_name = traceback.tb_frame.f_code.co_name
        print(
            f"[Exception {type(exception).__name__}]"
            f"Error in {file_name} at "
            f"line {line_no} in "
            f"function {function_name}: {str(exception)}"
        )