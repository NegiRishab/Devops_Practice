package com.devops.superhero.controller;

import com.devops.superhero.dto.SuperheroRequest;
import com.devops.superhero.model.Superhero;
import com.devops.superhero.repository.SuperheroRepository;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/api/superheroes")
@CrossOrigin(origins = "*")
public class SuperheroController {

    private final SuperheroRepository repository;

    public SuperheroController(SuperheroRepository repository) {
        this.repository = repository;
    }

    @GetMapping
    public List<Superhero> getAll() {
        return repository.findAll();
    }

    @PostMapping
    public ResponseEntity<?> create(@RequestBody SuperheroRequest request) {
        if (request.getName() == null || request.getName().isBlank()
                || request.getPower() == null || request.getPower().isBlank()) {
            return ResponseEntity.badRequest()
                    .body(Map.of("error", "Name and power are required"));
        }

        Superhero superhero = new Superhero(
                request.getName().trim(),
                request.getPower().trim()
        );
        return ResponseEntity.status(HttpStatus.CREATED).body(repository.save(superhero));
    }
}
