package com.devops.superhero.repository;

import com.devops.superhero.model.Superhero;
import org.springframework.data.jpa.repository.JpaRepository;

public interface SuperheroRepository extends JpaRepository<Superhero, Long> {
}
