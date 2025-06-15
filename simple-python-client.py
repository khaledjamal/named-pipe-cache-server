import win32file
import win32pipe
import pywintypes

PIPE_NAME = r"\\.\pipe\KeyValuePipe"

def send_command(command):
    handle = None
    try:
        # Open connection to the named pipe
        handle = win32file.CreateFile(
            PIPE_NAME,
            win32file.GENERIC_READ | win32file.GENERIC_WRITE,
            0,
            None,
            win32file.OPEN_EXISTING,
            0,
            None,
        )

        # Send command to the server
        win32file.WriteFile(handle, command.encode('utf-8'))

        # Read response from the server
        result, data = win32file.ReadFile(handle, 4096)
        return data.decode('utf-8')

    except pywintypes.error as e:
        if e.winerror == 2:  # ERROR_FILE_NOT_FOUND
            return "Error: Cache server not running"
        return f"Error: {str(e)}"
    except Exception as e:
        return f"Error: {str(e)}"
    finally:
        if handle:
            win32file.CloseHandle(handle)

# Example usage
if __name__ == "__main__":
    print("SET city dubai ->", send_command("SET city dubai"))
    print("GET city ->", send_command("GET city"))
    print("G city ->", send_command("G city"))  # Short form of GET