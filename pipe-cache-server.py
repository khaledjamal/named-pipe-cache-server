import threading
import win32pipe, win32file, win32con
import pywintypes
import os
import ctypes
import time
import sys
import datetime

# Create a log file
#log_file = open("cache.log", "w", encoding="utf-8")

# Custom logging function that writes to both console and file
def log(message):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    formatted_message = f"[{timestamp}] {message}"
    print(formatted_message)
    #log_file.write(formatted_message + "\n")
    #log_file.flush()  # Force write to disk immediately

PIPE_NAME = r'\\.\pipe\KeyValuePipe'

# In-memory key-value cache
cache = {}

def handle_client(pipe):
    try:
        #log("Client connected, starting communication loop")
        
        # Keep the connection open and handle multiple commands
        while True:
            try:
                # Read data from the client (up to 4096 bytes)
                #log("Waiting for client command...")
                result, data = win32file.ReadFile(pipe, 4096)
                
                # Decode the incoming bytes as UTF-8 and remove any extra whitespace
                command = data.decode('utf-8').strip()
                log(f"Received command: '{command}'")
                
                # Process the command
                parts = command.split()
                if not parts:
                    response = "ERROR: Empty command"
                elif parts[0].upper() == "SET" and len(parts) >= 3:
                    key = parts[1]
                    # Support values with spaces by joining all parts beyond the key
                    value = " ".join(parts[2:])
                    cache[key] = value
                    #log(f"SET operation - Key: '{key}', Value: '{value}'")
                    response = "OK"
                elif parts[0].upper() == "GET" and len(parts) == 2:
                    key = parts[1]
                    response = cache.get(key, "")
                    #log(f"GET operation - Key: '{key}', Returned: '{response}'")
                elif parts[0][0].upper() == "G" and len(parts) == 2:
                    key = parts[1]
                    response = cache.get(key, "")
                    #log(f"G operation - Key: '{key}', Returned: '{response}'")
                else:
                    response = "ERROR: Unknown command"
                    log(f"ERROR: Unknown command format: {command}")
                
                # Send the response
                log(f"Sending response: '{response}'")
                win32file.WriteFile(pipe, response.encode('utf-8'))
                #log("Response sent successfully, waiting for next command")
                
            except win32pipe.error as e:
                # Client disconnected or pipe broke
                #log(f"Pipe error: {e}")
                break
            except Exception as e:
                log(f"Error processing command: {e}")
                # Try to send error message back to client
                try:
                    error_msg = f"SERVER ERROR: {str(e)}"
                    win32file.WriteFile(pipe, error_msg.encode('utf-8'))
                except:
                    pass
                break
                
    except Exception as e:
        log(f"Exception in client handler: {e}")
    finally:
        try:
            #log("Client disconnected, cleaning up pipe")
            win32pipe.DisconnectNamedPipe(pipe)
            win32file.CloseHandle(pipe)
            #log("Pipe closed, ready for new connections")
        except Exception as e:
            log(f"Error while cleaning up pipe: {e}")

def create_pipe_server():
    try:
        pipe = win32pipe.CreateNamedPipe(
            PIPE_NAME,
            win32pipe.PIPE_ACCESS_DUPLEX,
            win32pipe.PIPE_TYPE_MESSAGE | win32pipe.PIPE_READMODE_MESSAGE | win32pipe.PIPE_WAIT,
            win32pipe.PIPE_UNLIMITED_INSTANCES,  # Allow multiple instances
            4096,       # Out buffer size
            4096,       # In buffer size
            0,          # Timeout in milliseconds
            None)       # Default security attributes
        return pipe
    except Exception as e:
        log(f"Error creating pipe: {e}")
        return None

def main():
    try:
        # Diagnostic information
        log(f"Python process ID: {os.getpid()}")
        log(f"Running as admin: {ctypes.windll.shell32.IsUserAnAdmin() != 0}")
        
        log(f"Starting pipe server on {PIPE_NAME}")
        log(f"Current cache state: {cache}")
        
        while True:
            try:
                pipe = create_pipe_server()
                if pipe is None:
                    log("Failed to create pipe, retrying in 1 second...")
                    time.sleep(1)
                    continue
                    
                #log("Waiting for client connection on " + PIPE_NAME)
                win32pipe.ConnectNamedPipe(pipe, None)
                #log("Client connected, starting handler thread")
                
                # Process the client connection in a new thread
                client_thread = threading.Thread(target=handle_client, args=(pipe,))
                client_thread.daemon = True
                client_thread.start()
                
            except pywintypes.error as e:
                log(f"Windows error: {e}")
                if e.winerror == 231:  # ERROR_PIPE_BUSY
                    log("Pipe busy, waiting before retry...")
                    time.sleep(1)
                elif e.winerror == 109:  # ERROR_BROKEN_PIPE
                    log("Broken pipe, creating new one...")
                else:
                    log("Unexpected error, retrying...")
                    time.sleep(1)
            except Exception as e:
                log(f"Unexpected error: {e}")
                time.sleep(1)
    except KeyboardInterrupt:
        log("Server shutting down due to keyboard interrupt")
    except Exception as e:
        log(f"Fatal error: {e}")
    finally:
        pass
        #log_file.close()

if __name__ == "__main__":
    main()