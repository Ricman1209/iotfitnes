package com.ricardo.iotFitness.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import com.ricardo.iotFitness.model.Usuario;


public interface UsuarioRepository extends JpaRepository<Usuario, Integer> {
    boolean existsByEmail(String email);
}