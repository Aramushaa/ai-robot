from robot import Robot

robot = Robot("Robo")

cmd = ""

while True:
    try:
        cmd = input("Enter command (wake/sleep/exit): ").strip().lower()

        if cmd == "wake":
            print(robot.wake())
        elif cmd == "sleep":
            print(robot.sleep())
        elif cmd == "exit":
            print("Exiting the program.")
            break
        else:
            print("Invalid command. Please enter 'wake', 'sleep', or 'exit'.")
    except Exception as e:
        print(f"An error occurred: {e}")