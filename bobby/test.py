from navigate_robot import Navigator

def main():
    navigator = Navigator()

    navigator.static_navigation("Charger")
    navigator.static_navigation("Ian's room")
    navigator.static_navigation("Kitchen")
    navigator.static_navigation("Docking pose")

if __name__ == "__main__":
    main()