package com.ricardo.iotFitness.model;

import jakarta.persistence.*;
import lombok.*;

@Entity
@Table(name = "usuario")

//lo nuevo de lombok
//@data es como el inicializador principal que nos genera gettes y setters
//
@Data
//crea un construcro vacio automaticamente
@NoArgsConstructor
//lo contrario a @noargscontructor, nos genera todos los atributos
@AllArgsConstructor

public class Usuario {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer idUsuario;

    @Column(nullable = false, length = 100)
    private String nombres;

    @Column(nullable = false, length = 100)
    private String apellidos;

    @Column(nullable = false, unique = true, length = 150)
    private String email;

    private String fechaNacimiento;

    @Column(length = 1)
    private String genero;
}