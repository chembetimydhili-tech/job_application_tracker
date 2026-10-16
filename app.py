applications = []

def add_application():
    company = input("Enter company name: ")
    role = input("Enter job role: ")
    status = input("Enter status (Applied/Interview/Selected/Rejected): ")

    application = {
        "company": company,
        "role": role,
        "status": status
    }

    applications.append(application)
    print("Application added successfully!\n")


def view_applications():
    if not applications:
        print("No applications added yet.\n")
        return

    for number, app in enumerate(applications, start=1):
        print(f"{number}. Company: {app['company']}")
        print(f"   Role: {app['role']}")
        print(f"   Status: {app['status']}\n")


while True:
    print("===== JOB APPLICATION TRACKER =====")
    print("1. Add application")
    print("2. View applications")
    print("3. Exit")

    choice = input("Choose an option: ")

    if choice == "1":
        add_application()
    elif choice == "2":
        view_applications()
    elif choice == "3":
        print("Thank you for using Job Application Tracker!")
        break
    else:
        print("Invalid choice. Please try again.\n")