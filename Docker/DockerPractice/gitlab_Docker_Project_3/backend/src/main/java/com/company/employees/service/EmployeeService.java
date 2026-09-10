package com.company.employees.service;

import com.company.employees.model.Employee;
import com.company.employees.repository.EmployeeRepository;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class EmployeeService {

    private final EmployeeRepository employeeRepository;

    public EmployeeService(EmployeeRepository employeeRepository) {
        this.employeeRepository = employeeRepository;
    }

    public List<Employee> getAllEmployees() {
        return employeeRepository.findAll();
    }

    public Employee getEmployee(Long id) {
        return employeeRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("Employee not found with id: " + id));
    }

    public Employee createEmployee(Employee employee) {
        return employeeRepository.save(employee);
    }

    public Employee updateEmployee(Long id, Employee employee) {
        Employee existing = getEmployee(id);
        existing.setName(employee.getName());
        existing.setEmail(employee.getEmail());
        existing.setEmployed(employee.getEmployed());
        existing.setTiming(employee.getTiming());
        existing.setRole(employee.getRole());
        existing.setDepartment(employee.getDepartment());
        return employeeRepository.save(existing);
    }

    public void deleteEmployee(Long id) {
        Employee existing = getEmployee(id);
        employeeRepository.delete(existing);
    }
}
