package com.company.employees.config;

import com.company.employees.model.Employee;
import com.company.employees.repository.EmployeeRepository;
import org.springframework.boot.CommandLineRunner;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

import java.util.List;

@Configuration
public class DataInitializer {

    @Bean
    CommandLineRunner seedEmployees(EmployeeRepository employeeRepository) {
        return args -> {
            if (employeeRepository.count() == 0) {
                List<Employee> employees = List.of(
                        new Employee("Aarav Sharma", "aarav@company.com", true, "09:00-17:00", "Software Engineer", "Engineering"),
                        new Employee("Priya Verma", "priya@company.com", true, "10:00-18:00", "QA Analyst", "Quality"),
                        new Employee("Rohan Mehta", "rohan@company.com", true, "09:30-17:30", "DevOps Engineer", "Infrastructure"),
                        new Employee("Neha Iyer", "neha@company.com", true, "11:00-19:00", "UI Designer", "Design"),
                        new Employee("Vikram Nair", "vikram@company.com", true, "08:00-16:00", "Product Manager", "Product"),
                        new Employee("Ishita Singh", "ishita@company.com", false, "09:00-17:00", "Business Analyst", "Business"),
                        new Employee("Karan Patel", "karan@company.com", true, "12:00-20:00", "Support Engineer", "Support"),
                        new Employee("Meera Rao", "meera@company.com", true, "09:00-17:00", "HR Specialist", "Human Resources"),
                        new Employee("Rahul Das", "rahul@company.com", false, "10:00-18:00", "Accountant", "Finance"),
                        new Employee("Ananya Gupta", "ananya@company.com", true, "09:00-17:00", "Marketing Lead", "Marketing")
                );
                employeeRepository.saveAll(employees);
            }
        };
    }
}
