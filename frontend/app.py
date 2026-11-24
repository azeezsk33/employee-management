
import streamlit as st
import requests
import os

# API URL
API_URL = os.getenv(
    "API_URL",
    "https://employee-management-1-rjhy.onrender.com"
).rstrip("/")

st.set_page_config(
    page_title="Employee Management System",
    page_icon="👨‍💼",
    layout="wide"
)

st.title("👨‍💼 Employee Management System")
st.caption("Manage your employee information easily")

st.sidebar.title("Navigation")

page = st.sidebar.radio(
    "Select Option",
    [
        "Dashboard",
        "Add Employee",
        "View Employees",
        "Search Employee",
        "Update Employee",
        "Delete Employee"
    ]
)


# API helper
def api_request(method, endpoint, **kwargs):
    try:
        response = requests.request(
            method,
            f"{API_URL}{endpoint}",
            timeout=10,
            **kwargs
        )
        return response

    except requests.RequestException as e:
        st.error(f"Backend connection failed: {e}")
        return None


# Dashboard
if page == "Dashboard":

    st.header("📊 Employee Dashboard")

    response = api_request("GET", "/dashboard/")

    if response and response.ok:

        data = response.json()

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Total Employees",
            data["total_employees"]
        )

        col2.metric(
            "Departments",
            len(data["departments"])
        )

        col3.metric(
            "Total Salary",
            f"₹{data['total_salary']:,.2f}"
        )

        st.subheader("Department-wise Employees")

        if data["departments"]:
            st.bar_chart(data["departments"])
        else:
            st.info("No employee data available.")


# Add Employee
elif page == "Add Employee":

    st.header("➕ Add New Employee")

    with st.form("employee_form"):

        emp_id = st.number_input(
            "Employee ID",
            min_value=1,
            step=1
        )

        name = st.text_input("Employee Name")

        department = st.selectbox(
            "Department",
            ["IT", "HR", "Finance", "Marketing", "Sales", "Other"]
        )

        salary = st.number_input(
            "Salary",
            min_value=1.0,
            step=1000.0
        )

        email = st.text_input("Email Address")

        submit = st.form_submit_button(
            "Add Employee"
        )

        if submit:

            if not name.strip() or not email.strip():
                st.error("Please enter name and email.")
            else:

                employee = {
                    "id": int(emp_id),
                    "name": name.strip(),
                    "department": department,
                    "salary": salary,
                    "email": email.strip()
                }

                response = api_request(
                    "POST",
                    "/employees/",
                    json=employee
                )

                if response and response.ok:
                    st.success("Employee added successfully!")

                elif response:
                    st.error(response.json().get(
                        "detail", "Unable to add employee"
                    ))


# View Employees
elif page == "View Employees":

    st.header("👥 All Employees")

    response = api_request("GET", "/employees/")

    if response and response.ok:

        employees = response.json()

        if employees:
            st.dataframe(
                employees,
                use_container_width=True,
                hide_index=True
            )
        else:
            st.info("No employees found.")


# Search Employee
elif page == "Search Employee":

    st.header("🔍 Search Employee")

    emp_id = st.number_input(
        "Enter Employee ID",
        min_value=1,
        step=1
    )

    if st.button("Search"):

        response = api_request(
            "GET",
            f"/employees/{int(emp_id)}"
        )

        if response and response.ok:

            st.success("Employee found!")

            st.json(response.json())

        elif response:
            st.error("Employee not found.")


# Update Employee
elif page == "Update Employee":

    st.header("✏️ Update Employee")

    response = api_request("GET", "/employees/")

    if response and response.ok:

        employees = response.json()

        if not employees:
            st.info("No employees available to update.")

        else:
            employee_ids = [
                emp["id"] for emp in employees
            ]

            emp_id = st.selectbox(
                "Select Employee ID",
                employee_ids
            )

            emp = next(
                item for item in employees
                if item["id"] == emp_id
            )

            with st.form("update_form"):

                name = st.text_input(
                    "Employee Name",
                    value=emp["name"]
                )

                department = st.text_input(
                    "Department",
                    value=emp["department"]
                )

                salary = st.number_input(
                    "Salary",
                    min_value=1.0,
                    value=float(emp["salary"])
                )

                email = st.text_input(
                    "Email",
                    value=emp["email"]
                )

                submit = st.form_submit_button(
                    "Update Employee"
                )

                if submit:

                    updated_employee = {
                        "id": emp_id,
                        "name": name.strip(),
                        "department": department.strip(),
                        "salary": salary,
                        "email": email.strip()
                    }

                    if not name.strip() or not department.strip():
                        st.error("Name and department are required.")
                    else:
                        result = api_request(
                            "PUT",
                            f"/employees/{emp_id}",
                            json=updated_employee
                        )

                        if result and result.ok:
                            st.success(
                                "Employee updated successfully!"
                            )
                        elif result:
                            st.error(result.json().get(
                                "detail", "Update failed"
                            ))


# Delete Employee
elif page == "Delete Employee":

    st.header("🗑️ Delete Employee")

    response = api_request("GET", "/employees/")

    if response and response.ok:

        employees = response.json()

        if not employees:
            st.info("No employees available to delete.")

        else:
            emp_ids = [
                emp["id"] for emp in employees
            ]

            emp_id = st.selectbox(
                "Select Employee ID",
                emp_ids
            )

            if st.button("Delete Employee", type="primary"):

                result = api_request(
                    "DELETE",
                    f"/employees/{emp_id}"
                )

                if result and result.ok:
                    st.success(
                        "Employee deleted successfully!"
                    )
                elif result:
                    st.error("Unable to delete employee.")
