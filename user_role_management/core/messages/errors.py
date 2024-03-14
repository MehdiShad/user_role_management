

EMPTY_COMPANY = "The company field is empty. Please select or enter your company to proceed."
NOT_FOUND_PROCESS_MESSAGE = "We couldn't find a service called {process_name} running."
UNAUTHORIZED_ACTION = "Looks like you need a different level of access to perform this action. Please contact your administrator for assistance."













def not_found_processes(process_name: str) -> str:
    return NOT_FOUND_PROCESS_MESSAGE.format(process_name=process_name)
